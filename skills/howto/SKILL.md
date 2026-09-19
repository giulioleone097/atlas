---
name: howto
description: Use when taking an idea from brainstorming to verified practice. Use durable context, compare approaches, evolution levels and scenarios, review the decision, execute authorized steps, and adapt the same plan from observed results.
argument-hint: "[idea, objective or saved map] [overrides: --out <file> --simulate --tickets --card-only --decision-only --evolve [next|leap|transform]]"
---

Read `<plugin root>/core/ATLAS.md` once if not loaded; `<plugin root>` is the parent of this skill's `skills/` directory. Carry scope, authorization and interactive/unattended context throughout. Resolve map-only/decision-only, card-only, ticket, simulate and read-only intents per core's Intent rule; a typed flag overrides. A decision-only intent returns the map; a card-only intent produces a scope card without implementation or publication. `--tickets` retains publication intent for an authorized build route; it is not implementation permission. `--simulate` can reopen only an affected node and cannot invent actors or facts. A saved map and its `next:` line are context, not fresh authority. A read-only intent propagates into children, including vocabulary/context handling; it permits no file writes or work handoffs.

1. Take the argument or objective already stated in this conversation. If absent in an unattended run, return the missing-subject gap; interactively, offer a relevant existing `docs/howto-*.md` or ask what to chart through `<plugin root>/skills/scope/references/asking.md` and wait. For a supplied map, read destination, nodes, checkpoints, evidence, next step and intent/source. Restore only authority supported by the originating user request, then apply current explicit overrides. Missing fields in an older map stay unknown; do not infer implementation or publication permission.

2. Read `<plugin root>/skills/scope/references/context.md` for relevant declared wiki/project context, reusing a current receipt. Establish an observable destination, acceptance evidence and real constraints from the request and available sources. Apply core's minimum-effective ladder: identify what must be true, remove unnecessary work and retain necessary guards. Read only relevant repository facts, existing issue/plan and decision evidence. On resume, recheck changed consequential assumptions, contracts and blockers; reopen only affected decisions, with the reason. Unchanged choices and applicable reach measurements are reused; a saved checkmark alone is not current proof.

3. Resolve evolution mode (none/all/next/leap/transform) and execution options through core's Intent rule and build's agency.md: explicit overrides, still-valid saved choices, then evidence-based selection. Missing flags are not missing decisions. A new mode, newly requested `--simulate`, or explicit new alternatives reopen only the affected approach node; if none exists, add one ready node even when the destination/map was settled. Preserve the user's goal. After review, record the mode, consequential input revisions, root budget, lineage and pending dependencies so the same unchanged request reuses them instead of reopening on every loop. Read `<plugin root>/skills/scope/references/atlasme.md`, the single shared brainstorming/decision engine. Carry selected simulation/evolution options with their evidence and explicit constraints; option selection never expands implementation authority. It composes scenario exploration and decision review from `<plugin root>/skills/scope/references/scenarios.md`; do not build another comparison here or call public atlasme back. Reuse a reviewed tree supplied by atlasme, existing stable decision/prerequisite IDs and material rejected alternatives. A simple settled subject needs no artificial nodes. Keep actions as evidence checkpoints with inputs, smallest useful step, observation and known time/cost budget or `unknown`. Forecasts are not completed work. Link the existing issue/plan; do not create a second backlog or one ticket per node.

4. The frontier contains unsettled decisions whose prerequisites are settled choices or verified checkpoint evidence, excluding choices deliberately deferred until the user reopens them. Resolve readable facts first; a missing source blocks only dependent decisions. Validate prerequisite IDs and cycles: correct an erroneous edge from evidence, otherwise retain the exact blocker. If a decision needs an evidence-producing checkpoint, identify the smallest one with satisfied inputs and a defined observation. When its preparation is already authorized, without read-only/decision-only/card-only limits, execute the checkpoint on its bounded outcome and proof: public `<plugin root>/skills/optimize/SKILL.md` for measurable alternatives or combinations, otherwise public `<plugin root>/skills/scope/SKILL.md`. Pass known candidates, selected options and remaining bounds; optimize owns experiments and its one ledger, linked here. It returns evidence to this map, never re-enters this controller. Preserve the parent acceptance and owner; checkpoint proof cannot close the parent or authorize publishing. Integrate the returned evidence into this map and recompute. An unchanged failed checkpoint is blocked, never retried merely by looping. Without authority or capability, retain its exact next step unexecuted. When neither decisions nor authorized evidence checkpoints can progress, go to step 6.

