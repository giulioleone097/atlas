# Bounded native actor simulation

Run only when actor or subsystem interaction can materially change a live choice, or the caller explicitly passes `--simulate`. This is a comparison aid inside `scenarios.md`, never a prediction engine, public skill, runtime or dependency.

1. Set limits before dispatch: two to four material roles, two or three meaningful branches and at most three rounds. Name the sourced seed, constraints, transition rules, stop triggers and the state/input revision. A role is a real actor or subsystem with a distinct incentive; omit decorative personas. Branches share the seed and constraints.

2. Inspect the live host for native read-only subagents. If unavailable, say `simulation: unavailable — analytical comparison only`; compare sourced incentives and reactions in the lead's analysis, label them hypotheses, and never present role-play as independent actors. Do not substitute another runtime or install anything.

3. For each branch and actor, create or reuse one isolated native instance. Give every actor the shared seed/constraints/rules plus only its branch's immutable state and approach, role/incentive and prior memory; never another branch's trajectory. It may read only the supplied material; it must not write, act externally, change goals, spawn agents, call workflows or use tools that do so. Record the native identity when the host supplies one; an old identity is evidence only of a snapshot, never a live session.

4. Dispatch each round from the same immutable state revision and wait at a synchronous barrier. Each actor returns exactly one structured proposal:

```
proposal: <branch>; round: <n>; input revision: <id>; actor: <role/native identity>
action: <proposed response>
reason: <sourced fact | stated assumption>
constraint/conflict: <effect on another role or branch | none>
memory: <compact update for this actor only>
```

5. A branch commits no transition until every expected actor returns one valid proposal for its exact revision; a missing/invalid actor leaves that round pending or incomplete. The lead alone applies the predeclared rules once at the barrier, increments that branch revision exactly once, and records before/after state, deterministic consequences separately from assumed reactions, conflicts, unknowns and rejected proposals. Actors neither vote nor reconcile. The caller's existing nonparticipating decision review consumes this record once; it is not an actor or extra council.

6. Preserve per-actor memory across its live rounds. Stop a branch only when material state and effects stabilize, its round/role/branch limit is reached, evidence is missing, or a constraint is violated; repeated actions alone are not stable while their effects accumulate. Stop the simulation when every branch stopped; report no future fact, KPI or probability claim.

7. When the caller may write an existing howto map or owner artifact, persist capability mode separately from source/input revisions, rules, branch state, each actor's memory, accepted and received-but-uncommitted exact-revision proposals/native identities, pending round and exact next action. Otherwise keep the record in-turn and label it unsaved, even when native agents ran. On resume, reload and validate all revisions/rules; a changed seed, input or rule invalidates affected dependent rounds and their memory rather than mixing old state with new. Do not replay valid completed rounds. Recover an incomplete round only with proposals for its exact immutable revision, discarding stale or mixed proposals; recreate agents when live identity cannot be verified.

Return branches, deterministic consequences, hypotheses, conflicts, evidence gaps, reviewer dissent, stop reason and `simulation: native | unavailable` and separate `persistence: saved | unsaved | unavailable`. The caller chooses the approach by constraints and evidence, never consensus.

Stop when the bounded comparison is reconciled, unavailable is explicit, or the next evidence checkpoint is clear.
