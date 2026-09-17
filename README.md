# atlas

<img src="assets/icon.png" alt="Atlas icon" width="128" />

One plugin for the whole development loop, for Claude Code, Codex, Devin and
Cursor, with a native skills-and-rules adapter for Antigravity. Lock the
outcome, take the shortest safe path, prove only changed behavior, stop. Five
stages carry setup through ship, nine entry points are typed by name (atlasme,
simplify, handoff, optimize, intel, question, howto, prototype, improve);
four agents cover locating, bounded implementation, review, and integration.

## Install

### Claude Code

From a local checkout:

```
/plugin marketplace add /path/to/atlas
/plugin install atlas@atlas
```

From GitHub:

```
/plugin marketplace add giulioleone097/atlas
/plugin install atlas@atlas
```

### Codex

```
codex plugin marketplace add giulioleone097/atlas   # or the local checkout path
codex plugin add atlas@atlas
```

Then run `codex`, open `/hooks`, trust the three plugin hooks (SessionStart,
SubagentStart, PreToolUse), and start a new thread.

```
sh /path/to/atlas/scripts/install-codex-agents.sh
```

Generates `atlas_scout`, `atlas_worker`, `atlas_reviewer`, and
`atlas_integrator` as Codex custom
agents from `agents/*.md`. Restart Codex after running it.

### Devin

```
devin plugins install giulioleone097/atlas   # or the local checkout path
```

Skills answer to `/atlas:<stage>`; the doctrine rides the plugin's always-on
`AGENTS.md` and the guard runs on `PreToolUse` via the root `hooks.json`. Where
the plugin manager is unavailable (`devin auth login` required), install at
user level instead:

```
sh /path/to/atlas/scripts/install-devin.sh     # --remove reverts
```

### Cursor

Install from **Customize → Plugins** pointing at `giulioleone097/atlas` (or a
local checkout). The `.cursor-plugin/plugin.json` manifest wires skills,
`rules/atlas-core.mdc` (the doctrine, `alwaysApply`), agents and
`hooks/cursor-hooks.json` (`beforeShellExecution` → the guard). At user level:

```
sh /path/to/atlas/scripts/install-cursor.sh    # --remove reverts
```

### ChatGPT and other MCP clients

The [native-skill exporter](integrations/chatgpt/README.md) prepares separate
Atlas and Spotter skill bundles, each with its doctrine and internal procedures.
Upload and installation depend on the ChatGPT account's Skills support.

The optional [workflow MCP bridge](integrations/mcp/README.md) serves one plugin
per process. Connect Atlas and Spotter through separate Secure MCP Tunnels and
custom apps. MCP tools do not install native skills; hooks, automatic per-turn
instructions and local execution still require host support.

### Checks

`sh scripts/check.sh` — the one-command acceptance run (validates, guard
fixtures, manifest JSON, doctrine sync, four-manifest version parity, per-host
hook event rules).

## The flow

```
atlasme ──► howto ─┐
setup? ────────────► scope ──► build ──► review ──► ship
             │          │          │
       intake, atlasme  plan, debug  shrink, reviewers,
       goal card      prove        integrator
                              simplify (shrink alone)

optimize ──► review           rounds of hypotheses toward a target
handoff  ──► scope <file>     stop early now, resume in the next session
```

The loop chooses its path: a small understood change uses direct implement,
review, fix and prove; broader or uncertain work goes through `scope`, `build`
and `review`, with each stage invoking the next through the host's skill tool.
`ship` runs when you say ship, commit or PR, or when the request said to carry
the work through. `setup` installs the doctrine in a project and builds its
map; the map is refreshed by the model when its stamp is behind facts needed for
the task. Type a
stage name only to run one alone or with flags.
`atlasme`, `simplify`, `handoff` and `optimize` can be selected automatically or invoked by name:
an idea explored through scenarios and a reviewed choice, a shrink pass on code nobody asked
to review, a session written down for the next one (which resumes it through
`scope <file>`), and a measured number pushed toward a target by rounds of
parallel hypotheses that keep only what beats the baseline.

## Skills

