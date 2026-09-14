---
name: howto
description: Use when an initiative has dependent decisions that span several sessions. Map what must be settled first, resolve the next available decision, and preserve the map for resumption.
argument-hint: "[the effort to chart] [--out <file>] [--tickets] [--card-only] [--decision-only]"
---

Carry the caller's scope and authorization throughout. `--decision-only` or a map-only request returns the decisions/map; `--card-only` may produce a scope card but never implementation or ticket publication. `--tickets` retains a publication request for the authorized build route; it is not implementation permission. Keep these intentions on the map with their originating user request. A saved map or its `next:` command is context, not fresh authorization; the current user request takes precedence. Propagate explicit read-only intent into decision children, including any vocabulary/context handling; it permits no file writes or work handoffs.

1. Take the argument as the subject. Empty: look for the most recent `docs/howto-*.md`; found, offer through the host's question tool to resume it, start something else, or stop, and continue with the answer; none, ask what to chart in one line and stop. A file whose first line is `# Howto:`: read its destination, nodes, next step, intent, ticket request and originating source. Reuse still-applicable user authorization only when that source establishes it, apply any current explicit override, then skip to step 4. Missing intent in an older map does not authorize implementation or publication.

2. A subject whose outcome, boundary and acceptance you could already write, or whose open decisions `<plugin root>/skills/scope/references/atlasme.md` would close in one pass (three or fewer questions, none blocked on another), needs no expanded map. Invoke `atlasme --decision-only` on it (Skill tool `atlas:atlasme`, `$atlasme` on Codex). Convert its result to the same map: destination includes outcome and acceptance, each settled decision becomes a checked node with its choice/evidence, deliberately open decisions remain unchecked; no decisions needed means an empty clear map. Compute the frontier and go to step 6. Howto owns persistence and the authorized handoff; this shortcut must preserve a map-only or card-only request.

3. Chart the map breadth-first, without resolving anything yet: read `<plugin root>/skills/scope/references/atlasme.md` far enough to enumerate the decision tree's nodes, one per decision, each carrying the list of nodes that must settle first (its blocking edges). A question not yet sharp enough to state precisely, only sensed as coming, is not a node: name the destination it clarifies instead and let it graduate into a node once a resolved neighbour sharpens it. Work that sits beyond the destination is not a node either: name it under Out of scope and move on.

4. The frontier is every unsettled node whose blocking nodes are all settled. An empty frontier with unsettled nodes still on the map means the map is wrong (a cycle, or a node that will never sharpen on its own): say so and stop. An empty frontier with none left: the way is clear, go to step 6.

5. Resolve exactly one frontier node this session, unless a second is a fact one bounded search settles outright: invoke `atlasme --decision-only` on that node's question alone (Skill tool `atlas:atlasme`, `$atlasme` on Codex; its question-tool contract lives in `<plugin root>/skills/scope/references/asking.md`, its reach-costing in `<plugin root>/skills/scope/references/atlasme.md`). Take its settled tree as the answer, mark the node settled on the map, and recompute the frontier. A resolution that sharpens a previously vague area turns that area into new nodes added to the map, not resolved in the same session.

6. An explicitly read-only request renders the map below with `next: return map` and returns immediately, skipping file writes and step 7. Otherwise write it to `--out <file>` when given, else `docs/howto-<yyyy-mm-dd>-<slug>.md`, reusing the file just read in step 1 once one exists rather than starting a second map for the same subject. Head it `# Howto: <subject>`. For an unsettled frontier, `next:` names the node and calls `howto <this map>` with the retained intentions, which retains map ownership while using `atlasme --decision-only`. For a clear map, name the scope handoff allowed by step 7, or state `return map` when only decisions were requested. Print the path.

```
# Howto: <subject>
next: <frontier node or clear> - <howto/scope with this map and retained flags | return map>
intent: <map only | card only | implementation>; tickets: <requested | not requested>; source: <originating user request>

## Destination
<what reaching the end of this map looks like, one or two lines>

## Nodes
- [x] <node> -> <what was chosen>. blocked by: <node, ... | none>
- [ ] <node> - blocked by: <node, ... | none>

## Out of scope
- <node or area ruled out, and why>
```

7. Return after the map is saved when decisions remain or only the map was requested. Do not resolve a second decision node this session; the bounded-fact exception in step 5 still applies. When the map is clear and a card was requested, invoke `scope --card-only` on it; when implementation was already requested, invoke `scope` on it (Skill tool `atlas:scope`, `$scope` on Codex). Carry `--tickets` when requested on either handoff; a card records that intent for later use without publishing. Run the authorized handoff in this turn, then return its result; never invoke build directly or treat saving the map as completion of requested implementation.
