from pathlib import Path
import tempfile
import unittest

import test_validate as baseline


class LineLinkValidationTests(unittest.TestCase):
    def diagnostics(self, target: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "notes").mkdir()
            (root / "sources.md").write_text(baseline.REGISTER, encoding="utf-8")
            (root / "notes/topic.md").write_text(baseline.NOTE, encoding="utf-8")
            (root / "README.md").write_text(f"[Owner]({target.format(root=root)})\n", encoding="utf-8")
            snapshot = baseline.VALIDATOR.read_snapshot(root)
            self.assertIsInstance(snapshot, baseline.VALIDATOR.Snapshot)
            return baseline.VALIDATOR.validate(snapshot)

    def test_absolute_native_line_pointer_resolves_base_file(self):
        self.assertEqual([], self.diagnostics("{root}/notes/topic.md:5"))

    def test_native_line_pointer_preserves_fragment_validation(self):
        self.assertEqual([], self.diagnostics("{root}/notes/topic.md:5#r-0001"))
        self.assertTrue(any("broken local anchor" in error for error in self.diagnostics("{root}/notes/topic.md:5#missing")))

    def test_native_line_pointer_rejects_missing_base_file(self):
        self.assertTrue(any("broken local link" in error for error in self.diagnostics("{root}/notes/missing.md:5")))

    def test_zero_and_negative_line_pointers_are_invalid(self):
        for line in ("0", "-5"):
            with self.subTest(line=line):
                self.assertTrue(any("local line pointer must be positive" in error for error in self.diagnostics("{root}/notes/topic.md:" + line)))

    def test_http_port_url_is_unchanged(self):
        self.assertEqual([], self.diagnostics("https://example.org:8443/spec.md#contract"))
        self.assertEqual(("/spec.md", "contract"), baseline.VALIDATOR.target_path("/library", "README.md", "https://example.org:8443/spec.md#contract"))

    def test_http_path_colon_is_not_a_local_line_pointer(self):
        self.assertEqual(("/spec.md:55", "contract"), baseline.VALIDATOR.target_path("/library", "README.md", "https://example.org:8443/spec.md:55#contract"))
        self.assertEqual([], self.diagnostics("https://example.org:8443/spec.md:0"))


if __name__ == "__main__":
    unittest.main()
