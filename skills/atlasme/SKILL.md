---
name: atlasme
description: Use when an idea or design needs clarification before implementation. Resolve open decisions with evidence, compare consequences across affected systems, and agree on the next step.
argument-hint: "[the idea, plan, design, file, issue or PR to grill] [--out <file>] [--tickets] [--decision-only]"
---

1. Take the argument as the subject. Empty: ask what to grill in one line and stop there. A file, an issue number, a URL or a PR: read it first through `<plugin root>/skills/scope/references/intake.md` (`<plugin root>` is the parent of the `skills/` directory this file lives in), list what the document already settles, and grill only the decisions it leaves open.

2. A subject whose outcome, boundary and acceptance you could already write is not grilled: say so in one line and carry that reading to step 3. Otherwise read `<plugin root>/skills/scope/references/atlasme.md` and work it to the end.

3. `--decision-only` returns the settled tree to the caller: skip the final handoff choice and never invoke scope/build or publish tickets. Otherwise, when the frontier is empty, first reuse any explicit authorization already given for this outcome: implementation selects build now, a card-only request selects card only, and an assessment-only request stops at the decisions. Only when that next step is undecided, ask one last question through the host's question tool, following `<plugin root>/skills/scope/references/asking.md` through the user's answer: build now, card only, or stop at the decisions, the recommendation first and chosen from what was settled. A design discussion alone does not authorize code changes; an existing implementation request does not require a second approval.

4. Print the settled tree exactly as the reference shows it, reach and risk per decision and the map when it applies. Card only, Stop, or `--out` given: write the tree to `--out <file>`, else `docs/atlasme-<yyyy-mm-dd>-<slug>.md`, headed `# Atlasme: <subject>` with a `next:` line, and print the path; `scope <file>` resumes from it. With `--decision-only`, print the tree and return to the caller, writing it only if `--out` was requested; the caller owns persistence and continuation. Otherwise carry an explicit `--tickets` or the user's request to create tickets as `--tickets`; it requests task publication, not permission to start implementation. On build now, invoke `scope` with the settled request and that flag when requested (Skill tool `atlas:scope`, `$scope` on Codex); on card only, invoke `scope --card-only --tickets` when tickets were requested, otherwise `scope --card-only`, retaining that intent on the card for later use. Follow core's skill execution contract; printing the tree or a next-step label does not complete the handoff.

Stop when the tree is printed and the chosen handoff has run, or when `--decision-only` has returned the tree to its caller.
