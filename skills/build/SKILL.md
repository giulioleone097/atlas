---
name: build
description: Use when implementing a feature, fixing a bug, refactoring or migrating code. Take the smallest correct path, investigate unknown causes, and complete scoped repairs, review and verification.
argument-hint: "[goal card | what to build | the failure] [overrides: --tickets --no-review]"
---

1. Take the goal card from `scope` or from the argument when one exists; otherwise lock the goal per core in one line, stating any chosen reading. An issue number, a URL, an image, a handoff or atlasme file is scope's input, not a card: invoke `scope` with it (Skill tool `atlas:scope`, `$scope` on Codex) and stop here; its intake reads the source, emits the card and invokes `build` with it.

2. Read `references/agency.md` when the mandate is not already bound; reuse a current receipt. A requested or active native goal/trigger uses `references/native.md` and its authorization rules; ordinary work needs no native lifecycle setup. Preserve ticket policy, selected tracker and write authority from the caller. An existing operational plan, `Size: complex`, several owners, a change others depend on, or `--tickets` runs `references/plan.md` before implementation, including its ticket persistence step. Reuse a plan already read, not another backlog. `--tickets` also requests tracking for a small change. Otherwise a small understood change uses core's short path with local review/fixes; an existing issue still follows `references/tickets.md` during execution. A failure with no known cause: read `<this skill>/references/debug.md` (`<this skill>` is the directory this file lives in). Load `references/fix.md`, `references/refactor.md` or `references/migrate.md` only for the applicable work, and `references/ui-taste.md` only when making visual design decisions.

3. Reuse relevant learned procedures through `<plugin root>/skills/scope/references/context.md`: check their trigger/preconditions against current facts and apply them to this slice, carrying an actual-use receipt. Locate only what is still unknown. Start at named files or the relevant map entry; a bounded search is normally enough. Use a `atlas-scout` (Codex: `atlas_scout`) when discovery is substantial and independent of useful work you can continue locally.

4. Cut the work into slices (the existing plan's tasks when present), each with outcome, owned paths, acceptance and its returned ticket reference. For tracked slices, execute the start/blocker/proof lifecycle in `references/tickets.md`; re-read dependencies and update the real record before starting ready work. Walk core's reuse ladder before writing new code. Derive necessary subgoals inside the mandate and select ready work through agency.md; discovered prerequisites can revise this same plan.

5. Follow core's test indispensability rule; TDD is optional. When a baseline failure is needed to prove a regression test distinguishes the defect, reproduce it in a disposable checkout without reverting the working tree. Take expected values from the contract or a worked example. Run relevant existing checks, and repeat only checks invalidated by a change or unresolved failure; do not ask for routine test-design approval.

6. Implement the local slice or a trivial edit inline; keep independently assignable work available for economical delegation in the next step.

7. Delegate independently assignable slices to `atlas-worker` subagents (Codex: `atlas_worker`) under core's delegation rule, adding the slice's acceptance check to each contract. Parallel writers need disjoint paths; use disposable worktrees when builds, generated files or tests would collide. Seed only needed tracked changes and explicitly selected new files, preserving the source index, unrelated edits and private files. Record that seeded baseline inside the worker checkout before edits; integrate only the worker's delta on owned paths against it, not the parent's existing changes. Install dependencies there only when required for proof, then remove the disposable checkout after integration. On a worker failure, change the inputs, scope or available capability before retrying. Unavailable optional delegation can fall back to local bounded work, disclosed as such; a required model or independent review stays blocked. Never retry an unchanged blocker or silently substitute an explicit model pin.

8. After each slice, compare actual results with expected observations through references/agency.md; update the same owner, adapt affected work and continue ready authorized actions. At the enclosing proof boundary, prove the acceptance check: run the proof command the card names exactly as written and capture its own exit status with the decisive output line (a trailing `| tail` reports tail's status, not the command's); when the card names none, `references/prove.md` chooses the check set.

9. Report:

```
<path> — <what changed>
proof: <command> — pass | fail | unavailable | reused
tickets: <references/tickets.md's line | none | unavailable: <gap>>
status: DONE | DONE_WITH_CONCERNS: <c> | BLOCKED: <b> | NEEDS_CONTEXT: <w>
follow-ups: <one line each, or "none">
```

In files mode the `tickets:` line is followed by the `board:` table `references/tickets.md` defines, read from the store in this turn. Then invoke `review` on the actual task diff (Skill tool `atlas:review`, `$review` on Codex) unless the short path already completed local review or `--no-review` was given; the flag skips only that handoff, and the short path's local review still runs. When no shipping stage is pending, run `<plugin root>/skills/ship/references/learn.md` on newly verified discoveries; recheck any affected proof after authorized learning edits. Otherwise ship owns that preflight. Record returned proof, learning/activation receipts and remaining delivery on the same owner, then reconcile native completion through `references/native.md` only at the outer boundary. Requested shipping remains part of acceptance. Do not commit here; ship runs when asked.
