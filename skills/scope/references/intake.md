# Intake: work that arrived from outside

Read when the argument is an issue number, a URL, a work item, a pasted bug report, a transcript, an image or a file, including handoff, atlasme and howto maps, rather than a task description.

1. Resolve the source identity before choosing a tool: provider/host, project or repository, stable ID and full URL. An explicit GitHub/GitLab issue, Linear/Jira issue or Azure work item uses that owner's available native connector or CLI, even when the code repository has another forge. Preserve the full identity through the card. Equal numbers or titles in different projects are not the same item.

   A bare number uses the project's declared tracker; with none, `sh <plugin root>/scripts/tracker.sh` (`<plugin root>` is the parent of the `skills/` directory) can identify a repository forge candidate. Resolve material ambiguity instead of guessing. Fetch with the resolved provider and explicit project/repository: GitHub `gh issue view <url> --comments`, GitLab `glab issue view <id> --repo <project> --comments`, Azure's native work-item read, or the available Linear/Jira connector. PR/MR URLs use that exact forge/project and its native PR read/diff.

   Missing access: name the unavailable operation and work from supplied content only as an unverified snapshot. An explicit remote owner remains selected; never fetch the same number from the code forge or substitute `docs/tickets/`. Local files are read only when they are the actual selected source. Never invent content or install a tool to read it. Ticket reconciliation belongs to `<plugin root>/skills/build/references/tickets.md`; intake carries authority without adding it.

   An image (a screenshot, a photo of a screen, a diagram) is read as the report: transcribe what it shows into a claim, the message, the state, the step it was taken at, before reproducing anything; its path is the `source:`. What the picture does not show is a missing detail for step 6, not a guess.

2. A pull request is an item with code attached: read the diff too, and everything below applies to it unchanged.

   A handoff file (`# Handoff:` on its first line, written by `handoff`) resumes its header outcome and its `next:` action; its Open list is a queue of actions, blockers, assumptions and follow-ups, not a replacement outcome or out-of-scope list. Reuse a Proven line only when its recorded commit still resolves, the named input paths are unchanged from that commit at `HEAD`, and the recorded command still applies; `git status --short` and a matching last commit alone do not prove that. Verify assumptions, do not redo valid proof, and carry decided lines into the card as settled, never re-asked. An atlasme file (`# Atlasme:` on its first line, written by `atlasme`) works the same way: its settled lines are decisions already made and are never re-asked, their `reach:` lines feed the card's Risk and Size without re-measuring while the contracts they name are unchanged, its open lines retain unresolved choices, and its `next:` line is the work. If it needs scenario evidence or has an unresolved approach, invoke howto with that same subject/tree and current authority, then return its result instead of scoping it again. A howto file (`# Howto:` on its first line, written by `howto`) works the same way at the scale of a whole map: its open nodes and prerequisite IDs determine the frontier, its settled choices and evidence are reused unless consequential new facts invalidate them, and its `next:` line identifies the continuation within current user authority. If that howto map still has unsettled nodes, execute `howto <file>` and return its map/result to the original caller; do not scope or build a partially settled map. A clear map continues through scope. Skip step 3 and 4 for all three unless the file names an item, then go to step 5.

3. Reproduce before believing. A bug gets the reporter's steps run against the code as it stands: the failing command, the request, the input. Report what happened - reproduced, did not reproduce, or could not tell and why. An unreproduced bug is not a fixed bug and not a wrong reporter; it is a missing detail, and step 6 asks for it.

4. Check the two things that make the work vanish before doing any of it:
   - **Already implemented.** Search by the domain concept the item describes, not by its wording, starting from `docs/atlas/map.md` when it exists; the feature may exist under another name. Found: say where it lives and stop.
   - **Already decided against.** Read the repository's own record of rejected work when it keeps one (a decisions or out-of-scope directory, closed items the CLI can list). Found: say which decision, and let the user reopen it deliberately rather than by accident.

5. Map the item onto the card fields: everything it says becomes outcome, acceptance, out of scope or risk, quoted where it is precise. What it leaves vague is the caller's: scope's card steps resolve it and set the size; atlasme settles its open decisions.

6. Too thin to act on: name exactly what is missing, as questions the reporter can answer, and never as "please provide more information". Say what you established yourself so nobody redoes it. Several open design branches rather than missing facts: that is `atlasme.md`, not a question list.

7. `--reply` posts what you found back on the item - reproduction result, what already exists, or the questions - after showing the text and getting the user's confirmation in this session. One comment, no agent attribution (the forge already records the author), and never a state change (no close, no label, no assignment) unless the user asked for that specific change.

```
source: <provider; project/repository; stable ID; URL> | <path> | pasted
claim: reproduced (<command>) | not reproduced (<what happened>) | not testable (<why>)
already: implemented at <path:line> | rejected in <path> | new
missing: <question> | none
next: card | atlasme | stop (<why>)
```

Stop once the block is printed: `next: card` returns to the caller's steps with what intake established, `next: atlasme` goes to `atlasme.md`, `next: stop` ends with the reason. Do not plan, do not write code, and do not change the item's state on your own initiative.
