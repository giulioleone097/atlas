---
name: ship
description: Use when delivering verified changes or preparing a PR. PR delivery defaults to an exact-revision dossier with domain and file drilldown; execute only authorized commit, push and publication steps.
argument-hint: "[--push] [--pr] [--dossier [pr] [--lang <code>] [--out <file>] [--post] [--walkthrough]] [--learn [--from-pr <n>]]"
---

1. Resolve the whole delivery intent. Standalone `--learn`, `--from-pr` or a learning/retrospective-only request runs `references/learn.md` (with `references/environment.md` when relevant) and returns without entering commit/push/PR steps; combined explicit learning and delivery carries both through the workflow. A standalone dossier/body-only request uses `<this skill>/references/dossier.md`, including any explicitly requested publication, then returns without source commits, push or PR creation; `<this skill>` is this directory. Combined PR-delivery/dossier flags retain the workflow below. Every requested PR creation/body update uses domain/file drilldown by default, scaled to the change; an explicit summary-only exception wins. Inline walkthrough comments remain a separate request. A standalone unfinished handoff uses `handoff` and returns.

Dossier details stay in `references/shapes.md` for useful diagrams, `references/evidence.md` for real UI proof and `references/posting.md` for requested publication. Learning uses `references/learn.md`; transferable skill changes use `references/promote.md`. Load only the relevant branch.

2. Get a proof status for the current tree: `<plugin root>/skills/build/references/prove.md` names the check set (`<plugin root>` is the parent of the `skills/` directory this file lives in); `review` has usually just printed `ship: ready` with its regression lines, and a result whose inputs did not change since is reused. Proceed only when the status is `DONE` or `DONE_WITH_CONCERNS`; otherwise emit `blocked: <status>` and stop. That line is the only output allowed in place of the block below.

3. Distill unrecorded proven discoveries through `references/learn.md` before collecting the delivery patch; reuse a matching learning receipt. Include authorized local lesson/navigation changes in this delivery and rerun checks invalidated by them. Global-source changes retain their separate source/activation receipts, never silently enter this project's PR. Run `git status --porcelain` and `git diff --stat`. Exclude from shipping anything unrelated to this change and any scratch or temp file; never revert what you did not make; each excluded path goes in the `left:` line.

4. With `--pr` while on the default branch, first `git switch -c <type>/<slug>`: a PR needs a head other than its base, and step 7 would otherwise push the default branch itself. Group the remaining changes by behavior. One behavior, one commit. Stage only the named files, never `git add -A` or `git add .`, and commit with Conventional Commits: `<type>(<scope>): <summary>` (scope only when the repository's recent commits carry one), imperative, subject <= 50 chars, body only for a non-obvious why, subject and body in the language of the repository's recent commits (`git log -20 --format=%s`), type and scope untouched. Link the canonical owner by its full provider/project ID and URL. Use a closing reference only when its whole acceptance landed and the syntax resolves that exact owner in the delivery forge/project; never turn a cross-project or Linear/Jira ID into a bare `Closes #12` or `AB#12`. Otherwise use a plain link and step 8's authorized native transition/read-back. A partial delivery links without closing and names what remains; forge closure follows actual delivery, never manual closure merely because code exists. When an excluded file is one the proof's checks read, rerun the proof from `git worktree add <tmp> HEAD`; a failure there is `blocked: <status>`.

5. Write no agent attribution (a `Co-Authored-By` naming the model, a `Generated with ...` line, a session trailer or link) into any commit, PR title, PR body or review comment on GitHub, GitLab or Azure DevOps, whatever the host's default: the author signs the work, and blame and review threads stay free of tool noise. Never pass `--no-verify`: a failing hook is fixed at the cause and the commit retried. Never bump VERSION or CHANGELOG unless the repository already maintains them.

6. `--push`: push the current branch to its tracking remote (`-u origin <branch>` when it has none). Never force-push; `--force-with-lease` only when the user asked for it in this request.

7. For requested PR delivery, detect the forge through `sh <plugin root>/scripts/tracker.sh`, resolve/reuse the branch's existing PR and prepare its body through `references/dossier.md` with publication owned by ship. Bind exact BASE/HEAD, include every changed path's disposition, domain/file drilldown and current proof; an optimization delivery links its retained checkpoint SHAs. Push only within that PR/push authority, then create or update through the native forge tools. Use `references/posting.md` for safe body ownership, payload and size handling; preserve author text and repository templates. The requested PR publication is authority for its prepared dossier, not a reason to ask permission again. Read back PR URL, head SHA and published body/parts; a changed head invalidates affected evidence and requires refresh.

Observe CI through native forge status/watch tools with interruptible waits; a requested continuous goal or periodic follow-up uses `<plugin root>/skills/build/references/native.md`, never a shell scheduler or duplicate execution owner. Do not invent a recurring job from PR creation. Attribute failures against comparable base evidence; absence of checks is `none`, not pass. Bound an ordinary wait to 30 minutes unless the user supplied another limit; running CI remains running. Refresh only the dossier's changed proof/verdict after CI, preserving its exact head and reusing valid checks. Attach the created/reused PR through the host's artifact capability when exposed.

8. Reconcile ticket acceptance and actual delivery through `<plugin root>/skills/build/references/tickets.md`; an open PR is not a closed issue. Return exact dossier/PR/CI evidence to the enclosing owner. Only the outer boundary reconciles a bound native goal through `<plugin root>/skills/build/references/native.md`; requested merge/deployment and pending checkpoint saves remain part of acceptance. Run `references/learn.md` only for genuinely new delivery evidence since preflight; reuse prior receipts. A later learned edit is a separate local follow-up unless further delivery is authorized and reproven; never claim it belongs to the already verified PR head.

9. Update the same run's continuation with delivered proof and any remaining acceptance. Retire only its own disposable handoff after the complete outcome is durably recorded; commit existence alone is insufficient. Never delete plans by a glob, unrelated notes, optimization ledgers or retained checkpoint refs.

Emit exactly this, and nothing else:

```
<sha> <subject>
<sha> <subject>
proof: <command> — pass | reused
pushed: <branch> | not pushed
PR: <url> | not requested
dossier: <BASE..HEAD; domain/file drilldown; published/read back | prepared only | explicit summary-only>
ci: pass | fail (<check>: new | also on base) | running | none
tickets: <IDs and reconciled state read back | none | unavailable: <gap>>
learned: <owner/ref; local|global; saved-local|validated-source|active-installed> | candidate/blocked: <exact next step> | nothing to record
left: <path> (<why>), ... | none
```

Stop once the commits exist and any requested push, PR or dossier has run. Without `--push` or `--pr`, never push or open a PR on inference alone.