| Skill | Use when | Result |
|---|---|---|
| `atlasme` | an idea needs brainstorming before choosing an approach | Compare approaches and scenarios, review the choice, carry authorized work into howto |
| `build` | implementing a feature, fixing a bug, refactoring or migrating code | Implement, fix and verify the requested code change |
| `handoff` | unfinished work must continue in another session | Save unfinished work for a reliable next session |
| `howto` | brainstorming must become a practical, verifiable outcome | Compare scenarios, review choices, execute authorized steps and adapt from evidence |
| `improve` | assessing codebase structure or choosing a broader improvement | Assess codebase structure and choose an improvement |
| `intel` | a research question needs evidence from official documentation, specifications, source code or first-party APIs | Research a question and produce a cited evidence brief |
| `optimize` | improving a measurable performance, resource or quality metric | Improve a measured metric while preserving guard limits |
| `prototype` | a design decision needs an interactive experiment | Test a design with disposable logic or UI prototypes |
| `question` | a decision depends on information another person holds | Prepare a questionnaire for someone holding missing facts |
| `review` | reviewing a code change, auditing a repository or addressing PR feedback | Review code, repair scoped defects and verify the result |
| `scope` | incoming work needs source verification, a bounded outcome or acceptance criteria | Verify incoming work and define its outcome and proof |
| `setup` | explicit installation/removal of project instructions, or discovery via `setup --map` | Configure Atlas project rules or refresh its repository map |
| `ship` | committing verified work, pushing changes, opening a PR or preparing its description | Deliver verified changes or prepare a PR description |
| `simplify` | simplifying code while preserving its behavior, or requesting a complexity, debt or rules audit | Simplify scoped code while preserving its behavior |

Atlas selects routes and technical options from the outcome, repository evidence and available resources; flags override those selections. `atlasme`, `howto` and `scope` retain choices and evidence through handoffs. Missing technical flags never require configuration questions. Atlas recommends KPIs and asks only for unsettled priorities, user values or authority through the permitted native question tool. Evolution starts at the smallest useful level and expands when evidence rules out the current approach; `--evolve [next|leap|transform]` overrides that selection. Explicit read-only, scope, model and resource limits remain binding.

Available specialist skills can supply bounded context or work through `skills/scope/references/composition.md`. Atlas owns software proof; a Spotter parent owns life priorities and personal knowledge. Neither plugin is required by the other. A visited owner/capability chain prevents mutual controller loops; relevant evidence returns to the same map.

Build owns an adaptive agency cycle: recover the user's mandate, derive necessary technical subgoals, choose available tools or specialists, act, verify the actual result and revise the next feasible actions. The same issue/plan retains scope, authority, proof and continuation. Independent authorized work continues around blockers; completion requires the enclosing acceptance and requested delivery. Native goals/triggers supply continuity only when available and explicitly activated; ordinary work needs no substitute goal or new runtime.

After `atlasme` settles an authorized implementation request, Atlas executes `howto` → `scope` → `build` → `review` in the same turn. An operational plan materializes missing outcome tickets before execution, reuses existing IDs, records priority/dependencies and maintains status/proof through delivery. `--tickets` also requests this for a small change; it is no longer required after an operational plan. A repository declares its tracker in one line, `atlas: tracker=<name> [project=<container>]`, in its own or an ancestor's AGENTS.md or CLAUDE.md, which `scripts/tracker.sh` reports as `declared=`; precedence runs explicit native owner, declared tracker, detected forge with an authenticated CLI, then authorized local files under `docs/tickets/`. Selecting a store is not write authority, and every stage report shows the `tickets:` line it read back. An unavailable declared remote remains an explicit blocked write, never a silent fallback. Every record and relation needs read-back. Matching GitHub, GitLab, Linear, Jira and Azure issues are the tickets themselves: refresh their current fields on entry, resume and authorized check-ins, write only authorized changes, then read back. Existing plans keep links and dated projections; remote conflicts or failed writes remain pending instead of overwriting team changes. Card-only, assessment-only and explicitly disabled tracking retain their boundaries.

