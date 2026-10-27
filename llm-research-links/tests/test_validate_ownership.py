import unittest

import test_validate_domains as domain_tests


class OwnershipValidationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = domain_tests.DomainValidationTests()
        self.documents = self.fixture.documents()

    def test_owner_requires_library_or_titled_link(self):
        for owner in ("somewhere", "This library", "https://example.org/owner", "[ ](https://example.org/owner)", "[Owner]( )"):
            with self.subTest(owner=owner):
                documents = self.fixture.documents()
                documents["notes/data-platforms/topic.md"] = documents["notes/data-platforms/topic.md"].replace("Canonical owner: this library", f"Canonical owner: {owner}")
                self.assertIn("R-0001: Canonical owner must be this library or a titled Markdown link", self.fixture.diagnostics(documents))

    def test_titled_owner_link_is_valid(self):
        self.documents["notes/data-platforms/topic.md"] = self.documents["notes/data-platforms/topic.md"].replace("Canonical owner: this library", "Canonical owner: [Owner](https://example.org/owner)")
        self.assertEqual([], self.fixture.diagnostics(self.documents))

    def test_owner_link_still_requires_valid_local_target(self):
        self.documents["notes/data-platforms/topic.md"] = self.documents["notes/data-platforms/topic.md"].replace("Canonical owner: this library", "Canonical owner: [Owner](missing.md)")
        self.assertIn("notes/data-platforms/topic.md: broken local link missing.md", self.fixture.diagnostics(self.documents))

    def test_imported_original_id_is_not_library_citation(self):
        self.documents["notes/data-platforms/topic.md"] = self.documents["notes/data-platforms/topic.md"].replace("original ID S-2-01", "original ID R-9999")
        self.assertEqual([], self.fixture.diagnostics(self.documents))

    def test_inline_code_foreign_id_is_not_library_citation(self):
        self.documents["README.md"] = "The upstream finding is `R-9999`; use R-0001 here.\n"
        self.assertEqual([], self.fixture.diagnostics(self.documents))

    def test_unquoted_unknown_id_remains_invalid(self):
        self.documents["README.md"] = "Upstream has `R-9998`. See R-9999.\n"
        self.assertIn("README.md: unknown citation R-9999", self.fixture.diagnostics(self.documents))

    def test_unquoted_unknown_id_after_import_origin_remains_invalid(self):
        self.documents["notes/data-platforms/topic.md"] += "\nSee R-9999.\n"
        self.assertIn("notes/data-platforms/topic.md: unknown citation R-9999", self.fixture.diagnostics(self.documents))


if __name__ == "__main__":
    unittest.main()
