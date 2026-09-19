---
name: intel
description: Use when a research question needs a cited brief from official documentation, specifications, source code or first-party APIs.
argument-hint: "[the question to research] [override: --out <file>]"
---

1. Take the argument or the question already stated in the conversation. Ask only when neither supplies the subject; preserve scope, explicit model/resource pins and any read-only or no-file intent.

2. Do bounded research locally. Delegate substantial independent reading only when a compatible native subagent is available and useful while the lead continues separate work. Give it the question, primary-source requirement, scope and evidence to return; the lead owns the final brief. Unavailable optional delegation permits a disclosed local fallback, never a separate task or substitution of a required model/independent review.

3. Investigate against primary sources: official docs, source code, specs and first-party APIs. Follow consequential claims to their owner; secondary commentary is a pointer to the original. Verify unfamiliar names and changing product/version claims using the user's exact term in a search, not recognition alone. State coverage and unavailable evidence. Synthesize in your own words; mark brief verbatim excerpts as quotations with their source, never as original prose.

4. Consolidate and check returned evidence, then write one Markdown brief with inline source citations. Use `--out <file>`, else the existing relevant note convention, else `docs/intel-<slug>.md`. Read an existing destination before editing and read the result back. An explicit read-only or no-file request returns the brief inline without writes.

5. Report the path and a one-line conclusion, including a material evidence gap. For an inline-only request, return that same conclusion with its supporting evidence:

```
<path> — <one-line summary of the findings>
```

Stop when the sourced brief is returned or its file is written and read back.
