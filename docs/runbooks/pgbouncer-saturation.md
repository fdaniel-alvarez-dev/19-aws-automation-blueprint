# PgBouncer saturation runbook

## Purpose
Restore throughput when client connections or pool sizes are saturating PgBouncer or the primary.

## Impact
- Connection storms
- Timeouts and queueing
- Increased latency and cascading failures

## Detection
- High client connection count.
- Pool queueing and timeouts.
- Database shows many idle-in-transaction sessions.

## Immediate mitigation
1) Stabilize: block abusive clients and reduce load.
2) Reduce pool pressure:
   - switch pool mode (transaction is safer for many workloads)
   - reduce application concurrency
3) Investigate slow queries and long transactions.

## Verification
- Connection counts stabilize and queueing drops.
- Latency recovers.

## Rollback / backout
- Revert application change that increased concurrency.
- Temporarily bypass PgBouncer only if you understand the blast radius.

## Follow-ups
- Add alerts for pool saturation and queue depth.
- Add guidance on transaction boundaries for ORMs.