Use `howto <objective>` for brainstorming through practice: define outcome and proof, compare materially different approaches under the same plausible conditions, review the choice, execute authorized steps, then compare real results with forecasts. Every material choice evaluates the interaction gate; it triggers automatically only for distinct supplied actors/subsystems whose grounded plausible reactions could change the choice, while `--simulate` explicitly requests that gate without inventing actors or facts. The caller alone coordinates native read-only actors from supplied state, with exact barriers, a root-shared three-wave budget through depth two, and one final nonparticipating reviewer. Actor output is hypothesis, never a future fact, KPI or probability; unavailable native delegation yields an explicit analytical comparison and missing evidence/value yields the smallest real checkpoint/question. It resolves what is ready without a one-decision-per-session limit. `howto <map>` validates and resumes saved simulation state without replaying completed rounds; a snapshot never proves a live agent session. `--decision-only` keeps the result at the map; `--card-only --tickets` retains ticket intent on a card for later work; implementation plus `--tickets` continues through scope and build. Explicit read-only mode returns an unsaved map. Decisions and checkpoints link existing issues; the map is not another backlog. Use `atlasme` to explore one idea and `scope` when the work is already defined.

The shared decision engine belongs to scope (`atlasme.md`, `scenarios.md` and internal `simulation.md`); howto calls it directly, so public skills cannot bounce back and repeat the same brainstorming. No simulator runtime, dependency, public mega-skill, council log or duplicate issue backlog is required.

When a decision requires an experiment, `howto` runs the smallest ready checkpoint within existing authority: `optimize` for measurable alternatives and combinations, otherwise `scope`. Optimize recommends KPI presets from context, explains its preferred metric and offers relevant alternatives through native questions when the priority is unspecified. Explicit KPI choices are reused; commands, scope and bounded options are selected autonomously; each candidate has its own Git worktree and equivalent inputs. Coordinator measurements are serial, compare with a fresh champion control and reject noise, changed workloads or broken guards. Promising improvements are combined and remeasured, including reconciled edits to the same file, within one root budget. The ledger records lineage, candidate outcomes and untested options. Dirty input can be snapshotted without touching the user's index; recovery state survives until checked integration and review pass. A checkpoint never completes the parent goal; map-only/read-only requests keep it as a proposed step.

Every stage keeps its branches in `references/`: the root file is a router, read in full, and a branch is read only when its case applies.

## Agents

Role definitions live in `agents/`; `agents/models.json` owns model mappings for each host.

- `atlas-scout` — read-only.
  Locates code; returns `path:line` references or `No match.`. Never suggests
  fixes.
- `atlas-worker` — implements one owned, disjoint
  slice under an explicit contract; reports changed files, proof, blockers,
  follow-ups.
- `atlas-reviewer` — read-only.
  In `mode: decision` or `mode: simulation-review`, challenges a brief and scenarios before implementation; `mode: simulation-actor` is a supplied-material-only constrained native actor.
  Otherwise reviews one lens (`correctness`, `slop`, `safety`, or `all`) against a baseline diff;
  reports every finding with a confidence score, never fixes anything itself.
- `atlas-integrator` — read-only.
  Merges reports when several areas need integration, settles contradictions by
  reading the code, catches cross-area defects, and runs the nearest checks with
  every failure attributed to the baseline before it is called new. There is no
  minimum reviewer team; Astra/Fable coordinate scope, decisions, and integration.

## Scripts

Seven read-only helpers let the skills use the repository's own commands instead of guessing. Each reads repository facts or diffs and returns structured or line-oriented output; every skill that needs one names it.

| Script | Answers | Used by |
|---|---|---|
| `scripts/checks.sh <path>` | the project's own typecheck, lint, test, build and e2e commands for that path or file (nx targets, package scripts, Playwright and Cypress configs, pyproject, .NET, cargo, go, make), or `none=1` | `build` (prove), `review`, `optimize`, `ship` (evidence), the integrator |
| `scripts/tracker.sh [repo]` | the repository's `atlas: tracker=` declaration from the nearest AGENTS.md/CLAUDE.md (`declared=`, `project=`), then the forge, the CLI and whether it is logged in, from the origin remote (GitHub/gh, GitLab/glab, Azure DevOps/az; any other host is probed through gh then glab, so an enterprise GitHub or self-hosted GitLab the CLI is logged into is found; else files under `docs/tickets/`) | `scope` (intake), `build` (plan), `ship` |
| `scripts/tokens.sh <ui path>` | the design tokens the repository already defines, with counts: custom properties, colours, fonts, sizes, theme keys | `build` on UI work, the reviewer's `taste:` tag |
| `scripts/consumers.sh [repo]` | what depends on this repository outside its tree: the names it publishes (package, module, crate, assembly, remote) and every sibling checkout or workspace member whose manifest names one of them | `review`, `ship` (dossier), the integrator's cross-repo sweep |
| `scripts/repo-facts.sh [repo] [months] [prs]` | the facts a map starts from, read-only: layout, languages, hot spots, authors, commit conventions, checks, instruction files, and through `gh` the merged-PR cadence, reviewers and inline commenters (bots kept apart) | `setup` (map) |
| `scripts/debt.sh [repo]` | the ledger of declared shortcuts: every `ceiling:` comment with its limit and upgrade trigger, `no-trigger` on the ones that will rot | `review --debt`, `setup` (map) |
| `scripts/pr-partition.py BASE HEAD` | the diff split into judgment, tests, mechanical, generated, docs and config, so only judgment code is read | `review`, `ship` (dossier) |

