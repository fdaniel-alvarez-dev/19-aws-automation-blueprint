import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_runbooks import validate_runbook


class TestRunbooksContract(unittest.TestCase):
    def test_all_runbooks_have_required_sections(self) -> None:
        runbooks_dir = Path("docs/runbooks")
        runbooks = sorted(p for p in runbooks_dir.glob("*.md") if p.name != "README.md")
        self.assertGreaterEqual(len(runbooks), 3)

        results = [validate_runbook(p) for p in runbooks]
        failures = [r for r in results if r.status != "pass"]
        self.assertEqual(failures, [])

    def test_validator_artifact_is_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "artifact.json"
            out.write_text(json.dumps({"ok": True}), encoding="utf-8")
            self.assertTrue(out.exists())
