# ChatGPT native-skill exports

`export_native_skills.py` produces independent upload bundles from the canonical
Atlas and Spotter repositories. Add `--plugin NAME=PATH` for another manifest-backed
plugin; for example, Jobs Engine Seeker:

```sh
python3 integrations/chatgpt/export_native_skills.py \
  --atlas-root /path/to/atlas \
  --spotter-root /path/to/spotter \
  --output /path/to/chatgpt-skills
```

```sh
python3 integrations/chatgpt/export_native_skills.py \
  --atlas-root /path/to/atlas \
  --spotter-root /path/to/spotter \
  --plugin jobs-engine-seeker=/path/to/jobs-engine-seeker \
  --output /path/to/chatgpt-skills
```

The output folder contains `atlas.zip`, `spotter.zip`, and one ZIP for each optional
plugin. Each archive has one native
`SKILL.md`, its canonical core, the maintained procedures and their referenced
documents. UI metadata and the source version come from the plugin manifest; skill
descriptions come from the maintained entries, so exports do not carry a second
Atlas/Spotter catalog. The Jobs Engine Seeker archive derives its UI metadata from its Codex
manifest and carries only the public fixture-engineering runtime closure; it excludes
operational workspaces, ledgers, reports, CVs, environment files, and credentials. The
Spotter archive also carries the minimal standard-library Wiki runtime
and its MIT attribution when its exported `scripts/wiki.sh` needs them. Procedures are
named `PROCEDURE.md` inside `references/package/` so an upload contains exactly one
skill entrypoint.

Directory and ZIP are prepared for separate upload in ChatGPT's Skills interface.
Verify that the account supports the upload, then complete the scan and installation
in the UI; generation alone does not prove that either skill is installed. See
[ChatGPT skills help](https://help.openai.com/en/articles/20001066). Native skills do
not create MCP listings, install agents or hooks, provide local execution, activate
schedules, or connect tracker and source accounts. The separate Atlas and Spotter
tunnel runtimes provide their own MCP listings and capabilities.

Full managed-plugin grouping is a workspace marketplace feature and needs a supported
workspace import flow; see [plugin management](https://developers.openai.com/codex/enterprise/plugin-management).

Rebuild after changes to either source repository, then validate the exported shape:

```sh
python3 integrations/chatgpt/export_native_skills.py \
  --atlas-root /path/to/atlas --spotter-root /path/to/spotter \
  --plugin jobs-engine-seeker=/path/to/jobs-engine-seeker \
  --output /path/to/chatgpt-skills --check
python3 <skill-creator>/scripts/quick_validate.py /path/to/chatgpt-skills/atlas
python3 <skill-creator>/scripts/quick_validate.py /path/to/chatgpt-skills/spotter
python3 <skill-creator>/scripts/quick_validate.py /path/to/chatgpt-skills/jobs-engine-seeker
```