5. Run the shared decision engine on the ready batch with its prerequisites, scenarios, evidence and constraints. Its asking contract owns native interactive rounds; unattended work records missing user choices and continues independent facts/checkpoints. Merge reviewed choices, material dissent and reopening triggers into this map. A returned `checkpoint-needed` becomes a checkpoint with its explicit prerequisites; resume step 4 when it is executable within existing authority. Continue only while new evidence or decisions allow progress. Pending required replies stay pending; an explicit pause stops its scope, and a blocker stops only dependent work. The procedure's return alone does not end this route.

6. Render the compact map below. An explicitly read-only request returns it without writes or step 7. Otherwise update the map already read, or use `--out <file>` when explicitly supplied, else `docs/howto-<yyyy-mm-dd>-<slug>.md`; use the selected project/document workspace, never the plugin/cache. If the host cannot persist it, return the portable text labelled unsaved. Re-read an existing destination before updating, reconcile concurrent changes, and read the result back; only that proves persistence. A write gap blocks promised persistence, not independently authorized work with the in-turn map. `next:` names the exact ready decision, blocker/evidence trigger or authorized scope handoff with retained flags. Preserve current-map ownership when resuming; do not create another backlog. Saving a checkpoint while a question is pending does not close the interaction.

```
# Howto: <subject>
next: <frontier node or clear> - <howto/scope with this map and retained flags | return map>
intent: <map only | card only | implementation>; tickets: <automatic for operational plan | explicitly requested | explicitly disabled; tracker and write authority; read-back IDs once materialized>; source: <originating user request>

options: <consequential selections, explicit|saved|inferred with evidence; remaining limits>

evolution: <none|all|next|leap|transform>; reviewed inputs: <consequential source revisions/constraints|not reviewed>

## Destination
<observable outcome; acceptance/proof; constraints>

## Nodes
graph: <stable node/type/parent/branch/prerequisite/input revision when branching is material; otherwise simple decisions>
branch analyses: <actual analyst identities, completed/pending receipts and remaining shared allowance | inline/not needed>
balance: <conditional leaf-to-parent/root comparison, affected ancestor revisions and decisive gaps>
- [x] D1 <decision> -> <choice; material alternative/reason; evidence; reach/risk when relevant>. blocked by: <IDs | none>
- [ ] D2 <decision> - blocked by: <IDs | none>; missing: <source or user choice>; state: <ready | waiting | deliberately deferred>

## Scenarios and decision review
<approach versus shared conditions; expected consequences and sourced constraints; native simulation state/result when run; independent agent/lens or self-review; decisive tradeoff, material dissent and observation that would change the choice>
simulation: <trigger automatic|explicit|skipped|needs-evidence and decisive reason; capability native-read-only|unavailable; result native|analytical comparison|pending; root budget spent/remaining; lineage; source/input revisions; rules; node/parent/branch state; branch-keyed actor memory/identities; accepted/rejected and uncommitted exact-revision proposals; pending dependency/barrier; next probe>
simulation persistence: <saved and read back | unsaved | unavailable>

## Checkpoints
- C1 needs: <decision/checkpoint IDs or source> -> <smallest useful step> -> <observable proof>; budget: <known time/cost + source | unknown>; result: <planned | verified evidence and observed time | blocked reason>; owner: <existing issue/plan | unassigned>

## Evidence and next check
<consequential sources/revisions; remaining assumption and observation that would reopen it>

## Out of scope
- <node or area ruled out, and why>
```

7. When only analysis was requested or decisions remain deliberately open/blocked, return the map; pending required replies retain the asking lifecycle. For a bounded specialist need, read `<plugin root>/skills/scope/references/composition.md` and retain this owner. When clear, invoke public `<plugin root>/skills/scope/SKILL.md` with `--card-only` for a card request, or existing implementation authority for work. Carry the same map, tracker, ticket policy/authority and requested `--tickets`; scope owns acceptance and build materializes operational-plan tickets before execution. Merge its read-back ticket references, actual evidence and observed time into this map, compare with the forecast, and persist via step 6. If new evidence changes the choice, reopen only the affected branch and continue authorized work; unchanged failures stay blocked. A map or checkpoint is not destination proof. Stop after the authorized route and its read-backs finish, or return the exact blocker and next observation.
