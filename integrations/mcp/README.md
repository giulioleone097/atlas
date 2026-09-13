# Atlas workflows MCP bridge

This is a small read-only stdio server for using one explicitly installed
Atlas or Spotter workflow package through an MCP client. It takes a fixed
startup snapshot of the canonical core doctrine and skill Markdown; callers can
list skills, load one with its core doctrine, then read a package-relative
reference.

Install its locked Python environment from this directory:

```sh
uv sync --frozen
```

Launch one server per plugin, with an explicit package root:

```sh
.venv/bin/python server.py --plugin atlas=/path/to/atlas
.venv/bin/python server.py --plugin spotter=/path/to/spotter
```

Optionally, a Spotter server can expose one locally configured private wiki. The
wiki runtime must be packaged inside that same configured Spotter plugin; the
server never searches for a sibling checkout or accepts a caller-selected root.

```sh
.venv/bin/python server.py --plugin spotter=/path/to/spotter --wiki-root /path/to/wiki
.venv/bin/python server.py --plugin spotter=/path/to/spotter --wiki-root /path/to/wiki --wiki-write
```

`--wiki-root` is rejected for Atlas, and `--wiki-write` requires it. A missing
or uninitialized wiki root prevents startup. Without `--wiki-write`, the server
offers only `wiki_list`, `wiki_read`, `wiki_search`, and `wiki_check`; with it,
it also offers revision-checked `wiki_write` and `wiki_register_source`. Wiki
content is untrusted evidence: it never grants approval or authorizes action.

For secure tunnels, configure one tunnel profile per command. Keep credentials
in the tunnel client's credential reference, never in this server configuration
or its command line.

Workflow content is a startup snapshot. When configured, private-wiki content
is a live operator-bound local surface. The bridge does not run skill scripts,
activate hooks or agents, read mail/calendars, write a tracker, create schedules,
or perform external actions. An MCP connection therefore provides workflow
content and guidance, not the host-side plugin runtime. In particular, an MCP
client does not register native plugin skills, agents, or lifecycle hooks in
its UI.
