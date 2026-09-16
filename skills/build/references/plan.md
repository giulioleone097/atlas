# Plan: four or more tasks, several owners, or a change others depend on

Read when the card is complex, an operational plan already exists or ticket creation is requested, including inherited `--tickets`. Reuse the existing plan and its settled tasks. Return to the caller after planning and ticket read-back; this procedure is not a separate public skill.

1. The goal card and originating mandate are the input. Preserve acceptance, scope, authorized actions, known constraints and continuation intent; derive technical subgoals through `references/agency.md`.
2. Read the code the work touches before decomposing anything. List the files each task will create or modify and what each one owns after the change. Name new files, symbols and task titles from the repo's `CONTEXT.md` when one exists.
3. Choose proof from existing checks or real exercises. Plan a new test only when indispensable under core's rule, naming the meaningful regression existing checks miss. Otherwise use `New test: none`; the existence or absence of a test suite alone decides nothing.
4. Cut a task where a reviewer could reject it and still accept its neighbour. Fold setup, configuration, and docs into the task whose deliverable needs them. Every task ends in something independently provable.
5. Assign owned paths per task. Tasks that can run beside each other must have prefix-disjoint path sets; when two tasks want the same file, order them with `After` rather than splitting the file to fake independence.
6. Reuse the selected existing plan. Otherwise four or more tasks, more than one owner, or a risk surface (authorization, payments, data migration, an external contract): write `docs/plans/<yyyy-mm-dd>-<slug>.md` in the shape below, the slug three or four words from the outcome. A smaller brief can stay in chat; its ticket references still persist on the records.
7. Write Non-goals from the card's exclusions plus everything the decomposition tempted you to add and you refused.
8. Self-check before handing off: every clause of the card's acceptance maps to a task, no task names a file or symbol no task produces, and no block carries placeholder text such as "TBD", "handle edge cases", or "as in T2".
9. For an operational plan within authorized work, execute `references/tickets.md` now, before implementation; `--tickets` is not required. That procedure owns tracker selection, authority, creation/reuse, priority, relations and read-back. Reuse explicit or standing ticket authority, including ordinary-language requests carried through atlasme/howto/scope. A draft-only request retains its boundary. Store the returned references beside tasks; pending required approval follows scope's asking contract.

10. Report the plan path or brief, confirmed ticket references and first ready task, or the exact persistence gap. Implementation continues only within the caller's authority; a ticket-write gap remains visible even if independent implementation can continue.

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
  Ticket: <read-back ID/URL or file path | exact blocked write>
```

The plan is written before any task runs.
