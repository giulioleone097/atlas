#!/usr/bin/env python3
"""Create self-contained Claude plugin ZIPs from tracked source files."""
import argparse
import json
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


ALLOWED = ("skills/", "core/", "agents/", "scripts/", "hooks/", "runtime/", "assets/")
ROOT_FILES = {"AGENTS.md", "README.md", "LICENSE", ".claude/CLAUDE.md", ".claude-plugin/plugin.json"}


def die(message):
    raise SystemExit(f"error: {message}")


def tracked_files(root):
    import subprocess
    result = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=False)
    if result.returncode:
        die(f"{root} is not a readable git worktree")
    paths = [item.decode() for item in result.stdout.split(b"\0") if item]
    selected = []
    for rel in paths:
        keep = rel in ROOT_FILES or rel.startswith(ALLOWED)
        if root.name == "atlas" and rel.startswith("docs/atlas/"):
            keep = True
        if "/tests/" in rel or "/test_" in rel or rel.startswith("evals/"):
            keep = False
        if root.name == "llm-wiki-kit" and rel.startswith("agents/copilot-cli/"):
            keep = False
        if root.name == "llm-wiki-kit" and (
            rel in {"Cargo.toml", "Cargo.lock"}
            or (rel.startswith("crates/") and (rel.endswith("/Cargo.toml") or "/src/" in rel))
        ):
            keep = True
        if keep:
            selected.append(rel)
    return selected


def safe_rel(path):
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or str(pure) in {"", "."}:
        die(f"unsafe archive path: {path}")
    return pure


def host_reference(name, core_file, is_wiki):
    core = (
        f"Read `{core_file}` once per task through this plugin root before acting; it is the canonical doctrine. "
        if core_file
        else "No bundled core doctrine is available; follow host and user instructions. "
    )
    wiki = ""
    if is_wiki:
        wiki = (
            "For wiki operations, persist only to the real store declared by the user or discovered schema; cloud scratch and this export are not stores. "
            "Use an existing `llm-wiki` runtime when present; otherwise `cargo run --locked --manifest-path <plugin-root>/Cargo.toml --target-dir <outside-plugin-dir>/llm-wiki-target -- ...` keeps build artifacts outside this immutable plugin. "
            "If Cargo is unavailable, state that exact runtime gap and perform independent reads only; never fabricate lint results. "
        )
    spotter = ""
    if name == "spotter":
        spotter = (
            "This full Claude plugin archive includes Spotter's bundled Python helper; this differs from earlier content-only native skill exports. "
            "Use it only after discovering an actual shell and Python runtime. Preserve the selected context root and read-only rules; an exported archive or cloud scratch is never the persistent store. "
        )
    return f"""# Claude host reference\n\nThis is the Claude adaptation exported from `{name}` (source version is retained in its manifest). Preserve host and user instruction precedence. Resolve the plugin root from the actual skill location by walking upward until `.claude-plugin/plugin.json`; never assume the working directory. {core}Discover actual host capabilities before using them. Native bundled agents and hooks remain discoverable when the host supports them; disclose unavailable actors or hooks instead of simulating them. {spotter}{wiki}"""


def prepend_reference(path):
    text = path.read_text()
    marker = "<!-- claude-host-reference -->"
    if marker in text:
        return
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                lines.insert(index + 1, f"\n{marker}\nRead `../../references/claude-host.md` before acting.\n\n")
                path.write_text("".join(lines))
                return
    path.write_text(f"{marker}\nRead `../../references/claude-host.md` before acting.\n\n{text}")


def adapt_wiki_agent(destination):
    agent = destination / "agents/wiki.md"
    if not agent.exists():
        return []
    text = agent.read_text()
    removed = [name for name in ("context-management", "programmatic-tool-calling") if f"  - {name}\n" in text]
    for name in removed:
        text = text.replace(f"  - {name}\n", "")
    if removed:
        agent.write_text(text)
    return removed


def reject_symlinked_path(root, rel):
    node = root
    for part in PurePosixPath(rel).parts:
        node /= part
        if node.is_symlink():
            die(f"refusing symlink inside selected path: {node}")


def copy_plugin(name, source, destination):
    source = source.resolve(strict=True)
    if not source.is_dir():
        die(f"plugin source is not a directory: {source}")
    if destination.exists():
        die(f"refusing to overwrite existing output: {destination}")
    files = tracked_files(source)
    if ".claude-plugin/plugin.json" not in files:
        die(f"missing tracked .claude-plugin/plugin.json in {source}")
    for rel in files:
        safe_rel(rel)
        src = source / rel
        reject_symlinked_path(source, rel)
        if not src.is_file():
            die(f"tracked selected path is not a regular file: {src}")
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    manifest_path = destination / ".claude-plugin/plugin.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("name") != name:
        die(f"--plugin name {name!r} differs from manifest name {manifest.get('name')!r}")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    references = destination / "references"
    references.mkdir()
    core_file = next((item for item in ("core/ATLAS.md", "core/SPOTTER.md") if (destination / item).is_file()), None)
    (references / "claude-host.md").write_text(host_reference(name, core_file, name == "llm-wiki-kit"))
    for skill in (destination / "skills").glob("*/SKILL.md") if (destination / "skills").is_dir() else []:
        prepend_reference(skill)
    return files, adapt_wiki_agent(destination)


def assert_archive(path):
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            safe_rel(info.filename)
            if info.is_dir() or (info.external_attr >> 16) & 0o170000 == 0o120000:
                die(f"archive contains directory or symlink entry: {info.filename}")


def package(directory, zip_path):
    if zip_path.exists():
        die(f"refusing to overwrite existing output: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                die(f"refusing internal symlink: {path}")
            if path.is_file():
                archive.write(path, path.relative_to(directory).as_posix())
    assert_archive(zip_path)
    with zipfile.ZipFile(zip_path) as archive:
        for path in sorted(directory.rglob("*")):
            if path.is_file() and archive.read(path.relative_to(directory).as_posix()) != path.read_bytes():
                die(f"ZIP read-back differs: {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin", action="append", required=True, metavar="NAME=PATH")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    output = args.out.resolve()
    if output.exists() and not output.is_dir():
        die(f"output is not a directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    plugins = []
    for value in args.plugin:
        if "=" not in value:
            die(f"--plugin must be NAME=PATH: {value}")
        name, raw_path = value.split("=", 1)
        if not name or "/" in name or "\\" in name or name in {".", ".."}:
            die(f"unsafe plugin name: {name!r}")
        plugins.append((name, Path(raw_path)))
    if len({name for name, _ in plugins}) != len(plugins):
        die("duplicate plugin name")
    with tempfile.TemporaryDirectory(dir=output.parent, prefix="claude-export-") as temporary:
        temporary = Path(temporary)
        for name, source in plugins:
            staged = temporary / name
            selected, removed = copy_plugin(name, source, staged)
            final_dir, final_zip = output / name, output / f"{name}.zip"
            if final_dir.exists() or final_zip.exists():
                die(f"refusing to overwrite existing output for {name}")
            package(staged, temporary / f"{name}.zip")
            shutil.move(str(staged), final_dir)
            shutil.move(str(temporary / f"{name}.zip"), final_zip)
            delta = f"; removed unavailable agent preloads: {', '.join(removed)}" if removed else ""
            print(f"{name}: {len(selected)} source files, {sum(1 for p in final_dir.rglob('*') if p.is_file())} package files, {final_zip}{delta}")


if __name__ == "__main__":
    main()
