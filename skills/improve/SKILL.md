---
name: improve
description: Use when assessing codebase structure or choosing a broader improvement. Route simplification, measured optimization and audits to their procedures; investigate structural problems and propose a bounded change.
argument-hint: "[what to make healthier: a direction, a subsystem or a planned change]"
---

1. Classify the ask from outcome and evidence, then run the best-supported branch under core's Intent rule. Product/outcome evolution invokes public `<plugin root>/skills/howto/SKILL.md` with the selected degree of change and current authority. Shrinking or de-slop invokes `simplify`; measurable latency, size, cost or quality invokes `optimize`, which discovers missing measurement options. An audit invokes `review` in its requested mode (`--repo`, `--debt`, `--rules`). A structural assessment such as "how can we make this easier to change" reads `<this skill>/references/deepen.md` (`<this skill>` is this file's directory). Several plausible routes are an engineering choice: inspect the relevant facts, choose the smallest route that can prove the outcome and carry necessary later stages. Ask through `<plugin root>/skills/scope/references/asking.md` only when unresolved user goals or value tradeoffs change acceptance; never ask the user to classify a skill.

2. A dispatch ends there: the invoked skill owns its report. A survey ends as deepen.md directs: report written, then the picked card handed to `atlasme` (Skill tool `atlas:atlasme`, `$atlasme` on Codex). Either way print:

```
dispatch: <the ask in a few words> -> howto --evolve | simplify | optimize | review --repo | --debt | --rules | deepen survey - <the signal that decided it>
report: <path - survey only>
card: <the pick> -> atlasme | none picked - <survey only>
```

Stop when the one dispatch has run or the survey report is printed and its pick handed to `atlasme`. One dispatch or one survey per run. A dispatched skill completes its own authorized edits and proof; only the structural survey is read-only, with its proposed change landing later through `scope` -> `build`.
