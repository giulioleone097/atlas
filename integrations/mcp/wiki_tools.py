"""Optional, operator-bound private-wiki tools for the Spotter MCP server."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations


WIKI_READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)
WIKI_WRITE = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=True,
    idempotentHint=True,
    openWorldHint=False,
)


def _load_runtime(package_root: Path) -> tuple[type[Any], type[ValueError]]:
    """Load only the runtime packaged with this configured Spotter plugin."""

    package_root = package_root.resolve()
    runtime = package_root / "runtime" / "spotter_wiki"
    components = [package_root / "runtime", runtime, *runtime.rglob("*.py")]
    if any(path.is_symlink() or not path.resolve().is_relative_to(package_root)
           for path in components):
        raise ValueError("private-wiki runtime must stay inside its Spotter package")
    init_file = runtime / "__init__.py"
    store_file = runtime / "store.py"
    if not init_file.is_file() or not store_file.is_file():
        raise ValueError("configured Spotter plugin has no private-wiki runtime")
    module_name = "_spotter_wiki_" + hashlib.sha256(
        str(runtime.resolve()).encode("utf-8")
    ).hexdigest()[:16]
    spec = importlib.util.spec_from_file_location(
        module_name, init_file, submodule_search_locations=[str(runtime)]
    )
    if spec is None or spec.loader is None:
        raise ValueError("configured Spotter plugin has an unreadable private-wiki runtime")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        store_type = module.WikiStore
        error_type = module.WikiError
    except (AttributeError, ImportError, OSError) as error:
        sys.modules.pop(module_name, None)
        raise ValueError("configured Spotter plugin has an invalid private-wiki runtime") from error
    if not isinstance(store_type, type) or not isinstance(error_type, type):
        raise ValueError("configured Spotter plugin has an invalid private-wiki runtime")
    return store_type, error_type


class WikiTools:
    """Expose a configured WikiStore without revealing its filesystem root."""

    def __init__(self, package: dict[str, Any], root: Path, writable: bool) -> None:
        if package["name"] != "spotter":
            raise ValueError("private wiki is available only for the Spotter plugin")
        package_root = package.get("_root")
        if not isinstance(package_root, Path):
            raise ValueError("configured Spotter plugin has no private-wiki runtime location")
        if root.is_symlink() or not root.is_dir():
            raise ValueError("wiki root is missing or not a directory")
        store_type, self._wiki_error = _load_runtime(package_root)
        self._store = store_type(root, writable=writable)
        self.writable = writable
        try:
            index = self._store.read("wiki/index.md")
            self._store.read("raw/manifests/sources.csv")
            if not index["content"].startswith("---\n"):
                raise ValueError("wiki index has no frontmatter")
            problems = self._store.check()["errors"]
            if any("sources.csv" in problem for problem in problems):
                raise ValueError("wiki source manifest is invalid")
        except self._wiki_error as error:
            raise ValueError("wiki root is uninitialized") from error

    def _call(self, method: str, *args: Any) -> Any:
        try:
            return getattr(self._store, method)(*args)
        except self._wiki_error as error:
            raise ToolError(str(error)) from None
        except OSError:
            raise ToolError("wiki filesystem operation failed") from None

    def list(self) -> dict[str, Any]:
        return {
            "capabilities": {
                "read": True,
                "search": True,
                "check": True,
                "write": self.writable,
                "register_source": self.writable,
                "compose": self.writable,
            },
            "writable": self.writable,
            "files": self._call("list_files"),
        }

    def read(self, path: str) -> dict[str, Any]:
        return self._call("read", path)

    def search(self, query: str, limit: int = 20) -> dict[str, Any]:
        return self._call("search", query, limit)

    def check(self) -> dict[str, Any]:
        return self._call("check")

    def write(self, path: str, content: str, expected_revision: str) -> dict[str, Any]:
        return self._call("write", path, content, expected_revision)

    def register_source(
        self, source: dict[str, str], expected_revision: str
    ) -> dict[str, Any]:
        return self._call("register_source", source, expected_revision)

    def compose(self, changes: list[dict[str, str]]) -> dict[str, Any]:
        return self._call("compose", {"changes": changes})


def register_wiki_tools(server: Any, wiki: WikiTools) -> None:
    """Register the live wiki surface after its local configuration succeeds."""

    @server.tool(
        description="List private-wiki file metadata and its configured capabilities.",
        annotations=WIKI_READ_ONLY,
        structured_output=True,
    )
    def wiki_list() -> dict[str, Any]:
        return wiki.list()

    @server.tool(
        description="Read one allowlisted private-wiki file by relative path.",
        annotations=WIKI_READ_ONLY,
        structured_output=True,
    )
    def wiki_read(path: str) -> dict[str, Any]:
        return wiki.read(path)

    @server.tool(
        description="Search private-wiki evidence with a bounded result limit.",
        annotations=WIKI_READ_ONLY,
        structured_output=True,
    )
    def wiki_search(query: str, limit: int = 20) -> dict[str, Any]:
        return wiki.search(query, limit)

    @server.tool(
        description="Check private-wiki consistency and report errors and warnings.",
        annotations=WIKI_READ_ONLY,
        structured_output=True,
    )
    def wiki_check() -> dict[str, Any]:
        return wiki.check()

    if not wiki.writable:
        return

    @server.tool(
        description="Persist compiled personal context together with its source registry, index and append-only log. Read current files first; pass changes with path, content and expected_revision. Include raw/manifests/sources.csv, wiki/index.md, wiki/log.md and at least one sourced content page. Preflights the whole batch; writes are atomic per file, not a multi-file transaction. Identical retries are safe. Return read-back revisions before claiming saved context.",
        annotations=WIKI_WRITE,
        structured_output=True,
    )
    def wiki_compose(changes: list[dict[str, str]]) -> dict[str, Any]:
        return wiki.compose(changes)

    @server.tool(
        description="Write one private-wiki file using expected_revision from wiki_read/list; empty string requires a new file. Stale revisions fail.",
        annotations=WIKI_WRITE,
        structured_output=True,
    )
    def wiki_write(path: str, content: str, expected_revision: str) -> dict[str, Any]:
        return wiki.write(path, content, expected_revision)

    @server.tool(
        description="Upsert one source using the current revision of raw/manifests/sources.csv; stale revisions fail.",
        annotations=WIKI_WRITE,
        structured_output=True,
    )
    def wiki_register_source(
        source: dict[str, str], expected_revision: str
    ) -> dict[str, Any]:
        return wiki.register_source(source, expected_revision)
