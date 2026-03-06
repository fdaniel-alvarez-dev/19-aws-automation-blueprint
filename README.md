# 19-aws-reliability-security-runbooks

A production-minded operations runbook kit: concrete checklists, verified drills, and CI-friendly validation for incident response.

Focus: runbooks


## Why this repo exists
Runbooks only matter when they work under pressure.
This repository turns operational knowledge into executable drills and validated documentation so on-call is calmer and incidents end faster.

## The top pains this repo addresses
1) Runbooks that reduce MTTR—clear detection/mitigation/verification steps, not vague guidance.
2) Evidence-backed recovery—backup/restore drills that verify outcomes instead of producing artifacts only.
3) Safe operations hygiene—validated runbook structure in CI and guarded production-mode tests for real integrations.

## Quick demo (local)
Prereqs: Docker + Docker Compose.

```bash
make demo
```

What you get:
- a small Postgres HA lab (primary + replica) with PgBouncer
- verified backup/restore drills (safe restore into an isolated verify database)
- a runbook validator that enforces required sections across `docs/runbooks/*.md`

## Design decisions (high level)
- Prefer drills and runbooks over “tribal knowledge”.
- Keep the lab small but realistic (replication + pooling + backup).
- Make failure modes explicit and testable.

## What I would do next in production
- Add PITR with WAL archiving + periodic restore tests.
- Add SLOs (p95 query latency, replication lag) and alert thresholds.
- Add automated migration checks (preflight, locks, backout plan).

## Tests (two modes)
This repository supports exactly two test modes via `TEST_MODE`:

- `demo`: fast, offline checks against fixtures/docs only (no Docker calls).
- `production`: real integration checks against Dockerized Postgres when properly configured.

Demo:
```bash
TEST_MODE=demo python3 tests/run_tests.py
```

Production (guarded):
```bash
TEST_MODE=production PRODUCTION_TESTS_CONFIRM=1 python3 tests/run_tests.py
```

## Sponsorship and authorship
Sponsored by:
CloudForgeLabs  
https://cloudforgelabs.ainextstudios.com/  
support@ainextstudios.com

Built by:
Freddy D. Alvarez  
https://www.linkedin.com/in/freddy-daniel-alvarez/

For job opportunities, contact:
it.freddy.alvarez@gmail.com

## License
Personal/non-commercial use is free. Commercial use requires permission (paid license).
See `LICENSE` and `COMMERCIAL_LICENSE.md` for details. For commercial licensing, contact: `it.freddy.alvarez@gmail.com`.
Note: this is a non-commercial license and is not OSI-approved; GitHub may not classify it as a standard open-source license.
