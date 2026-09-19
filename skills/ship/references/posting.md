# Posting the dossier

Use for ship's authorized PR body publication or an explicit standalone `--out`, `--post` or `--walkthrough` request. Ship remains the publisher when it called dossier; standalone preparation never publishes on inference.

1. Write the exact dossier to `--out` or the caller's requested artifact and read it back. Prepare the complete publication payload before any missing approval question. A matching explicit PR create/update or `--post` request supplies publication authority; do not ask again for the same terms. Read-only or preparation-only intent prevents publication.

An output-only request returns here. A walkthrough-only request uses step 5 without changing the body; combined explicit intents perform their respective actions once. Body publication alone uses steps 2–4. A local-range dossier needs no existing PR.

2. Reread current PR identity, head and body before mutation. Manage Atlas-owned `<!-- atlas:narrate -->` content while preserving repository templates and author edits. For an unmarked body, preserve its text and append the requested dossier; replacing author text requires matching authority. Reconcile ambiguous/concurrent changes rather than overwrite them. Use structured native arguments or supported body-file/stdin options, such as `gh pr edit <n> -R OWNER/REPO --body-file <file>`; never interpolate multiline source text as shell code.

3. Keep the full revision-bound dossier and honor the forge's actual payload limits. When a body cannot hold it, publish the first screen plus a durable full-dossier link or authorized domain threads, with each part bound to the same HEAD. On Azure DevOps, use the existing closed-thread mechanism from `<plugin root>/skills/review/references/pr.md` without inline context, so documentation does not create unresolved review tasks. Read back every published part; partial publication remains partial.

4. Read back the published body/links and current head. A mismatch, changed head or missing required impact/risk/ownership coverage invalidates the publication proof: refresh affected evidence/content within authority and verify again. Never claim a current complete dossier from a successful write alone.

5. Inline `--walkthrough` is separate from the default body drilldown. On GitHub, prepare `comments.json` with `path`, diff `line` and a concise reason, then validate with `python3 <this skill>/scripts/pr-walkthrough.py OWNER/REPO <n> comments.json -C <repo>`. Add `--post` only with explicit inline-review publication authority. Read back the posted review and its revision; no repeated confirmation for authority already supplied.
