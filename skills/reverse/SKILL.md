---
name: reverse
description: Use when reverse engineering an achieved development result to identify which practices contributed, test their limits and internalize repeatable improvements.
---

1. Take the achieved result and available evidence from the request or current work. Read `<plugin root>/core/ATLAS.md` if not loaded; `<plugin root>` is the parent of `skills/`. Preserve scope, read-only limits and existing source/write authority. This entry reconstructs how a result was achieved; a future target alone is missing outcome evidence.
2. Run `<this skill>/references/analyze.md`; `<this skill>` is this directory. Reuse a matching analysis receipt and refresh only changed evidence. The analysis returns supported practices, hypotheses, limits and the smallest useful reuse check.
3. Pass that receipt to `<plugin root>/skills/ship/references/learn.md` for deduplication, ownership, validation and authorized activation. It reuses the analysis, never calls this entrypoint back. Read-only returns proposed rules without writes. An unsupported mechanism stays a candidate; saving or installing it cannot make it proven.

```text
result: <verified outcome/source revision; baseline -> observed KPI, guards and total cost; gaps>
practice: <action -> mechanism -> result; evidence, competing explanation and limits>
reuse: <trigger/preconditions -> minimum effective action -> check/reopen condition>
learning: <owner; candidate|unchanged|saved-local|validated-source|active-installed|blocked; proof and next real reuse>
```

Merge the analysis and learning receipts on the existing work owner; show a graph only when useful. Stop after authorized checks/writes/read-backs or the exact evidence/activation gap. Return to an enclosing workflow without starting another optimization, commit or release.
