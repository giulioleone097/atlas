# Claude native exporter

Creates separate, self-contained Claude ZIPs from tracked Atlas-family sources.
It keeps Claude manifests, skills, native agents/hooks, runtime code and needed
Atlas doctrine documents while excluding local state, caches, Git data,
credentials, `.mcp.json`, root host hooks, tests and evals.

```sh
python3 integrations/claude/export_native_plugins.py \
  --plugin atlas=/Users/giulioleone/Sviluppo/atlas \
  --plugin spotter=/Users/giulioleone/Sviluppo/spotter \
  --plugin llm-wiki-kit=/Users/giulioleone/Sviluppo/llm-wiki-kit \
  --out /path/to/claude-portability
```

The exporter resolves a symlinked source root, rejects symlinks among selected
files and unsafe archive names, never overwrites an output, and verifies each
ZIP by byte-for-byte read-back. Each package adds `references/claude-host.md`
and a skill-local instruction to read it. Source versions stay unchanged; the
generated host reference records the adaptation.

Upload each ZIP under Claude Settings → Plugins → Add → Upload plugin, then
enable it. Chat uses the packaged skills; native hooks and subagents require
a supporting host such as Cowork. The host reference makes core instructions
available even when session hooks do not run.

Cowork and Claude Code cloud should download account-enabled plugins into
`~/.claude/plugins/synced/`. Start a new session and verify actual manifests
and `claude plugin list` there; an enabled account entry alone does not prove
delivery to that environment. This synchronization does not install plugins
in local terminal sessions. Uploading a package also does not configure a
durable personal wiki store.

Official references: [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
and [Plugins synced from claude.ai](https://code.claude.com/docs/en/plugins-reference#plugins-synced-from-claudeai).
