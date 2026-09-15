# Atlasme: brainstorm and settle an undecided design

Shared decision engine for atlasme, howto and scope. Read for open design branches or explicit brainstorming/scenario exploration. It returns analysis to its caller; questions live in `asking.md`, scenario comparison and decision review in `scenarios.md`, execution in scope/build.

1. Establish the required observation and real constraints first. Build only material decision nodes, reusing the caller's IDs and settled choices. Every decision hangs off its actual prerequisites. The **frontier** contains decisions answerable now from settled choices and verified evidence. Distinguish choosing an approach from predicting its consequences; an explicit brainstorming request explores alternatives even when the destination is clear.

2. Find the facts yourself, always. A frontier question that needs something the repository, the filesystem, or a command can answer is not a question for the user: one bounded search settles it inline; substantial discovery goes to one `atlas-scout` per fact (Codex: `atlas_scout`) while you keep going. A running lookup is an unsettled prerequisite: only the questions downstream of it wait, the rest of the frontier is asked now. Never ask the user for what you could read, and treat a statement about how the code behaves today as a fact to check there, not a settled premise: a contradiction, with its `path:line`, is the next question.

3. Cost each option by its reach, measured at HEAD since no diff exists yet. The domains it would touch and their entry points come from `docs/atlas/map.md` (Domini, Confini, Repository collegati) when the repository has a map, else from one bounded search; every shared contract the option would change (an exported symbol, a schema, an endpoint, a config key, a message) gets its consumers counted with `git grep -w`; the repositories outside this one come from `sh <plugin root>/scripts/consumers.sh` (`<plugin root>` is the parent of the `skills/` directory this file lives in), marked unread when not checked out; a code-graph server's impact query is used when the host exposes one and cited as the source. That reach is the option's cost clause in the round. A decision whose options touch the same code, or none (a name, a wording, a policy), gets no reach. A count is what was measured, never "should be fine"; a forecast is not evidence, so no ✅, ⚠️ or ❌ here: those belong to `ship`, which measures the real diff.

4. Run `scenarios.md` for material open approaches, carrying the factual seed and measured reach. Reuse its reviewed choices and evidence instead of inventing another comparison. If it needs an experiment, return the exact `checkpoint-needed` with prerequisite IDs and decisive observation; never ask the user to guess an empirical answer. The caller may execute it within existing authority and resume this same tree. Otherwise ask only unresolved user choices in the frontier through `asking.md`; routine engineering choices within authorized constraints remain the agent's responsibility. An unattended run records the missing user choice and continues independent facts without a question panel.

5. Resolve the question batch through `asking.md`'s interaction lifecycle. Blocking tools return answers; an asynchronous acknowledgement leaves the batch pending until the user's later reply. Never answer your own round or continue to the next round on assumptions.

6. Each answer or checkpoint result reshapes the tree: settled decisions unblock their dependents. Recompute and review only branches whose assumptions changed. Questions depending on an unanswered choice wait for that choice. Vocabulary updates follow `glossary.md` when writes are authorized; read-only/decision-only analysis returns the proposed meaning without writing. A contradiction with an existing term remains explicit rather than silently changing it.

7. Stop when the frontier is empty: every branch visited, nothing silently assumed. Then print the settled tree, one entry per decision with the reach and risk of what was chosen, and hand off. A reach or risk line with nothing to say is omitted. When the settled choices reach more than one domain, one map follows the tree in the grammar of `<plugin root>/skills/ship/references/shapes.md`, "The map": lanes as the reader's mental model, the nodes the work would change, the untouched neighbours that prove the reach; no per-domain diagram, since nothing has changed yet.

```
settled:
- <decision> -> <what was chosen>. rejected: <the alternative, and why>
  reach: <domain> (<entry path:line>) -> <contract> -> <n consumers at HEAD>; <linked repository> (<n> | unread)
  risk: <the consequence in plain words>
  scenarios: <shared conditions and consequences; facts versus hypotheses>
  review: <independent agent/lens | self-review>; dissent: <material objection | none>; reopen: <observation>
open (deliberately): <what the user chose to leave undecided, or "none">
map: <one flowchart, only when more than one domain is reached>
next: <reviewed choice | user decision | checkpoint-needed with input/action/proof>
```

`scope` reuses the reach lines for the card's Risk and Size while the contracts they name are unchanged at HEAD, so the reach is measured once.

8. Record the decisions that will outlive the session. A decision whose rejected alternative a future reader would otherwise re-litigate goes to ship's learn step when the work lands, not to a document nobody reads. Do not invent an architecture-decision-record directory the repository does not already keep.

9. Never write code, start building or treat silence as agreement in this procedure. Return the reviewed choice, open branches or evidence checkpoint to its caller; returning analysis does not finish an authorized parent workflow.
