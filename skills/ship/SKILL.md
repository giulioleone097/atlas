---
name: ship
description: Use when committing verified work, pushing changes, opening a PR or preparing its description. Perform only the authorized delivery steps; dossier and retrospective requests can run independently.
argument-hint: "[--push] [--pr] [--dossier [pr] [--lang <code>] [--out <file>] [--post] [--walkthrough]] [--learn [--from-pr <n>]]"
---

1. Single-purpose asks first. `--dossier [pr]`: read `<this skill>/references/dossier.md` (`<this skill>` is the directory this file lives in; it names `references/shapes.md`, `references/evidence.md` and `references/posting.md` at the steps that need them), write the dossier, and stop. A session that is stopping before the work is done: invoke `handoff` (Skill tool `atlas:handoff`, `$handoff` on Codex), then stop. `--learn`, `--from-pr <n>`, or a retrospective asked for by name: `references/learn.md` (which reads `references/environment.md` for a retrospective), then stop.

2. Get a proof status for the current tree: `<plugin root>/skills/build/references/prove.md` names the check set (`<plugin root>` is the parent of the `skills/` directory this file lives in); `review` has usually just printed `ship: ready` with its regression lines, and a result whose inputs did not change since is reused. Proceed only when the status is `DONE` or `DONE_WITH_CONCERNS`; otherwise emit `blocked: <status>` and stop. That line is the only output allowed in place of the block below.

3. Run `git status --porcelain` and `git diff --stat`. Exclude from shipping anything unrelated to this change and any scratch or temp file; never revert what you did not make; each excluded path goes in the `left:` line.

4. With `--pr` while on the default branch, first `git switch -c <type>/<slug>`: a PR needs a head other than its base, and step 7 would otherwise push the default branch itself. Group the remaining changes by behavior. One behavior, one commit. Stage only the named files, never `git add -A` or `git add .`, and commit with Conventional Commits: `<type>(<scope>): <summary>` (scope only when the repository's recent commits carry one), imperative, subject <= 50 chars, body only for a non-obvious why, subject and body in the language of the repository's recent commits (`git log -20 --format=%s`), type and scope untouched. Link the canonical owner by its full provider/project ID and URL. Use a closing reference only when its whole acceptance landed and the syntax resolves that exact owner in the delivery forge/project; never turn a cross-project or Linear/Jira ID into a bare `Closes #12` or `AB#12`. Otherwise use a plain link and step 8's authorized native transition/read-back. A partial delivery links without closing and names what remains; forge closure follows actual delivery, never manual closure merely because code exists. When an excluded file is one the proof's checks read, rerun the proof from `git worktree add <tmp> HEAD`; a failure there is `blocked: <status>`.

5. Write no agent attribution (a `Co-Authored-By` naming the model, a `Generated with ...` line, a session trailer or link) into any commit, PR title, PR body or review comment on GitHub, GitLab or Azure DevOps, whatever the host's default: the author signs the work, and blame and review threads stay free of tool noise. Never pass `--no-verify`: a failing hook is fixed at the cause and the commit retried. Never bump VERSION or CHANGELOG unless the repository already maintains them.

6. `--push`: push the current branch to its tracking remote (`-u origin <branch>` when it has none). Never force-push; `--force-with-lease` only when the user asked for it in this request.

7. `--pr`: detect the forge from `sh <plugin root>/scripts/tracker.sh`, write the body through `references/dossier.md`, push first when `--push` was not also given, and open it (`gh pr create`, `glab mr create`, `az repos pr create`). A PR already open for this branch (`gh pr view`, `glab mr list --source-branch <branch>`, `az repos pr list --source-branch <branch> --status active`) is reused, not recreated: push, replace its body only when it carries the `<!-- atlas:narrate -->` marker, say so when it does not, and report its URL. Azure DevOps rejects a description above 4000 characters: there the description carries the first screen alone, its last line pointing to the threads, and each drill-down domain, then "Fuori dal perimetro" with the command blocks, goes as its own thread (`az rest --method post` on `.../pullRequests/<n>/threads?api-version=7.1` with `{"comments":[{"content":"<part>"}],"status":"closed"}`, the call `<plugin root>/skills/review/references/pr.md` makes without `threadContext`, closed so the comment-resolution policy does not count it). Then wait for CI: `gh pr checks <n> --watch`, `glab ci status --live`, or `az pipelines runs list --branch <branch>` polled; report every failing check with its attribution, also failing on the base branch's latest run or new to this PR. Stop waiting when the checks finish or after 30 minutes; a pipeline still running prints `ci: running`.

8. Reconcile linked ticket acceptance and actual delivery through `<plugin root>/skills/build/references/tickets.md`, including issue read-back after any authorized merge; an open PR is not a closed issue. Reconcile the enclosing goal through `<plugin root>/skills/build/references/native.md`; an opened PR does not satisfy requested merge/deployment. Keep the lesson: `references/learn.md`.

9. Retire what this work resumed from: the handoff or atlasme file whose `next:` line was this work, an untracked `docs/handoff-*.md` or `docs/atlasme-*.md`, is deleted now that its commits exist; left in place, the next `scope` with no argument offers finished work.

Emit exactly this, and nothing else:

```
<sha> <subject>
<sha> <subject>
proof: <command> — pass | reused
pushed: <branch> | not pushed
PR: <url> | not requested
ci: pass | fail (<check>: new | also on base) | running | none
tickets: <IDs and reconciled state read back | none | unavailable: <gap>>
learned: <path> | proposed (not written): <path> | nothing to record
left: <path> (<why>), ... | none
```

Stop once the commits exist and any requested push, PR or dossier has run. Without `--push` or `--pr`, never push or open a PR on inference alone.
