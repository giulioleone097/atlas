# Dossier: the approval document

Default PR body contract for `ship --pr` and requested PR body updates; also callable alone. Domain/file drilldown is included without another flag. Scale detail to the change; an explicit summary-only request overrides presentation, never the truth of the proof. When called by ship, return the prepared body to that owner; do not publish twice.

1. Resolve the range. A PR number or URL: per the forge `sh <plugin root>/scripts/tracker.sh` names (`<plugin root>` is the parent of the `skills/` directory this file lives in), `gh pr view <n> --json number,url,headRefName,baseRefName,headRefOid,mergeable`, `glab mr view <iid> --output json` (`source_branch`, `target_branch`, `sha`, `detailed_merge_status`) or `az repos pr show --id <n>` (`sourceRefName`, `targetRefName`, `lastMergeSourceCommit`, `mergeStatus`); then `git fetch origin +refs/heads/<base>:refs/remotes/origin/<base> +<head>:refs/remotes/origin/pr/<n>` with `<head>` = `refs/pull/<n>/head` on GitHub, `refs/merge-requests/<iid>/head` on GitLab, the `sourceRefName` on Azure DevOps (it publishes no head ref); range `merge-base(origin/<base>, origin/pr/<n>)..origin/pr/<n>`. A branch or nothing: current branch against the merge-base with the default branch. Record `OWNER/REPO` (tracker.sh's `repo=`), `<n>`, `BASE`, `HEAD` and the merge status field named above.

2. Audience, language, size. Write the shortest clear approval document preserving full meaning: change, reason, behavior, evidence, constraints, uncertainty and next action. Cut repetition and ceremony, not content or readability. Use plain precise words and only useful structure; avoid cryptic compression. Technical locators belong with their evidence unless essential to the sentence. Explicit language wins; a supplied rewrite retains its language, otherwise use recent repository PRs/commits. Translate headings/labels; keep `<!-- atlas:narrate -->`. Omit empty or duplicative sections; the example below is not a quota of headings or bullets. Examples such as 500 to 300 words are not targets; an explicit word limit applies, otherwise use only necessary words.

3. Partition the exact range with `python3 <plugin root>/scripts/pr-partition.py -C <repo> BASE HEAD`. Account for every changed path: inspected behavior, generated/mechanical with its producer/check, or an explicit evidence gap. Read the judgment bucket deeply and group it into meaningful domains, using the existing map when relevant. Mechanical/generated files are accounted for without pretending they were semantically reviewed. Link real affected consumers; do not invent outside domains or silently omit paths.

4. Blast radius, mechanical: affected projects from the workspace tool (`nx show projects --affected --base=BASE --head=HEAD`; turbo, bazel, `go list`, solution references elsewhere), pure dependents marked; `python3 <this skill>/scripts/pr-contracts.py -C <repo> BASE HEAD` (`<this skill>` is the skill directory above this `references/` folder) for removed exported symbols and changed signatures with consumers outside the diff and deleted files still referenced (judge each hit); for every shared contract the diff changes (DTO, schema, socket event, endpoint, config key, bus message, Helm value) name the consumers at HEAD with `git grep -w` and record the line that absorbs or breaks - that line is what the drill-down cites, not "should be fine". Then outside the repository: `sh <plugin root>/scripts/consumers.sh` names the sibling checkouts and workspace members that depend on this one; each gets the same `git grep -w` for the changed contracts and its own domain in the drill-down when it is reached, marked unread when it could not be read.

5. Reuse executed proof only for the same HEAD, inputs and relevant environment. Run missing or invalidated repository checks for affected behavior/dependents; use `python3 <this skill>/scripts/test-summary.py` for existing JUnit/TRX output. Attribute failures with comparable base evidence, rerunning the base when needed. Add required contract/container/migration/E2E proof only for the actual change; `<this skill>/references/evidence.md` owns real visual artifacts. A test's existence or a plausible code path is not an executed pass. Report unavailable checks, unproven safety and incomplete coverage as gaps with owner/next observation; never turn missing evidence or absent CI into a green result. Writing a dossier alone is not a reason to repeat unchanged tests.

6. Read the judgment bucket per domain, entry points first; above 25 files dispatch one `atlas-scout` per domain in one message (Codex: `atlas_scout`) asking "what does each file do now, why did it change, what reaches it from outside, and what did NOT change around it", and read only their `path:line` lines. Every domain needs its before/after shape and its boundary list, so a scout that returns prose without call sites gets one follow-up, then you read the entry points yourself.

7. Use `<this skill>/references/shapes.md` when a map or before/after diagram clarifies changed relationships. Keep one overall map for interacting domains and only useful domain diagrams. A small single-path change can use a concise explanation and its file drilldown; do not create diagrams merely to fill a template.

8. Preserve and fill the repository PR template; the dossier sits beneath it. Bind exact BASE/HEAD. Keep merge, deployment and rollout gates distinct: a release-only restriction does not establish a merge blocker, and unknown readiness is unassessed. Compression may neither strengthen nor weaken a supplied claim or invent a verdict. The first screen stays within 20 lines; domain/file drilldown retains every changed path and evidence/gap link, using collapsible detail where supported. Include optimization checkpoint SHAs and measured lineage when relevant. State each required action once and reference it elsewhere instead of repeating it.

```
<!-- atlas:narrate -->
range: <BASE..HEAD; source/PR identity; proof date>
## Verdetto: <mergeabile | mergeabile con condizioni | non mergeabile oggi>
<the one blocking reason and its fix, owner named; or "nulla blocca">

## Cosa cambia
- <3-5 bullets: what the user or operator gets, what disappears, what stays untouched>

## Mappa
<one map: lanes = runtimes or tiers, changed and unchanged nodes, the hero edge marked>

## Drill-down
### <n>. <domain, in plain words> - <✅ | ⚠️ | ❌> - <files changed, +lines/-lines>
<two or three sentences: the pressure that opened this domain and what runs differently now, in the order it runs>
<the domain's diagram>
- confine: <what leaves this domain> - <consumer at HEAD> - <the line that absorbs it or the test that pins it>
- prova: <what ran> - <result, counts, base attribution for a pre-existing failure> | <flow> - <e2e command> - <passed n/n> - <screenshot or video link>
- decisione: <chosen> over <rejected> - <the measured reason>
- rischio: <the consequence in plain words>
<details><summary>Dettaglio file e prove</summary> changed paths and dispositions, path:line per claim, behavior/boundary/evidence or gap, deleted paths and remaining consumers </details>

## Fuori dal perimetro
- <what> - <why it could not be verified here> - <who covers it and when: release runbook, nightly job, the author before merge>

<details><summary>Comandi eseguiti</summary> one line per command as run: result, counts, base comparison, worktree paths, range, date </details>
<details><summary>Ordine di lettura</summary> <= 25 `path - what it does now, why it changed`, follow-ups </details>
```

9. ✅ means applicable executed evidence passes with coverage stated; ⚠️ includes pre-existing failures, residual risks and evidence gaps; ❌ means a new attributed failure or unmet required criterion. Before returning, remove avoidable prose while checking that every distinct claim, qualifier, evidence link and required path remains, with equal or better readability. Moving text to details or an appendix is navigation, not compression; blockers stay visible. Domain 25-line and main 400-line limits are ceilings, never targets. Retain complete revision-bound path coverage in a linked appendix when needed, without artificial domain splits or a duplicate review.

10. Use `<this skill>/references/posting.md` for requested persistence/publication. Reuse matching explicit publication authority; a dossier-only request does not grant it. In a ship workflow return the prepared body, BASE/HEAD and proof/coverage references to ship, which publishes and reads back once.
Stop after returning the complete dossier or performing its authorized standalone publication. Keep gaps explicit; do not edit code or promote generated-file accounting to a semantic review.
