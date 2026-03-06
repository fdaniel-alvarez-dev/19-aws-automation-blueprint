#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNBOOKS_DIR = REPO_ROOT / "docs" / "runbooks"

REQUIRED_SECTIONS = [
    "Purpose",
    "Impact",
    "Detection",
    "Immediate mitigation",
    "Verification",
    "Rollback / backout",
    "Follow-ups",
]


@dataclass(frozen=True)
class ValidationResult:
    file: str
    status: str  # pass|fail
    missing_sections: list[str]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _headings(markdown: str) -> set[str]:
    headings = set()
    for line in markdown.splitlines():
        m = re.match(r"^##\s+(.*)$", line.strip())
        if m:
            headings.add(m.group(1).strip())
    return headings


def validate_runbook(path: Path) -> ValidationResult:
    abs_path = path if path.is_absolute() else (REPO_ROOT / path).resolve()
    text = abs_path.read_text(encoding="utf-8", errors="replace")
    headings = _headings(text)
    missing = [sec for sec in REQUIRED_SECTIONS if sec not in headings]
    status = "pass" if not missing else "fail"
    return ValidationResult(file=str(abs_path.relative_to(REPO_ROOT)), status=status, missing_sections=missing)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate runbook structure and produce an evidence artifact.")
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    parser.add_argument("--out", default="artifacts/runbook_validation.json")
    args = parser.parse_args(argv)

    if args.mode == "production" and os.environ.get("PRODUCTION_RUNBOOKS_CONFIRM") != "1":
        sys.stderr.write(
            "Production validation is guarded.\n"
            "Set PRODUCTION_RUNBOOKS_CONFIRM=1 to confirm you intend to validate runbooks in production mode.\n"
            "Example:\n"
            "  PRODUCTION_RUNBOOKS_CONFIRM=1 python3 tools/validate_runbooks.py --mode production\n"
        )
        return 2

    runbooks = sorted(p for p in RUNBOOKS_DIR.glob("*.md") if p.name != "README.md")
    results = [validate_runbook(p) for p in runbooks]

    failures = [r for r in results if r.status != "pass"]
    artifact = {
        "collected_at": _now_iso(),
        "mode": args.mode,
        "required_sections": REQUIRED_SECTIONS,
        "results": [asdict(r) for r in results],
    }

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")

    if failures:
        sys.stderr.write("Runbook validation failed:\n")
        for f in failures:
            sys.stderr.write(f"- {f.file}: missing {', '.join(f.missing_sections)}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
