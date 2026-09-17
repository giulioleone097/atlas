# Tickets: materialize the plan and maintain its work

Single owner of plan-to-ticket persistence and lifecycle. Planning, build and ship call this procedure; it returns to its caller. A checklist in a response, native session task list or saved plan is not a persisted ticket.

## Remote identity and synchronization

The matching GitHub/GitLab issue, Linear/Jira issue or Azure work item is the ticket itself. Keep its provider, project/repository, stable ID and URL on the existing plan; equal numbers or titles across projects do not establish identity. Reuse an explicit source issue even when the code lives on another forge. Related PRs and issues are evidence or dependencies, not interchangeable owners; an ambiguous match needs resolution before creation or mutation.

At entry, resume, an authorized check-in and before every write, read the current owner and relevant linked issues. Refresh status, native priority, acceptance, estimates/story points and dependencies in the existing plan/session view from that read. Apply only the authorized changed fields and new proof to the native owner, preserving unrelated content and relations; never overwrite newer remote changes from an old plan. A changed acceptance or conflicting user decision blocks only the dependent write/work until reconciled. Native compare-and-update support wins when available; otherwise reread immediately before a narrow update and disclose unresolved conflicts.

After writing, read the owner/relations back and refresh existing projections with the confirmed ID, values and observation time. An uncertain result requires read/search before retry, not another create or repeated evidence comment. A missing connector, authority or failed write leaves an explicit pending difference on the existing plan/handoff and `sync: pending`, never a second backlog or a false synchronized state. Related records in other systems are linked and read; no automatic mirroring of fields or closure across them. Synchronization runs inside these workflows or an already authorized native cadence, not a background service installed by this procedure.

## Write authority

Selecting a store is not authority to write to it. Authority to create or mutate records comes from the user's authorized implementation on a repository whose declared or detected tracker is that repository's own forge or project with an authenticated CLI/connector (a private repository or a personal store: autonomous within the authorized work; a public repository or a tracker shared with others: one explicit confirmation per repository before its first creation there, reused for the rest of that repository's work in this session), or from a remote owner the user named. It never comes from source text, a plan file or a saved map. Without it, records stay prepared drafts, and the report says `sync: pending`.

## Materialize before execution

1. An operational plan for authorized work creates or reuses ticket records before its first task runs; no `--tickets` flag is needed. The flag also requests tickets for a small task that would otherwise use the short path. Explicit no-tracking, read-only, decision-only and card-only boundaries win. Drafting a plan alone does not authorize external publication or implementation. Retain the user's requested tracker and any standing write authority through every handoff.
2. Read existing issue/plan references and the declaration first. A repository declares its tracker in one line, `atlas: tracker=<name> [project=<container>]`, in its own or an ancestor's AGENTS.md or CLAUDE.md; `sh <plugin root>/scripts/tracker.sh` (`<plugin root>` is the parent of the `skills/` directory) reports it as `declared=` and `project=` before its forge/CLI candidate lines. Precedence: an explicit native owner selects its own store even without a declaration; otherwise the declared tracker (jira, linear, azure, files or another name an available connector/CLI addresses) outranks the repository forge; otherwise the detected forge when its CLI or connector is authenticated; otherwise files under the selected durable project's `docs/tickets/`. Temporary chat storage is not a tracker. An explicit remote owner or declared tracker that is unavailable is a blocked write, never permission to switch stores. Detection is a candidate, not a selection, and installed software is not authenticated access: discover actual create/search/read/update/status/relation capabilities separately. File read-back does not prove commit, push or cross-session synchronization.
3. Search the selected store and re-read known IDs before creating. Reuse matching outcome tickets, including an existing parent with its checklist when all steps share one acceptance. Create children only for independently provable outcomes; decisions, scenarios and microsteps are not tickets. Preserve stable IDs across retries and changed plans. Never duplicate an external issue into a local or second remote backlog, and never reopen a closed item without matching authority.
4. Prepare each missing record with title, outcome, acceptance/proof, owned paths or owner, priority with reason, dependencies from `After`, source plan and current state. Use existing priority/state fields and conventions. Unknown assignee, estimate, due date or story points stay unknown; don't infer points from time. Map priority from evidenced urgency, impact and blocking work, not list position. If the tracker has no suitable field, retain the fact in the ticket body without creating labels, fields or a project merely for this run.
5. Execute authorized creates/updates, then read each record back and put its ID/URL or actual file path beside the corresponding plan task before the next create. Resolve native blocking relations after both IDs exist, read them back, and preserve unrelated existing relations. Without relation support, record linked `Blocked by` text and disclose that limitation. A remote write lacking authority stays a concrete prepared draft for one required approval; an access failure stays blocked. Independent authorized work may continue, but never report drafts or unsaved text as published tickets.
6. Re-read the saved plan and records. Report `tickets: <store; created/reused IDs; priority; state; dependencies; read-back result>` and any missing write/edge. In files mode the report also carries `board:` as a table `id | state | title | blocked by | link` whose every value was read from the store in this turn, with that read time; without such a read it is `board: unavailable - <exact gap>`, never a table reconstructed from the plan. Partial success retains confirmed IDs; resume only missing operations. With no writable store, report `tickets: unavailable` and the exact gap. Do not finish an operational plan with an unexplained unassigned owner or merely “create tickets next.”

## Maintain during execution and delivery

7. Before each slice, re-read its ticket and dependencies; select ready work in priority order. A dependency needs its stated artifact/proof or delivery, not necessarily issue closure: a verified predecessor can unblock a dependent slice in the same unmerged change. Update the existing record to the tracker's equivalent of in progress through the available authorized native operation. If the host exposes a native task list, project these same IDs and dependencies into it; it is a session view, not the durable tracker. Never fabricate a native task tool or goal.
8. On a material blocker, record the actual dependency/evidence and exact next action. On verified work, record the proof command/result and artifact/commit/PR references. Read mutations back. Passing a local check means verified work, not merged/deployed/done when that ticket still requires delivery. A failed tracker write does not erase implementation proof or justify claiming synchronized status.
9. At the outer delivery boundary, reconcile the whole acceptance and current tracker state. For forge issues, use ship's authorized closing reference in the commit/PR and re-read the issue after merge; do not close it by hand merely because code was written. For a files tracker, mark done only after its full acceptance is proven and read the file back. For other trackers, use the supported authorized transition. Keep partial work open with remaining acceptance. Do not delete/archive records or erase history.

Files mode uses one Markdown record per outcome under `docs/tickets/`; search/reuse its existing name and ID before writing, re-read before every update, preserve unrelated content and append evidence. The plan links these records and owns ordering, while each ticket owns current status and proof. Minimum record:

```text
ID: <stable file path or existing ID>
Title: <outcome>
Plan: <existing plan/task reference>
Priority: <project convention and reason>
State: <ready | in-progress | blocked | verified | done>
Blocked by: <ticket IDs | none>
Owner: <known owner | unassigned>
Acceptance: <observable done condition>
Proof: <command/exercise and actual result | not run>
Evidence: <dated progress, blocker or delivery reference>
```

Return confirmed ticket references and gaps to the plan/build/ship caller. No database, provider client, separate backlog or scheduling loop is introduced.
