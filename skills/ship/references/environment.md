# Retro: improve the environment, not the code

Use when the user asks for a retrospective on a session rather than a rule about the code. The subject is what the next agent will find waiting for it. Read the session's own record first; a category with no evidence in that record is not a candidate.

Rank candidates by evidenced wasted work or failed outcomes in that session. Return only distinct reusable candidates to `learn.md`; it owns scope, authority, writing and verification. No fixed lesson quota.

| Category | Look for | Trigger |
|---|---|---|
| Navigation | the search that took many tries, the file nobody could find, the hidden dependency between two files | the session spent more than a few tool calls locating something |
| Automated check | the mistake a typecheck, lint rule, or test would have caught for free | a defect reached review that a machine could have caught |
| Review rule | the standard the reviewer missed, or the rule that fired on something harmless | the review missed a real defect, or flagged noise twice |
| Steering weight | instructions in AGENTS.md or CLAUDE.md that steer nothing, or that belong in a review rule instead | the file is long and the session ignored parts of it |
| Tool economy | the command whose output flooded the context, the tool called in a loop, the query that returned a whole file to read one line | one call cost a visible share of the window |
| Information access | the fact that existed but was not reachable: a log the agent could not read, a service with no read-only access | a question was answered by guessing because the source was out of reach |

Implementation benefits from useful navigation and cheaper reads; review needs the applicable standard. An unused instruction is a candidate for investigation, not proof that its safeguard is unnecessary. Narrow or remove only superseded or disproven guidance within scope after checking its callers and protected behavior.

Return the evidence, smallest durable change and proposed owner to `learn.md`. Its existing-authority gate applies; this reference adds no confirmation step or mutation authority.
