# Bounded native actor simulation

Internal procedure owned by the caller's coordinator, never a public skill, runtime or child workflow. `scenarios.md` calls it to evaluate the gate; dispatch only when qualified. The flag requests evaluation but cannot invent supplied actors, facts or reactions.

1. Evaluate the gate once: `trigger: automatic` when distinct supplied actors/subsystems interact and grounded plausible reactions could change feasibility, selected approach, priority or outcome; `explicit` when `--simulate` requests the same qualifying comparison; `skipped` for mechanical, settled or direct-arithmetic choices; `needs-evidence` for the smallest missing source/value read, checkpoint or user question. An explicit flag never creates actors or facts. Keep trigger separate from `capability: native-read-only | unavailable` and `result: native | analytical comparison | pending`; `automatic` never proves native execution.

2. Only for `automatic` or `explicit`, before dispatch state the supplied seed, constraints, transition rules, stop triggers and input revision. For a new root only, set a root-shared budget of three `DISPATCH WAVES`, maximum depth two (root is 0), two to three branches and two to four supplied material roles per node. Persist the existing map's root context/bounds, spent waves, pending dependency stack, node/parent/branch states and revisions, actor memory and proposals only when that map write is already authorized; otherwise keep it in-turn and unsaved. Exported self-contained references state root budget and lineage. Resume the existing root bounds and spent count; never reset them. Reuse completed exact results free; never add stores or a backlog.

3. The coordinator resolves the smallest material unresolved `INTERACTION` node. Missing empirical facts return a bounded read/checkpoint; missing values use `asking.md`; neither becomes an imagined simulation. A child has its parent ID, branch, input revision and material dependency, a scoped seed/constraint, and independent branch actors. Only the coordinator opens it, waits on it, and returns only its conditional summary to affected parent revisions; the waiting parent is pending, not stable, and no wave dispatches it with its dependent child. Siblings remain reusable and never receive another branch trajectory. Stop repeated node+input+rules with no new information.

4. Inspect the live host for actual native read-only capability. If unavailable, return `capability: unavailable; result: analytical comparison` from sourced incentives/reactions, labelled hypotheses, never role-play or another runtime. Otherwise dispatch only through that capability. Actors receive supplied seed, constraints, rules, branch state, role and role-only memory; they use no tools, writes, actions, goals, spawns or workflows, and cannot read beyond that material. Each new wave, including recovery, retry or refinement, consumes one remaining shared wave **before** dispatch. A wave is one ready node's bounded actor batch across its active branches; different nodes consume separate waves. For each exact node/branch/round/revision, dispatch all expected actors from the same immutable revision and wait at its complete barrier. Each returns:

```
proposal: <branch>; round: <n>; input revision: <id>; role: <supplied logical role>
node: <node ID>; parent: <parent ID | root>; lineage: <root/...>; dependency: <material dependency | none>
action: <proposed response>
reason: <sourced fact | stated assumption>
constraint/conflict: <effect on another role or branch | none>
memory: <compact update for this actor only>
```

5. Bind the actual actor identity from native dispatch/result metadata, never self-reported names; actors cannot invent the next revision. A branch changes only after every exact proposal is valid. The coordinator alone applies predeclared rules once, increments that branch revision once, and records deterministic consequences separately from hypotheses, conflicts, unknowns and rejected proposals. Preserve per-actor memory; stop a branch only when material state/effects stabilize, its limits end, evidence is missing or a constraint is violated. Parent resumption after a child consumes remaining waves. Budget/depth/unknown stops return the exact next probe, never success; preserve stale/uncommitted proposals only for their exact revision.

6. On resume validate seed/input/rules; changes invalidate affected dependent nodes and memory, including parents whose result used that child. Do not replay still-valid complete rounds; recover only exact-revision proposals and recreate an actor when its native identity is a snapshot rather than a verified live session. The caller's nonparticipating reviewer checks the consolidated tree; reuse an unchanged verdict and recheck only material revisions with that reviewer. Material new input/counterexample may reopen only its affected node; dissent never votes or participates.

Return branches, lineage, exact state/revisions/barriers, deterministic consequences, hypotheses, conflicts, gaps, dissent and stop reason; `trigger: automatic | explicit | skipped | needs-evidence`, decisive reason, `capability: native-read-only | unavailable`, `result: native | analytical comparison | pending`, and persistence `saved and read back | unsaved | unavailable`. The caller chooses by constraints and evidence, never consensus.

Stop when reconciliation, an exact next probe, or explicit unavailability is returned.
