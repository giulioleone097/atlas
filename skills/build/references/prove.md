# Prove: the smallest decisive check set

Read at the end of a build whose card names no proof command, and from ship before committing.

1. Take the acceptance check from the goal card if one exists; otherwise read the request and state the check that would fail if the change were wrong.
2. Choose the smallest decisive existing check or real exercise of the path (curl, CLI run, script); typecheck, lint and tests are options, not a mandatory sequence. A UI change is proven by a real picture of the changed flow: the end-to-end harness recording through `<plugin root>/skills/ship/references/evidence.md`, or a screenshot of the dev server exercising it; typecheck and unit tests alone do not prove what the user sees. Authoring or updating the end-to-end scenario itself follows `<plugin root>/skills/build/references/e2e.md`. Take commands from the repository: `sh <plugin root>/scripts/checks.sh <changed path>` (`<plugin root>` is the parent of the `skills/` directory this file lives in) lists available checks. Run required checks and narrow others to the changed behavior. Stop adding checks once the relevant failure would be caught.
3. Before running a command, check whether a prior run already proves it for the current tree: same command, no file it depends on changed since. Reuse that result and mark it `reused` instead of rerunning.
4. Run every remaining command exactly as written. Capture exit status and the decisive line of output, not the full log.
5. Verify core's efficiency criterion as well as behavior. Reuse the current review or compare with relevant existing/native approaches: if a demonstrated simpler equivalent removes avoidable code/work while preserving behavior, safety, maintainability and readability, adopt it within scope. Counts alone prove no improvement; do not minify or transfer hidden work to the reader/caller. Fix supported gaps and rerun only invalidated checks. No speculative search for a global minimum or tests written merely to produce proof.
6. Classify the result:
   - `DONE` — required checks passed and the scoped efficiency criterion holds; reuse existing evidence instead of a second review.
   - `DONE_WITH_CONCERNS: <concern>` — acceptance holds, with a disclosed residual risk; never use this for a failed required criterion.
   - `BLOCKED: <blocker>` — required proof is unavailable or a required criterion remains unmet, including a demonstrated efficiency gap that cannot be repaired within the current bounds.
   - `NEEDS_CONTEXT: <what>` — the acceptance check itself is unclear or has no reachable proof.

Emit exactly this, and nothing else:

```
<command> — pass | fail | unavailable | reused
<command> — pass | fail | unavailable | reused
DONE | DONE_WITH_CONCERNS: <concern> | BLOCKED: <blocker> | NEEDS_CONTEXT: <what>
```

Stop once the status line is emitted.
