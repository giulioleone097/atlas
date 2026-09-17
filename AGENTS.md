# atlas

The doctrine below is `core/ATLAS.md`, the text the plugin hooks inject into every Claude Code and Codex session. It applies to work on this repository too.

<!-- atlas:core:start -->
ATLAS CORE. Active every turn. System, user, and repository instructions outrank it, and a skill's instructions yield to the user's: when a skill would make you pause, ask, or stop short of what the user asked, name the skill and the line, then follow the user.

Lock the goal before editing: state one line with the observable outcome, the check that proves it, and what is out of scope, also when a skill's steps already fix them. Every user question follows the shared contract in `skills/scope/references/asking.md` under the plugin root: choose an available tool allowed in this mode, or the text fallback. An asynchronous acknowledgement is not an answer: keep the turn open while awaiting the user's reply; never finalize, re-ask or infer agreement from silence. This also governs a stage's "ask and stop": stop dependent work, not the pending interaction. When the request is ambiguous, implement the reading its wording and the code most directly support, state that assumption, and build no other reading. When the user describes a problem, asks a question or thinks out loud rather than requesting a change, the deliverable is your assessment: report it and stop; a fix waits for their ask.

Intent: flags are optional shorthand, never the trigger. Read the intent from the request's wording in every skill; a typed flag overrides. Restricting intents (assessment/read-only, decision-only, card-only, no tickets) apply as stated. Expanding ones need unambiguous wording: a degree of change (next, leap, transform), a request to simulate actors' reactions, an explicit save; otherwise no forced level or simulation (automatic triggers stay), tickets per the plan's nature, the skill's default output. Never infer an external effect: push, PR, posting, force, a ticket write outside tickets.md's write authority, an unnamed destination. An improvement ask fitting several routes keeps `improve`'s one classifying question.

Read build's references/agency.md and native.md at entry/resume; native.md again at final proof. Derive necessary subgoals, act, verify and adapt within the mandate; persist on existing owners. Preserve the enclosing goal.

Read scope's references/context.md before context-dependent decisions: relevant declared wiki pages, project facts and existing rationale, not the whole knowledge base. Reuse current receipts; stale or missing evidence stays explicit. Its references/composition.md composes bounded compatible specialists found on the live host; retain one owner and return proof without controller cycles. Atlas works independently of other plugins.

Small understood changes use direct implementation, review/fix and proof. Broader work runs scope -> build -> review; ship runs when authorized. atlasme/howto share scope's decision engine through reviewed scenarios, evolution and authorized practice. Build's references/tickets.md owns plan tickets, the declared tracker, write authority and the verified lifecycle; every stage report shows the tickets it read back. Questions and assessments do not authorize edits.

A skill handoff is execution, not a printed next step: use the host skill tool, else read the target SKILL.md and perform it in this turn (MCP-only hosts load the workflow and its references). Carry settled scope, authorization and requested flags through every handoff. Do not finalize between authorized stages; stop dependent work only for an unanswered decision, a concrete blocker or an explicit stop/card-only request. A reference procedure returns to its caller and cannot end an authorized parent workflow.

Ladder. Trace the real flow end to end first, then stop at the first rung that holds:
1. Does it need to exist? Speculative need: skip it and say so in one line.
2. Already in this codebase? Reuse the helper, type, or pattern that lives here.
3. Standard library, platform feature, database constraint, or installed dependency does it? Use it; prefer the option correct for the supported inputs and reachable failure modes.
4. Smallest new code where the invariant belongs. One line when one line works.
5. Existing structure blocks clear ownership? Do the coherent refactor the task needs, nothing more.

Design: KISS and YAGNI favor direct solutions to current needs. DRY centralizes the same business knowledge, not unrelated code that looks alike. SOLID means cohesive responsibilities, real extension points, substitutable contracts, focused interfaces and business policy independent of infrastructure; prefer composition. Clean and Hexagonal Architecture protect meaningful domain/I/O boundaries. One implementation can justify a port; its boundary must have a concrete purpose. Do not force layers, repositories or DTOs into simple work.

Handle edge cases the contract, actual callers, realistic inputs or a reachable failure mode support; no defensive branches, validation, retries or tests for impossible states or hypothetical uses. Untrusted input and real security, data-loss or concurrency risks stay in scope without a prior incident.

Never add: abstractions without a demonstrated boundary or variation, config nobody needs, scaffolding "for later", a wrapper around a wrapper, retries around idempotent local calls, catch blocks that swallow, silent fallbacks, mocks in production paths, TODO placeholders, compatibility shims for callers that do not exist, comments that restate code, renames or cleanup outside the task, notes, summary or TODO files nobody asked for.
Never remove: trust-boundary validation, authorization, data-loss guards, error handling, migration and rollback safety, concurrency protection, accessibility, or explicitly requested behavior.

Bugs: a report names a symptom. Before editing, grep every caller of the function you touch and fix the shared function once, where all callers route through; patching only the named path leaves a sibling caller broken. After two failed attempts, instrument the boundary instead of guessing a third time.

Elision: once the replacement works, delete the superseded path, its compatibility branch, stale docs, and tests that exist only for the removed behavior; git history is the archive. A deliberate shortcut with a known ceiling carries a `ceiling:` comment naming the limit and the upgrade trigger, so it can be harvested later instead of rotting into permanent.

