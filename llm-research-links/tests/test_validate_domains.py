from pathlib import Path
import tempfile
import unittest

from test_validate import NOTE, REGISTER, VALIDATOR


class DomainValidationTests(unittest.TestCase):
    def documents(self) -> dict[str, str]:
        return {
            "sources.md": REGISTER.replace("notes/topic.md", "notes/data-platforms/topic.md"),
            "notes/data-platforms/topic.md": NOTE + "- Tags: mcp, sql-mcp\n- Projects: alpha, cross-project\n- Use when: Designing SQL tool contracts.\n- Canonical owner: this library\n",
            "taxonomy.md": "## data-platforms\n\nSQL and database evidence.\n",
            "notes/data-platforms/index.md": "# Data platforms\n\n[Original](topic.md#r-0001)\n",
            "projects.md": "# Projects\n\n## alpha\n\n[Original](notes/data-platforms/topic.md#r-0001)\n\n## cross-project\n\n[Original](notes/data-platforms/topic.md#r-0001)\n",
        }

    def diagnostics(self, documents: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for document, content in documents.items():
                path = root / document
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            snapshot = VALIDATOR.read_snapshot(root)
            self.assertIsInstance(snapshot, VALIDATOR.Snapshot)
            return VALIDATOR.validate(snapshot)

    def test_nested_record_and_indexes_are_valid(self):
        self.assertEqual([], self.diagnostics(self.documents()))

    def test_unknown_domain(self):
        documents = self.documents()
        documents["taxonomy.md"] = "## ui-components\n"
        self.assertIn("notes/data-platforms/topic.md: unknown domain data-platforms", self.diagnostics(documents))

    def test_each_retrieval_field_is_required(self):
        for field in ("Tags", "Projects", "Use when", "Canonical owner"):
            with self.subTest(field=field):
                documents = self.documents()
                documents["notes/data-platforms/topic.md"] = "\n".join(line for line in documents["notes/data-platforms/topic.md"].splitlines() if not line.startswith(f"- {field}:")) + "\n"
                self.assertIn(f"R-0001: missing field {field}", self.diagnostics(documents))

    def test_retrieval_lists_are_normalized_sorted_and_unique(self):
        for value, diagnostic in (("SQL", "comma-separated normalized slugs"), ("sql-mcp, mcp", "unique and alphabetically sorted"), ("mcp, mcp", "unique and alphabetically sorted")):
            with self.subTest(value=value):
                documents = self.documents()
                documents["notes/data-platforms/topic.md"] = documents["notes/data-platforms/topic.md"].replace("Tags: mcp, sql-mcp", f"Tags: {value}")
                self.assertIn(f"R-0001: Tags must be {diagnostic}", self.diagnostics(documents))

    def test_duplicate_canonical_sections_across_paths(self):
        documents = self.documents()
        documents["notes/data-platforms/duplicate.md"] = documents["notes/data-platforms/topic.md"]
        self.assertIn("R-0001: duplicate evidence ID", self.diagnostics(documents))

    def test_old_forwarding_anchor_remains_valid_without_duplicate_evidence(self):
        documents = self.documents()
        documents["notes/topic.md"] = '<a id="r-0001"></a>\n\n[Moved](data-platforms/topic.md#r-0001)\n'
        documents["README.md"] = "[Original location](notes/topic.md#r-0001)\n"
        self.assertEqual([], self.diagnostics(documents))

    def test_index_requires_canonical_target(self):
        documents = self.documents()
        documents["notes/topic.md"] = '<a id="r-0001"></a>\n'
        documents["notes/data-platforms/index.md"] = "[Original](../topic.md#r-0001)\n"
        self.assertIn("notes/data-platforms/index.md: noncanonical index target ../topic.md#r-0001", self.diagnostics(documents))

    def test_broken_nested_anchor(self):
        documents = self.documents()
        documents["notes/data-platforms/index.md"] = "[Original](topic.md#missing)\n"
        self.assertIn("notes/data-platforms/index.md: broken local anchor topic.md#missing", self.diagnostics(documents))

    def test_missing_and_inconsistent_domain_index(self):
        documents = self.documents()
        del documents["notes/data-platforms/index.md"]
        self.assertIn("notes/data-platforms/index.md: missing domain index", self.diagnostics(documents))
        documents["notes/data-platforms/index.md"] = "# Empty\n"
        self.assertIn("notes/data-platforms/index.md: index records do not match domain evidence", self.diagnostics(documents))

    def test_missing_and_inconsistent_project_index(self):
        documents = self.documents()
        del documents["projects.md"]
        self.assertIn("projects.md: missing project index", self.diagnostics(documents))
        documents["projects.md"] = "## different-project\n\n[Original](notes/data-platforms/topic.md#r-0001)\n"
        diagnostics = self.diagnostics(documents)
        self.assertIn("projects.md: index records do not match project alpha", diagnostics)
        self.assertIn("projects.md: index records do not match project different-project", diagnostics)

    def test_stale_domain_index(self):
        documents = self.documents()
        documents["taxonomy.md"] += "\n## ui-components\n"
        documents["notes/ui-components/index.md"] = "[Original](../data-platforms/topic.md#r-0001)\n"
        diagnostics = self.diagnostics(documents)
        self.assertIn("notes/ui-components/index.md: domain index has no canonical evidence", diagnostics)
        self.assertIn("notes/ui-components/index.md: index records do not match domain evidence", diagnostics)

    def test_duplicate_index_links(self):
        documents = self.documents()
        documents["notes/data-platforms/index.md"] += "[Again](topic.md#r-0001)\n"
        documents["projects.md"] += "[Again](notes/data-platforms/topic.md#r-0001)\n"
        diagnostics = self.diagnostics(documents)
        self.assertIn("notes/data-platforms/index.md: index records do not match domain evidence", diagnostics)
        self.assertIn("projects.md: index records do not match project cross-project", diagnostics)

    def test_register_and_domain_index_sorting(self):
        documents = self.documents()
        row = documents["sources.md"].splitlines()[-1]
        second_row = row.replace("R-0001", "R-0002").replace("r-0001", "r-0002").replace("[Original]", "[Alpha]")
        documents["sources.md"] = documents["sources.md"].replace(row, second_row + "\n" + row)
        second_note = documents["notes/data-platforms/topic.md"].replace("R-0001", "R-0002")
        documents["notes/data-platforms/topic.md"] += second_note
        documents["notes/data-platforms/index.md"] += "[Alpha](topic.md#r-0002)\n"
        diagnostics = self.diagnostics(documents)
        self.assertIn("sources.md: source IDs must be sorted numerically", diagnostics)
        self.assertIn("notes/data-platforms/index.md: index records must sort by topic, source title, then ID", diagnostics)

    def test_replacement_cycle_in_nested_records(self):
        documents = self.documents()
        documents["sources.md"] += documents["sources.md"].splitlines()[-1].replace("R-0001", "R-0002").replace("r-0001", "r-0002") + "\n"
        second_note = documents["notes/data-platforms/topic.md"].replace("R-0001", "R-0002")
        documents["notes/data-platforms/topic.md"] += "- State: superseded\n- Replacement: R-0002\n" + second_note + "- State: superseded\n- Replacement: R-0001\n"
        self.assertIn("R-0001: Replacement cycle", self.diagnostics(documents))


if __name__ == "__main__":
    unittest.main()
