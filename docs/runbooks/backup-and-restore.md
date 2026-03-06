# Backup & restore drill

Goal: make recovery predictable by practicing it.

## Purpose
Prove you can restore data successfully, safely, and repeatably.

## Impact
- Without tested restores, backups can silently rot.
- During incidents, ambiguity increases downtime and data-loss risk.

## Detection
- Scheduled drill cadence (e.g., weekly/monthly) or after high-risk changes.
- Restore failures or verification query failures.

## Immediate mitigation
Run the drill:
```bash
make up
make seed
make backup
make restore
make verify
```

## Verification
- `make verify` completes successfully.
- The restore runs into an isolated verification database (`appdb_verify`) by default.

## Rollback / backout
- If a restore step fails, do not run destructive commands on the primary database.
- Keep `appdb` untouched; rerun the drill and inspect logs (`make logs`).

## Follow-ups
- Add PITR (WAL archiving) and schedule periodic PITR restore drills.
- Track RTO/RPO metrics and align them with your reliability objectives.