`scripts/check.sh` is the plugin's own acceptance: four strict validations, the guard fixtures, manifest parity, doctrine sync, per-host hook event rules, and the repository rules executed (skill bodies under 120 lines, references under 80, no host env var inside a skill, every script parses, tracker, checks and debt detectors answer on this repo).

## Hooks

One hooks file per host family — the events and the output shape differ, so
they do not share a file. All scripts are POSIX `sh` + `python3 -c` (no node,
no jq):

- `hooks/hooks.json` — Claude Code and Codex. `SessionStart` and
  `SubagentStart` run `scripts/core-context.sh`, which injects
  `core/ATLAS.md` as `additionalContext` so the doctrine is active
  every turn and inside every subagent. `SubagentStart` has no matcher, so it
  injects into every subagent in the session, not only atlas's; set
  `ATLAS_SUBAGENT_MATCHER=<regex>` (unanchored, case-insensitive, for
  example `^atlas`) to narrow it to the agent types that match; the pre-rename
  `SNIPER_SUBAGENT_MATCHER` is still honored as fallback.
  `PreToolUse` on `Bash` runs `scripts/guard.sh`.
- `hooks.json` (plugin root) — Devin. `PreToolUse` on `exec` /
  `write_to_process` runs the guard; the doctrine rides the plugin's always-on
  `AGENTS.md` rule instead of a session hook.
- `hooks/cursor-hooks.json` — Cursor. `beforeShellExecution` runs the guard;
  the doctrine rides `rules/atlas-core.mdc` (`alwaysApply`).

The guard and the context script answer every host with one payload — each
host reads the fields it knows (`permissionDecision` for Claude/Codex,
`decision`/`reason` for Devin, `permission`/`user_message` and
`additional_context` for Cursor) — and both read the command from whichever
field the host sends (`tool_input.command`, `text_input`/`bytes_input`, or
top-level `command`). The guard denies:
  - `--no-verify` as a token in a segment that also has `git`
  - `git push --force` / `-f` / a `+refspec` (e.g. `+main`), but not
    `--force-with-lease`
  - `git reset --hard`
  - `git checkout ... .` in any form (`checkout .`, `checkout -- .`,
    `checkout HEAD -- .`, `checkout -f .`)
  - `git restore ... .` in any form, unless it is staged-only
    (`--staged`/`-S` without `--worktree`/`-W`)
  - `git clean -f*` (any flag combination containing `f`)
  - `rm -rf` / `-fr` / `-r -f` targeting `/`, `~`, `$HOME`, `${HOME}`, `.`,
    `..`, or `*` (with or without a trailing `/` or `/*`)

  Everything else is allowed, including `rm -rf node_modules`,
  `rm -rf dist`, and `git push --force-with-lease`. Any parse or script error
  prints nothing and allows the command — the guard never traps the user.

To disable: `/plugin disable atlas` (Claude), `codex plugin remove atlas`
(Codex), `devin plugins remove atlas` (Devin), or remove the host's entry in
its hooks file.

## Codex notes

- Skills: same files, invoked as `$name` instead of `/atlas:name`.
- Hooks: same `hooks/hooks.json`; trust it once in `/hooks` (see Install).
- Agents: not bundled — `scripts/install-codex-agents.sh` generates
  `atlas_scout`, `atlas_worker`, `atlas_reviewer`, `atlas_integrator`
  (hyphens become underscores) as `~/.codex/agents/*.toml`; `build`,
  `review`, `optimize`, `ship` and `setup` spawn them when installed,
  otherwise fall back to inline/sequential.