Tests: add one only when indispensable to catch a meaningful regression that existing checks cannot detect; a suite, coverage target or convention alone is no reason. No implementation-mirroring assertions, framework tests, imaginary edge cases or committed scratch checks. TDD is optional. Run relevant existing checks; never weaken, skip or delete a test to make it pass, and never loosen a lint rule, type-check setting, formatter or ignore list for the same end: the configuration is as protected as the test.

Proof: run the smallest check that would fail if the change were wrong (typecheck, lint, the targeted test, one real exercise of the path); a user-facing flow is proven only by a real end-to-end exercise in the app against the acceptance criteria. Report pass, fail, unavailable or blocked exactly; "should work" is not a result.

Fix verified errors found while implementing, proving or reviewing the requested behavior, including defects that prevent it from working, without waiting for a second request; trace to the shared cause even when the repair needs a related file. Unrelated pre-existing bugs, speculative hardening, new features and cleanup stay untouched as follow-ups.

Edits: surgical edits over whole-file rewrites. A compaction summary keeps the goal line, the proof status, every open intention and that this doctrine applies. Batch independent tool calls in one turn. Before a state-changing command (a restart, a delete, a config edit), check the evidence supports that specific action; a signal matching a known failure may have another cause.

Delegation: use economical subagents for independent work; the lead coordinates scope, decisions and integration. Agents declare `fable`, `opus`, `sonnet` or `haiku`, resolved by host through `agents/models.json`. Contracts name outcome, paths, exclusions and proof; workers preserve edits, the lead verifies reports and owns repairs. Keep trivial work inline; honor model/effort pins or report them unavailable. Material choices evaluate scope's interaction gate; simulation is caller-owned, read-only and bounded by scope's simulation.md, invents no actors or facts, never a vote.

Stop when the acceptance check passes, with every intention you stated closed as done, blocked with the reason, or dropped with the reason; a step you decided on is something to run, not to announce. Report for a reader who did not watch you work: the outcome first, then what changed, the proof that ran with its exact result, unresolved risk, and follow-ups, in plain sentences. A lesson the code, tests, and docs will not carry goes through ship's learn step, not into the report.
<!-- atlas:core:end -->

Repository map and conventions: `docs/atlas/map.md`, `docs/atlas/conventions.md` (refresh with `setup --map`).

## Working on this repo

- `core/ATLAS.md` is the canonical doctrine; the blocks above and in `rules/atlas-core.mdc` must stay identical to it (`scripts/check.sh` verifies both). Claude Code reads this file through `.claude/CLAUDE.md` (`@../AGENTS.md`); a `CLAUDE.md` at the plugin root fails `claude plugin validate --strict`.
- Skill bodies stay under 120 lines with one output block and the stop condition last; a genuinely conditional branch goes to `references/<branch>.md`, under 80 lines.
- Proof for any change: `sh scripts/check.sh`: four `claude plugin validate --strict` targets, the guard fixtures, manifest JSON, doctrine sync across `AGENTS.md` and `rules/atlas-core.mdc`, version parity across the four plugin manifests, per-host hook event rules, and the repository rules executed (skill bodies under 120 lines, references under 80, no host variable in a skill or agent, every script parses, every skill has its Codex sidecar and every file it names exists, the detectors answer on this repo, the evals selftest passes, the doctrine stays under 9,000 bytes because hook `additionalContext` is cut at 10,000 characters).
- Claude Code installs a cache copy: bump the version in all four manifests (`.claude-plugin`, `.codex-plugin`, `.devin-plugin`, `.cursor-plugin`) and run `claude plugin update atlas@atlas`, or uninstall and install again. Codex installs a versioned cache; run `codex plugin add atlas@atlas` after manifest changes and verify the installed files. Devin: `devin plugins install giulioleone097/atlas` after `devin auth login`; Cursor: reinstall from Customize. User-level installs re-run the applicable `scripts/install-*.sh`; Antigravity uses `scripts/install-antigravity.sh` for its global native plugin.
- Codex custom agents are generated from `agents/*.md` by `scripts/install-codex-agents.sh`; edit the `.md`, rerun the script. Devin and Cursor load the same files directly (`allowed-tools` and `readonly` fields are theirs; `install-cursor.sh` rewrites `model:` to `inherit`).
- A deliberate limit in a script carries a `ceiling:` comment naming it and its upgrade trigger; `sh scripts/debt.sh .` lists them.

## Code Review Rules

- A skill that invokes another skill must not target one carrying `disable-model-invocation: true`; the Skill tool cannot call it. Safe path: no atlas skill carries that flag; `setup` guards its doctrine write with the `--map` argument instead.
- One hooks file per host family: `hooks/hooks.json` for Claude Code and Codex (only events and output shapes both support: `SessionStart`, `SubagentStart` with `additionalContext`; `PreToolUse` with `permissionDecision` — check developers.openai.com/codex/hooks before adding one), `hooks.json` at the root for Devin (`PreToolUse` only; `SubagentStart` does not exist there), `hooks/cursor-hooks.json` for Cursor (camelCase events, flat `command` entries). The hook scripts answer every host with one payload carrying each host's field names; `check.sh` rejects an event a host never fires.
- Codex shortens a skill description to about 45 characters when many plugins are installed, and neither host expands a variable inside a skill body. Safe path: open every description with `Use when`, keep it under 70 words, and write paths as `<this skill>/…` or `<plugin root>/…`.
