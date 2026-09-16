# Tickets: materialize the plan and maintain its work

Single owner of plan-to-ticket persistence and lifecycle. Planning, build and ship call this procedure; it returns to its caller. A checklist in a response, native session task list or saved plan is not a persisted ticket.

## Materialize before execution

1. An operational plan for authorized work creates or reuses ticket records before its first task runs; no `--tickets` flag is needed. The flag also requests tickets for a small task that would otherwise use the short path. Explicit no-tracking, read-only, decision-only and card-only boundaries win. Drafting a plan alone does not authorize external publication or implementation. Retain the user's requested tracker and any standing write authority through every handoff.
2. Read existing issue/plan references and the project's declared tracker first. Use its native connector or CLI; `scripts/tracker.sh` under the plugin root only detects a forge/CLI candidate, not the selected tracker or its authority. A configured Jira, Linear or Azure tracker outranks the repository forge. With no declared tracker, use an authorized detected tracker, otherwise files under the selected durable project's `docs/tickets/`; temporary chat storage is not a tracker. A declared remote tracker that is unavailable is a blocked write, never permission to switch stores. Discover actual create/search/read/update/status/relation capabilities separately; installed software is not authenticated access. File read-back does not prove commit, push or cross-session synchronization.
3. Search the selected store and re-read known IDs before creating. Reuse matching outcome tickets, including an existing parent with its checklist when all steps share one acceptance. Create children only for independently provable outcomes; decisions, scenarios and microsteps are not tickets. Preserve stable IDs across retries and changed plans. Never duplicate an external issue into a local or second remote backlog, and never reopen a closed item without matching authority.
4. Prepare each missing record with title, outcome, acceptance/proof, owned paths or owner, priority with reason, dependencies from `After`, source plan and current state. Use existing priority/state fields and conventions. Unknown assignee, estimate, due date or story points stay unknown; don't infer points from time. Map priority from evidenced urgency, impact and blocking work, not list position. If the tracker has no suitable field, retain the fact in the ticket body without creating labels, fields or a project merely for this run.
5. Execute authorized creates/updates, then read each record back and put its ID/URL or actual file path beside the corresponding plan task before the next create. Resolve native blocking relations after both IDs exist, read them back, and preserve unrelated existing relations. Without relation support, record linked `Blocked by` text and disclose that limitation. A remote write lacking authority stays a concrete prepared draft for one required approval; an access failure stays blocked. Independent authorized work may continue, but never report drafts or unsaved text as published tickets.
6. Re-read the saved plan and records. Report `tickets: <store; created/reused IDs; priority; state; dependencies; read-back result>` and any missing write/edge. Partial success retains confirmed IDs; resume only missing operations. With no writable store, report `tickets: unavailable` and the exact gap. Do not finish an operational plan with an unexplained unassigned owner or merely “create tickets next.”

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
