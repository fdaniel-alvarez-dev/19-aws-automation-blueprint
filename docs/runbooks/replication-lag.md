# Replication lag runbook

## Purpose
Restore healthy replication and reduce the risk of data loss or read-staleness.

## Impact
- Stale reads from replicas
- Increased risk during failover (replica may not be caught up)
- Potential user-visible performance degradation

## Detection
- Replica not connected to primary.
- `pg_stat_replication` shows high `replay_lag`.
- Replica is not in recovery mode when it should be.

## Immediate mitigation
1) Stabilize: stop risky deploys and large migrations.
2) Confirm primary health and available disk.
3) Restart the replica service if it is stuck.

## Verification
- `make check` reports the replica connected and `pg_is_in_recovery()` is `true`.
- Replication lag stabilizes and trends downward.

## Rollback / backout
- Revert the change that introduced large write amplification.
- Temporarily route reads to primary if replica is unhealthy.

## Follow-ups
- Add alerting thresholds for lag and replica disconnects.
- Review slow queries and autovacuum behavior.
