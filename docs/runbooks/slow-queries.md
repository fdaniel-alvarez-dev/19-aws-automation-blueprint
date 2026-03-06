# Slow queries runbook

## Purpose
Restore acceptable p95/p99 latency by identifying and mitigating the highest-impact queries.

## Impact
- Request latency increases
- Timeouts and cascading failures in upstream services
- Elevated CPU/IO on the database

## Detection
- Elevated latency SLI, increased timeouts, or saturation alerts.
- Increased active connections / blocked sessions.

## Immediate mitigation
1) Stabilize: stop heavy background jobs and large backfills.
2) Identify top queries by total time and mean latency.
3) Consider safe short-term mitigations:
   - add an index (if low risk)
   - cap concurrency (PgBouncer limits)
   - add statement timeouts for non-critical workloads

## Verification
- p95 latency returns to within SLO.
- CPU/IO stabilize.

## Rollback / backout
- If a new index causes regressions, drop it (ideally concurrently) in a maintenance window.
- Revert the release that introduced the query regression.

## Follow-ups
- Add regression tests for query plans (where feasible).
- Add dashboards for query latency distributions.
