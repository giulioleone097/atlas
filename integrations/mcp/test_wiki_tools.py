import asyncio
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from mcp.server.mcpserver.exceptions import ToolError

from server import create_server, load_package
from wiki_tools import WikiTools


class WikiToolsTests(unittest.TestCase):
    def setUp(self):
        runtime_source = os.environ.get("SPOTTER_RUNTIME_DIR")
        if runtime_source is None:
            self.skipTest("set SPOTTER_RUNTIME_DIR to the packaged Spotter runtime")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.package_root = Path(self.temp.name) / "spotter"
        for directory in ("core", "skills/grill", ".codex-plugin"):
            (self.package_root / directory).mkdir(parents=True)
        (self.package_root / "core/SPOTTER.md").write_text("Doctrine", encoding="utf-8")
        (self.package_root / ".codex-plugin/plugin.json").write_text(
            '{"name":"spotter","version":"1.0.0"}', encoding="utf-8"
        )
        (self.package_root / "skills/grill/SKILL.md").write_text(
            "---\nname: grill\ndescription: Triage a request\n---\n", encoding="utf-8"
        )
        shutil.copytree(Path(runtime_source) / "spotter_wiki", self.package_root / "runtime/spotter_wiki")
        self.wiki_root = Path(self.temp.name) / "wiki"
        (self.wiki_root / "raw/manifests").mkdir(parents=True)
        (self.wiki_root / "wiki").mkdir()
        (self.wiki_root / "SCHEMA.md").write_text("schema", encoding="utf-8")
        (self.wiki_root / "raw/manifests/sources.csv").write_text(
            "source_id,title,type,path_or_url,date,owner,status,notes\n", encoding="utf-8"
        )
        (self.wiki_root / "wiki/index.md").write_text("---\ntitle: Index\n---\n", encoding="utf-8")
        self.package = load_package("spotter", self.package_root)

    def test_rejects_incomplete_root_and_marks_overwrites(self):
        from wiki_tools import WIKI_WRITE
        self.assertTrue(WIKI_WRITE.destructive_hint)
        (self.wiki_root / "raw/manifests/sources.csv").unlink()
        with self.assertRaisesRegex(ValueError, "uninitialized"):
            WikiTools(self.package, self.wiki_root, writable=True)

    def test_read_only_surface_and_atlas_isolation(self):
        wiki = WikiTools(self.package, self.wiki_root, writable=False)
        server = create_server(self.package, wiki)

        async def assert_tools():
            listed = await server.call_tool("wiki_list", {})
            self.assertFalse(listed.structured_content["writable"])
            self.assertIn("wiki/index.md", str(listed.structured_content["files"]))
            with self.assertRaises(ToolError):
                await server.call_tool("wiki_write", {"path": "wiki/new.md", "content": "x", "expected_revision": ""})

        asyncio.run(assert_tools())
        default_server = create_server(self.package)
        self.assertEqual(
            sorted(default_server._tool_manager._tools),
            ["list_workflows", "load_workflow", "read_reference"],
        )
        atlas = dict(self.package, name="atlas")
        with self.assertRaisesRegex(ValueError, "only for the Spotter"):
            WikiTools(atlas, self.wiki_root, writable=False)

    def test_write_requires_current_revision_and_rejects_escaped_path(self):
        server = create_server(self.package, WikiTools(self.package, self.wiki_root, writable=True))

        async def assert_cas_and_boundary():
            created = await server.call_tool(
                "wiki_write", {"path": "wiki/new.md", "content": "one", "expected_revision": ""}
            )
            self.assertTrue(created.structured_content["changed"])
            with self.assertRaises(ToolError):
                await server.call_tool(
                    "wiki_write", {"path": "wiki/new.md", "content": "two", "expected_revision": "stale"}
                )
            with self.assertRaises(ToolError):
                await server.call_tool(
                    "wiki_read", {"path": "../outside.md"}
                )

        asyncio.run(assert_cas_and_boundary())


if __name__ == "__main__":
    unittest.main()