- No `disable-model-invocation` anywhere: every stage is model-invocable so
  the loop can chain; `setup` guards its doctrine write with the `--map`
  argument the model passes when it only refreshes the map.

Per project, run `/atlas:setup` (`$setup` on Codex): it writes the doctrine
block into the repository's `AGENTS.md` (created, or appended between
`<!-- atlas:core:start -->` / `<!-- atlas:core:end -->` markers, nothing else
touched) and makes `CLAUDE.md` import it with `@AGENTS.md` (or `.claude/CLAUDE.md`
when the project keeps it there). Claude Code and Codex load global and project
instructions together; the project file is the more specific one, and when the
block is present the hook injects nothing at either event, so the doctrine costs
its tokens once. Teammates without the plugin get the same rules from the file.
Re-run after a core update; the block is replaced, your sections stay.

- Codex substitutes `${CLAUDE_PLUGIN_ROOT}` in `hooks/hooks.json` only. Inside a skill body neither host expands a variable, and Codex presents skills to the model as absolute skill roots, so every path in a skill is written relative to the file that names it (`<this skill>/scripts/…`, `<plugin root>/scripts/…`); `scripts/check.sh` fails on any `CLAUDE_SKILL_DIR` or `${CLAUDE_PLUGIN_ROOT}` inside a skill or agent.

## Devin and Cursor notes

- Devin reads the plugin's `AGENTS.md` as an always-on rule (the doctrine),
  `agents/*.md` as custom subagents (it uses the `allowed-tools` field, and
  `atlas:`-prefixed profile names), and the root `hooks.json` — its only
  plugin hooks convention. There is no `SubagentStart` on Devin, so subagents
  there rely on their own prompts.
- Cursor reads `.cursor-plugin/plugin.json`; `rules/atlas-core.mdc` carries
  the doctrine with `alwaysApply` (its body must stay identical to
  `core/ATLAS.md` — `check.sh` verifies). Agent frontmatter `readonly: true`
  keeps scout/reviewer/integrator read-only; `model:` pins are
  Claude/Devin names — on Cursor the installers rewrite them to `inherit`,
  and the plugin bundle leaves them for the model picker to resolve.
- Both installers (`install-devin.sh`, `install-cursor.sh`) exist because the
  plugin managers are not always reachable; they copy skills as `atlas-<stage>`
  (rewriting `atlas:` references to `atlas-`), merge hook entries without
  touching others, and are idempotent and reversible (`--remove`).

## Evals

`evals/` measures the plugin with real headless sessions per cell, bare, using
baseline, current, and optional previous-plugin arms, scored on the files left
behind by deterministic scorers that prove themselves on good and bad
references first (`python3 evals/run.py --selftest`, also run by
`scripts/check.sh`). Five probes cover path safety, canonical root causes,
per-client limits, bounded fixes, and meaningful domain/I/O boundaries. See
`evals/README.md`; missing or partial live metrics remain explicitly unavailable.

## Sources

See [`docs/sources.md`](docs/sources.md) for what was taken from where, with
star counts and rejected alternatives.

## License

MIT — see [`LICENSE`](LICENSE).

## Antigravity

Run `sh scripts/install-antigravity.sh` for a global native plugin at `~/.gemini/config/plugins/atlas`. It includes skills, their references/helpers and the canonical doctrine as a plugin rule. Re-run after updating Atlas; open a new session to load it. This adapter does not register hooks or custom agents; use the host capabilities actually available. The directory follows [Antigravity plugin documentation](https://www.antigravity.google/docs/plugins).

## Native goals and loops

Atlas binds work to an existing native goal and uses supported host continuation rather than a custom runner. An explicit goal request can activate the native primitive when the session permits it; ordinary work still completes without creating a goal. Request timed/event work through `setup --schedule <request>` or natural language. Goal execution and recurring triggers are separate: no schedules activate on installation.

[Native lifecycle](skills/build/references/native.md) documents Codex goals/heartbeats, Claude Code goals/cron, Cursor goals/loops/Automations, Antigravity goals/schedules and Devin Scheduled Sessions. Availability is checked per operation in the receiving session; workflow MCP and ChatGPT skill uploads do not register host primitives. Existing owner references, evidence-based completion and non-overlapping execution apply across skill handoffs and host changes.
