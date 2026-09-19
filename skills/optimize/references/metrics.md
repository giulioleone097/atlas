# Recommend and settle the KPI

Optimize owns this contract. Presets are starting points, not compulsory metrics, targets or new dependencies. Read only evidence relevant to the requested outcome.

Efficacy and efficiency hold together: prefer a demonstrated equally sound result with less end-to-end time, effort or maintained code; never lower outcome quality to improve a proxy. Include verification/rework and user/reader effort when material. Compare like workloads and scopes. Lines/words are diagnostics under consistent formatting and full content coverage, not optimization targets in themselves; measured savings require comparable evidence, not claims from a shorter diff.

| Preset | Suggested primary metric | Direction | Companion checks or guards |
|---|---|---|---|
| Latency / duration | p95 request latency in ms, or elapsed build/task seconds | Lower | Same workload and concurrency; correctness, error rate |
| Throughput | Successful operations per second | Higher | Fixed workload, p95 latency, errors, resource limits |
| Resources | Peak resident MiB, CPU seconds or measured I/O operations | Lower | Same completed work; correctness and elapsed time |
| Footprint | Shipped compressed bytes or installed bytes | Lower | Same supported features and target; build checks |
| Cost | Measured cost per successful task | Lower | Same evaluation set and quality; current sourced rates |
| Quality | Passed cases / fixed total, or an existing calibrated score | Higher | Held-out cases, latency and cost; no changed denominator |

1. Inspect the user outcome, relevant callers, benchmarks, recent comparable evidence and a small authorized probe. Recommend one primary KPI and only material guard metrics; offer up to two viable alternatives when they represent different user benefits. For each state what it measures, unit/direction, why it serves the outcome, available source/command and coverage gap. A custom domain KPI is preferable when the presets would be proxies without a demonstrated link. Never ask the user to invent a metric or shell command from scratch.

2. Reuse an explicit metric/priority or a still-valid user-selected contract, including one inherited from another skill. Otherwise present the recommendation and meaningful alternatives through `<plugin root>/skills/scope/references/asking.md`: discover the permitted native tool and its actual schema/mode, recommendation first, accept a custom reply and await the answer. Ask which result matters and any material tradeoff, not which flags to type. An inferred recommendation saved by an agent is not user selection. If the user explicitly delegates KPI choice, choose and disclose the evidence-backed recommendation within known values; delegation never authorizes new targets or relaxed constraints. Unattended/no-questions runs retain an unresolved priority while continuing independent discovery.

3. Keep one primary metric; other relevant metrics are guards or diagnostic observations. Do not invent composite weights, tradeoffs or numeric targets. Existing accepted limits win; a missing consequential tolerance is a user decision, not an assumed allowance. Express a minimum-quality guard as a corresponding maximum error/loss metric when needed. A preset chooses neither acceptable regression nor a new benchmark result.

4. Bind selected KPI, population/workload, unit, direction, command, setup, resolution, correctness checks, guards and selection provenance on the single experiment ledger. Distinguish recommendation, user answer and measured baseline. Keep workload and guards fixed across singles and combinations; changed acceptance requires a new contract and comparable control. Missing measurement capability blocks that claim; simulated values, activity counts and unlabeled proxies never prove the requested outcome.

Return the settled contract or exact pending decision to optimize; commands, paths, worktrees and bounded execution options remain agent-owned.
