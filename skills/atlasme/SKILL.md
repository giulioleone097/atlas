---
name: atlasme
description: Use when brainstorming an idea or design. Explore feasible approaches and scenarios, challenge the choice with decision review, resolve missing user decisions, and continue already-authorized work through howto.
argument-hint: "[idea, design, file, issue or PR to explore] [--out <file>] [--tickets] [--decision-only]"
---

1. Take the argument or idea already stated in the conversation as the subject. Missing: follow `<plugin root>/skills/scope/references/asking.md`. A file, issue, URL or PR first uses `<plugin root>/skills/scope/references/intake.md` (`<plugin root>` is the parent of `skills/`); retain what the source settles and explore the remaining choices. Read `<plugin root>/core/ATLAS.md` once if not loaded.

2. A mechanical request whose approach is already settled needs no invented alternatives. Otherwise read `<plugin root>/skills/scope/references/atlasme.md` and run its shared brainstorming/scenario engine to a reviewed choice or exact evidence checkpoint. Reuse existing choices, sources and review findings; a clear destination alone does not settle the route. Propagate read-only, decision-only and unattended boundaries into the procedure.

3. `--decision-only` returns the tree to its caller without execution or ticket publication. Assessment/read-only requests stop at the analysis. Otherwise reuse explicit authorization: implementation continues through howto with the reviewed choice or evidence checkpoint; card-only retains its boundary. If the next step genuinely lacks a user decision, ask through `<plugin root>/skills/scope/references/asking.md` and await the answer. A design discussion alone does not authorize implementation; existing authority needs no second approval.

4. Return the reference's tree and decision-review evidence. Explicit `--out` saves it as `# Atlasme: <subject>` in the selected user workspace, after re-reading/reconciling an existing file and reading the write back; read-only always suppresses writes. Otherwise pass the in-turn result to avoid a second decision document. Existing atlasme files remain resumable. For authorized implementation or a card, invoke public `<plugin root>/skills/howto/SKILL.md` with this same subject, settled tree/checkpoint, source authority, `--card-only` when requested and `--tickets` when requested. Howto owns the route and persistence, scope owns the card, build owns execution/tickets. A tree or next-step label does not complete the handoff.

Stop when the tree is printed and the chosen handoff has run, or when `--decision-only` has returned the tree to its caller.
