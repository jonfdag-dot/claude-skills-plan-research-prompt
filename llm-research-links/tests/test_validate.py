import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("research_validate", Path(__file__).parents[1] / "scripts" / "validate.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("validator module unavailable")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

REGISTER = """# Sources

| ID | Source | Useful for | Authority | Checked | Evidence note |
|---|---|---|---|---|---|
| R-0001 | [Original](https://example.org/spec) | Contract | PRIMARY | 2026-09-01 | [Note](notes/topic.md#r-0001) |
"""
NOTE = """# Topic

## R-0001

- Claim: Earlier documentation supports a narrow contract.
- Status: VERIFIED
- Basis: DOCUMENTED
- Applies to: Historical imported document only.
- Evidence: [Original](https://example.org/spec), section Contract.
- Access: PARTIAL
- Origin: IMPORTED; original ID S-2-01; path /original/register.md; revision UNKNOWN; original checked 2026-09-01.
- Recheck: Fetch the exact current contract before use.
- Corroboration: Single-source; no runtime probe.
- History: 2026-09-12 — Imported without live verification.
"""


class ValidationTests(unittest.TestCase):
    def diagnostics(self, register: str = REGISTER, note: str = NOTE, extra: str = "") -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes").mkdir()
            (root / "sources.md").write_text(register, encoding="utf-8")
            (root / "notes/topic.md").write_text(note, encoding="utf-8")
            if extra:
                (root / "README.md").write_text(extra, encoding="utf-8")
            snapshot = VALIDATOR.read_snapshot(root)
            self.assertIsInstance(snapshot, VALIDATOR.Snapshot)
            return VALIDATOR.validate(snapshot)

    def test_partial_import_is_valid(self):
        self.assertEqual([], self.diagnostics())

    def test_duplicate_source_id(self):
        self.assertIn("R-0001: duplicate source ID", self.diagnostics(REGISTER + REGISTER.splitlines()[-1] + "\n"))

    def test_duplicate_evidence_id(self):
        self.assertIn("R-0001: duplicate evidence ID", self.diagnostics(note=NOTE + NOTE[NOTE.index("## R-0001"):]))

    def test_missing_required_field(self):
        self.assertIn("R-0001: missing field Basis", self.diagnostics(note=NOTE.replace("- Basis: DOCUMENTED\n", "")))

    def test_unknown_citation(self):
        self.assertIn("README.md: unknown citation R-9999", self.diagnostics(extra="See R-9999."))

    def test_missing_local_file(self):
        self.assertTrue(any("broken local link" in item for item in self.diagnostics(extra="[Missing](notes/missing.md)")))

    def test_missing_fragment(self):
        self.assertTrue(any("broken local anchor" in item for item in self.diagnostics(extra="[Wrong](notes/topic.md#absent)")))

    def test_bad_dates(self):
        for value in ("2026-02-30", "2026-9-01", "yesterday"):
            with self.subTest(value=value):
                self.assertTrue(any("invalid Checked date" in item for item in self.diagnostics(REGISTER.replace("2026-09-01", value))))
        self.assertTrue(any("invalid Attempted date" in item for item in self.diagnostics(note=NOTE + "- Attempted: UNKNOWN\n")))
        self.assertTrue(any("invalid History date" in item for item in self.diagnostics(note=NOTE.replace("2026-09-12", "2026-02-30"))))

    def test_bad_enums(self):
        for field, value in (("Status", "VERIFIED"), ("Basis", "DOCUMENTED"), ("Access", "PARTIAL")):
            with self.subTest(field=field):
                self.assertTrue(any(f"invalid {field}" in item for item in self.diagnostics(note=NOTE.replace(f"- {field}: {value}", f"- {field}: MAYBE"))))
        self.assertTrue(any("invalid Authority" in item for item in self.diagnostics(REGISTER.replace("PRIMARY", "BEST"))))

    def test_bad_replacements(self):
        for replacement in ("R-0001", "R-9999", "later"):
            with self.subTest(replacement=replacement):
                self.assertTrue(any("invalid Replacement" in item for item in self.diagnostics(note=NOTE + f"- Replacement: {replacement}\n")))
        self.assertIn("R-0001: superseded record needs Replacement", self.diagnostics(note=NOTE + "- State: superseded\n"))

    def test_import_provenance_required(self):
        self.assertTrue(any("Origin missing revision" in item for item in self.diagnostics(note=NOTE.replace("revision UNKNOWN;", ""))))

    def test_malformed_source_link(self):
        self.assertTrue(any("Source must be" in item for item in self.diagnostics(REGISTER.replace("[Original](https://example.org/spec)", "https://example.org/spec"))))

    def test_checked_unknown_after_failed_fetch(self):
        self.assertEqual([], self.diagnostics(REGISTER.replace("2026-09-01", "UNKNOWN"), NOTE.replace("- Status: VERIFIED", "- Status: UNKNOWN").replace("- Access: PARTIAL", "- Access: UNAVAILABLE").replace("original checked 2026-09-01", "original checked UNKNOWN") + "- Attempted: 2026-09-01\n"))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes").mkdir()
            (root / "sources.md").write_text(REGISTER, encoding="utf-8")
            (root / "notes/topic.md").write_text(NOTE, encoding="utf-8")
            command = [sys.executable, "-B", str(Path(__file__).parents[1] / "scripts/validate.py"), str(root)]
            valid = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
            (root / "notes/topic.md").unlink()
            invalid = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(1, invalid.returncode)
            self.assertIn("missing canonical evidence section", invalid.stdout)


if __name__ == "__main__":
    unittest.main()
