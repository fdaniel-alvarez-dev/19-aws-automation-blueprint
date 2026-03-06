# Runbooks

Runbooks should reduce MTTR by turning “what do we do now?” into a checklist.

Suggested approach:
- confirm user impact
- stabilize first, then investigate
- capture learnings and improve automation

## Runbooks in this repo
- `backup-and-restore.md`: verified restore drill (safe, isolated verify DB)
- `replication-lag.md`: detect and respond to replication health issues
- `slow-queries.md`: triage p95/p99 latency via top queries and index hints (lab-friendly)
- `pgbouncer-saturation.md`: connection pool saturation and safe mitigations
