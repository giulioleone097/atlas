# Plan: four or more tasks, several owners, or a change others depend on

Read when the card is complex or ticket creation is requested, including inherited `--tickets`. Return to build after planning/publication; this procedure is not a separate public skill.

1. The goal card is the input; plan from it.
2. Read the code the work touches before decomposing anything. List the files each task will create or modify and what each one owns after the change. Name new files, symbols and task titles from the repo's `CONTEXT.md` when one exists.
3. Choose proof from existing checks or real exercises. Plan a new test only when indispensable under core's rule, naming the meaningful regression existing checks miss. Otherwise use `New test: none`; the existence or absence of a test suite alone decides nothing.
4. Cut a task where a reviewer could reject it and still accept its neighbour. Fold setup, configuration, and docs into the task whose deliverable needs them. Every task ends in something independently provable.
5. Assign owned paths per task. Tasks that can run beside each other must have prefix-disjoint path sets; when two tasks want the same file, order them with `After` rather than splitting the file to fake independence.
6. Count the tasks. Four or more, more than one owner, or a risk surface (authorization, payments, data migration, an external contract): write `docs/plans/<yyyy-mm-dd>-<slug>.md` in the shape below, the slug three or four words from the outcome. Otherwise the brief stays in chat, no file.
7. Write Non-goals from the card's exclusions plus everything the decomposition tempted you to add and you refused.
8. Self-check before handing off: every clause of the card's acceptance maps to a task, no task names a file or symbol no task produces, and no block carries placeholder text such as "TBD", "handle edge cases", or "as in T2".
9. `--tickets` or the caller's explicit request to create tickets publishes the prepared tasks. Reuse that authorization; do not require a second confirmation merely because this stage was reached through `atlasme` or `scope`. A request only to discuss or draft tasks does not authorize publication. Before a genuinely unapproved publication, present the concrete tickets and ask once through `<plugin root>/skills/scope/references/asking.md`; pending answers block publication, not independent authorized work.
   Resolve the tracker using `sh <plugin root>/scripts/tracker.sh <project-dir>` (`<plugin root>` is the parent of `skills/`). Re-read ticket references already on the source/card/plan and search the target tracker for this same outcome/task before creating anything; reuse matching items and retain their ids, never duplicate them on retry or resumption. Create only missing tickets, one per independently provable task, using its title/body and supported blocking relations from `After`. Discover the actual native connector or CLI relation capability; a command name alone does not prove support. Never reopen or close existing items.
   With no tracker CLI/connector or missing authentication, prepare `docs/tickets/<nn>-<slug>.md` instead, reuse existing matching drafts and preserve unrelated files, with `Blocked by:` references. Explicitly report local drafts and the missing remote capability; they are not published tickets. For every successful create or relation write, read it back and retain the id/URL on the existing plan/card before the next write. Report partial publication with confirmed ids and unresolved edges; retry only the missing operations.

10. Report the plan path or the brief and name the task to start with; implementation continues from the build steps.

Use exactly this shape, in chat or in the file:

```
Goal: <outcome from the card>
Acceptance: <the card's acceptance check>
Non-goals: <what this plan will not do>

T1 <behavior-named title>
  Paths: <owned paths, disjoint from every task that can run beside it>
  Acceptance: <check that passes only if T1 landed>
  Proof: <exact command or exercise>
  New test: <none, or real regression and why existing checks miss it>
  After: <task ids that must land first, or ->
```

The plan is written before any task runs.
