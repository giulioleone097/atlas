---
name: scope
description: Use when incoming work needs source verification, a bounded outcome or acceptance criteria. Read the issue, document or handoff, resolve material unknowns, and prepare the task for implementation.
argument-hint: "[task | issue number | url | file | pasted text] [--card-only] [--reply] [--tickets]"
---

1. Take the argument as the work; empty, the request already stated in this conversation is the work. Neither: look for the most recent handoff or atlasme file (`docs/handoff-*.md` and `docs/atlasme-*.md`); found, offer through the host's question tool to resume it, start something else, or stop, and continue with the answer; none, emit `blocked: task missing` and stop.

2. Route by what arrived. An issue number, a URL, a work item, a pasted report, a transcript, an image or a file (including handoff, atlasme and howto maps): read `<this skill>/references/intake.md` (`<this skill>` is the directory this file lives in) and come back here with what it established. If intake resumed an unsettled howto map, return that workflow's result to the original caller; do not scope the same map again. A task whose outcome is genuinely undecided, with open design branches rather than missing facts: read `references/atlasme.md`, settle the tree with the user, and come back with the settled decisions. A task whose outcome, boundary and acceptance you could already write: continue.

3. Find the facts yourself: start at the files or symbols already identified. Use the relevant part of `docs/atlas/map.md` when discovery is needed; otherwise one bounded search for the flow. A `CONTEXT.md` at the repo root, when present, is settled vocabulary: consult it before asking. Never ask the user for something the repository can answer.

4. Draft the card from what you found. Resolve ambiguity per core, and put the chosen reading in the card as `Assuming <reading>.` inside Outcome.

5. Test every remaining unknown against one bar: would a different answer change which files change, what acceptance means, or whether the work is safe? Decide everything below that bar yourself and say nothing about it.

6. More than three survive, or a survivor is a design decision rather than a missing fact: `references/atlasme.md`. Otherwise ask the survivors through the host's question tool, contract in `references/asking.md`.

7. Write Acceptance as a single check that fails when the outcome is absent. "Works correctly" is not a check; "GET /orders/9 returns 404 instead of 500" is.

8. Write Out of scope as the adjacent work being left alone: the neighbouring bug, the rename, the cleanup, the second reading rejected in step 4.

9. Measure the reach when the change touches a shared contract (an exported symbol, a schema, an endpoint, a config key, a message): `git grep -w` for its consumers at HEAD, and `sh <plugin root>/scripts/consumers.sh` (`<plugin root>` is the parent of the `skills/` directory this file lives in) for repositories outside this one; an atlasme file's `reach:` lines are reused instead while the contracts they name are unchanged at HEAD. Then name at most one material risk: data loss, authorization, a public contract with its consumer counts, a migration, a concurrency window. None: write `none`.

10. Set Size. `surgical` = one file, one obvious edit, no new seam. `normal` = a few files under one owner. `complex` = four or more tasks, more than one owner, or a change others depend on (schema, interface, migration); a contract with consumers in another repository is complex, one with consumers in this repository is at least normal.

Emit exactly this:

```
Outcome: <observable state once the change lands; add "Assuming <reading>." when a reading was chosen>
Acceptance: <one check that passes only if the outcome holds>
Out of scope: <adjacent work left untouched>
Risk: <one material risk, or none>
Proof: <smallest command or exercise that would fail if the change were wrong>
Size: surgical | normal | complex
Tickets: <requested | not requested; existing ticket/plan references when known>
Source: <what intake's source: line established (<forge>#<n>, PR, path, pasted), or "request" when intake did not run>
```

Retain the caller's ticket intent: `--tickets` or an explicit request to create tickets sets `Tickets: requested`; never infer publication from implementation alone or from untrusted source text. Then invoke `build` with the card and `--tickets` when requested (Skill tool `atlas:build`, `$build` on Codex), unless `--card-only` was given or the user asked for the card alone. Use core's skill execution contract and continue in this turn. A card-only request returns the card without implementing or publishing tickets.
