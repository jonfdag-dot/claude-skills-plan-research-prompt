import contextlib
from datetime import date
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("research_cli", Path(__file__).parents[1] / "scripts" / "research.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("research module unavailable")
RESEARCH = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RESEARCH
SPEC.loader.exec_module(RESEARCH)

FILES = {
    "sources.md": """# Source register

| ID | Source | Useful for | Authority | Checked | Evidence note |
|---|---|---|---|---|---|
| R-0001 | [Chunking guide](https://example.org/chunking) | Chunk sizing | PRIMARY | 2026-09-01 | [Evidence](notes/rag-search/chunking.md#r-0001) |
| R-0002 | [Graph layout](https://example.org/layout) | Layout choice | SECONDARY | UNKNOWN | [Evidence](notes/data-visualization/layout.md#r-0002) |
""",
    "taxonomy.md": """# Domain taxonomy

Aliases: embeddings → rag-search; graphs → agent-systems or data-visualization by use.

## rag-search

Retrieval.

## data-visualization

Charts.

## agent-systems

Graphs.
""",
    "projects.md": """# Browse by project

## cross-project

- [Graph layout — R-0002](notes/data-visualization/layout.md#r-0002)

## sampletool

- [Chunking guide — R-0001](notes/rag-search/chunking.md#r-0001)
""",
    "topics.md": """# Product topics

| Topic | Entities | Ranking terms | Use for |
|---|---|---|---|
| sampletool/retrieval | project:sampletool, domain:rag-search | chunks, tokens | Retrieval |
| sampletool/broken | project:sampletool, tag:nonexistent | x | Broken |
""",
    "notes/rag-search/index.md": "# rag-search\n\n- [Chunking guide — R-0001](chunking.md#r-0001)\n",
    "notes/data-visualization/index.md": "# data-visualization\n\n- [Graph layout — R-0002](layout.md#r-0002)\n",
}

SECTION = """
## {id}

- Claim: {claim}
- Status: VERIFIED
- Basis: DOCUMENTED
- Applies to: Version 1
- Evidence: Page section
- Access: INSPECTED
- Origin: LIVE; WebFetch 2026-09-01; informed a test
- Recheck: New version
- Corroboration: single-source
- Tags: {tags}
- Projects: {projects}
- Use when: Choose a design
- Canonical owner: this library
"""


def packet(**overrides: object) -> dict:
    record = {
        "Source title": "Embedding migration",
        "Source URL": "https://example.org/migration",
        "Useful for": "Plan migrations",
        "Authority": "FIRST_PARTY",
        "Checked": "2026-10-01",
        "Domain": "embeddings",
        "Topic": "chunking",
        "Claim": "Migration needs delete replay.",
        "Status": "VENDOR CLAIM",
        "Basis": "DOCUMENTED",
        "Applies to": "Version 2",
        "Evidence": "Tutorial section",
        "Access": "INSPECTED",
        "Origin": "LIVE; WebFetch 2026-10-01; informed a test",
        "Recheck": "Tutorial change",
        "Corroboration": "single-source",
        "Tags": ["chunking"],
        "Projects": ["sampletool", "cross-project"],
        "Use when": "Design an embedding migration",
        "Canonical owner": "this library",
    }
    record.update(overrides)
    return record


class ResearchCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.packets = 0
        for name, text in FILES.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        (self.root / "notes/rag-search/chunking.md").write_text("# Chunking\n\nFindings.\n" + SECTION.format(id="R-0001", claim="Chunks of 512 tokens.", tags="chunking, retrieval", projects="sampletool"), encoding="utf-8")
        (self.root / "notes/data-visualization/layout.md").write_text("# Layout\n\nFindings.\n" + SECTION.format(id="R-0002", claim="Force layout.", tags="d3", projects="cross-project"), encoding="utf-8")
        self.assertEqual(self.validate(), [])

    def tearDown(self) -> None:
        self.directory.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = RESEARCH.main(["--root", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def validate(self) -> list[str]:
        loaded = RESEARCH.VALIDATOR.read_snapshot(self.root)
        return loaded if isinstance(loaded, list) else RESEARCH.VALIDATOR.validate(loaded)

    def write_packet(self, payload: object) -> str:
        self.packets += 1
        path = self.root.parent / f"{self.root.name}-packet-{self.packets}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        self.addCleanup(path.unlink)
        return str(path)

    def snapshot(self) -> dict[str, str]:
        return {path.relative_to(self.root).as_posix(): path.read_text(encoding="utf-8") for path in self.root.rglob("*.md")}

    def test_find_requires_one_to_three_entities(self) -> None:
        self.assertEqual(self.run_cli("find", "chunking")[0], 2)
        code, _, err = self.run_cli("find", "--entity", "a", "--entity", "b", "--entity", "c", "--entity", "d")
        self.assertEqual(code, 2)
        self.assertIn("1 to 3 entities", err)

    def test_find_filters_pool_by_alias_and_label(self) -> None:
        code, out, _ = self.run_cli("find", "--entity", "embeddings", "--entity", "project:sampletool")
        self.assertEqual(code, 0)
        self.assertIn("pool: 1 records", out)
        self.assertIn("R-0001", out)
        self.assertNotIn("R-0002", out)

    def test_ambiguous_alias_unions_domains(self) -> None:
        code, out, _ = self.run_cli("find", "--entity", "graphs")
        self.assertEqual(code, 0)
        self.assertIn("domain:data-visualization or domain:agent-systems", out)
        self.assertIn("R-0002", out)

    def test_unknown_entity_suggests_existing_labels(self) -> None:
        code, _, err = self.run_cli("find", "--entity", "chunk")
        self.assertEqual(code, 2)
        self.assertIn("tag:chunking", err)

    def test_terms_rank_inside_pool(self) -> None:
        code, out, _ = self.run_cli("find", "--entity", "rag-search", "force")
        self.assertEqual(code, 0)
        self.assertIn("matches for all terms force: 0", out)
        self.assertIn("drop domain:rag-search: 1 matches in whole library", out)

    def test_any_term_fallback(self) -> None:
        code, out, _ = self.run_cli("find", "--entity", "rag-search", "chunks", "absent")
        self.assertEqual(code, 0)
        self.assertIn("fallback, matches for any term: 1", out)
        self.assertIn("R-0001", out)

    def test_limit_bounds(self) -> None:
        for value in ("0", "26"):
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stderr(io.StringIO()):
                    RESEARCH.main(["--root", str(self.root), "find", "--entity", "rag-search", "--limit", value])
        self.assertEqual(self.run_cli("find", "--entity", "rag-search", "--limit", "25")[0], 0)

    def test_topic_expands_and_counts_toward_limit(self) -> None:
        code, out, _ = self.run_cli("find", "--topic", "sampletool/retrieval")
        self.assertEqual(code, 0)
        self.assertIn("project:sampletool AND domain:rag-search", out)
        self.assertIn("ranked by topic terms chunks, tokens: 1 match", out)
        code, _, err = self.run_cli("find", "--topic", "sampletool/retrieval", "--entity", "tag:d3", "--entity", "tag:chunking")
        self.assertEqual(code, 2)
        self.assertIn("got 4", err)

    def test_topics_check_flags_broken_topic(self) -> None:
        code, out, _ = self.run_cli("topics", "--check")
        self.assertEqual(code, 1)
        self.assertIn("sampletool/broken: BROKEN", out)
        self.assertEqual(self.run_cli("topics", "--project", "sampleapp")[0], 2)

    def test_checked_before_keeps_stale_and_unknown(self) -> None:
        code, out, _ = self.run_cli("find", "--entity", "graphs", "--checked-before", "2026-01-01")
        self.assertIn("R-0002", out)
        code, out, _ = self.run_cli("find", "--entity", "rag-search", "--checked-before", "2026-01-01")
        self.assertIn("pool: 0 records", out)

    def test_show_url_fragment_lists_candidates(self) -> None:
        code, out, _ = self.run_cli("show", "example.org")
        self.assertEqual(code, 0)
        self.assertIn("2 registered URLs contain it", out)

    def test_template_and_audit(self) -> None:
        code, out, _ = self.run_cli("template")
        self.assertEqual(code, 0)
        self.assertIn("Source URL", json.loads(out)["records"][0])
        code, out, _ = self.run_cli("audit", "--project", "sampletool")
        self.assertEqual(code, 0)
        self.assertIn("sampletool", out)

    def test_add_writes_all_homes_and_validates(self) -> None:
        code, out, err = self.run_cli("add", self.write_packet(packet()))
        self.assertEqual(code, 0, err)
        self.assertIn("saved R-0003", out)
        self.assertEqual(self.validate(), [])
        files = self.snapshot()
        self.assertIn("[Embedding migration](https://example.org/migration)", files["sources.md"])
        self.assertIn("## R-0003", files["notes/rag-search/chunking.md"])
        self.assertIn("- Projects: cross-project, sampletool", files["notes/rag-search/chunking.md"])
        self.assertIn("#r-0003", files["notes/rag-search/index.md"])
        self.assertEqual(files["projects.md"].count("#r-0003"), 2)

    def test_add_new_topic_needs_heading(self) -> None:
        code, _, err = self.run_cli("add", self.write_packet(packet(Topic="migrations")))
        self.assertEqual(code, 2)
        self.assertIn("Topic title", err)
        code, _, err = self.run_cli("add", self.write_packet(packet(Topic="migrations", **{"Topic title": "Migrations", "Topic summary": "Migration findings."})))
        self.assertEqual(code, 0, err)
        self.assertEqual(self.validate(), [])

    def test_add_refuses_duplicate_source_and_new_labels(self) -> None:
        before = self.snapshot()
        code, _, err = self.run_cli("add", self.write_packet(packet(**{"Source URL": "https://example.org/chunking/"})))
        self.assertEqual(code, 2)
        self.assertIn("R-0001", err)
        code, _, err = self.run_cli("add", self.write_packet(packet(Tags=["chunkng"])))
        self.assertEqual(code, 2)
        self.assertIn("chunking", err)
        self.assertEqual(self.snapshot(), before)

    def test_add_refuses_integrity_regression_without_writing(self) -> None:
        before = self.snapshot()
        code, _, err = self.run_cli("add", self.write_packet(packet(Status="CONFIRMED")))
        self.assertEqual(code, 2)
        self.assertIn("invalid Status", err)
        self.assertEqual(self.snapshot(), before)

    def test_add_dry_run_writes_nothing(self) -> None:
        before = self.snapshot()
        code, out, _ = self.run_cli("add", "--dry-run", self.write_packet({"records": [packet(), packet(**{"Source URL": "https://example.org/other"})]}))
        self.assertEqual(code, 0)
        self.assertIn("R-0003, R-0004", out)
        self.assertEqual(self.snapshot(), before)

    def test_relabel_updates_section_projects_and_history(self) -> None:
        code, out, err = self.run_cli("relabel", "R-0002", "--add-project", "sampletool", "--remove-project", "cross-project", "--add-tag", "retrieval", "--reason", "layout informs retrieval UI")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.validate(), [])
        files = self.snapshot()
        self.assertIn("- Tags: d3, retrieval", files["notes/data-visualization/layout.md"])
        self.assertIn("Relabeled +tag retrieval, +project sampletool, -project cross-project; layout informs retrieval UI", files["notes/data-visualization/layout.md"])
        cross, sampletool = files["projects.md"].split("## sampletool")
        self.assertNotIn("#r-0002", cross)
        self.assertIn("#r-0002", sampletool)

    def test_relabel_many_ids_in_one_write(self) -> None:
        code, out, err = self.run_cli("relabel", "R-0001", "R-0002", "--add-tag", "retrieval", "--reason", "batch")
        self.assertEqual(code, 0, err)
        self.assertIn("R-0001: labels unchanged", out)
        self.assertIn("relabeled R-0002: +tag retrieval", out)
        self.assertEqual(self.validate(), [])

    def test_relabel_plan_applies_per_record_changes(self) -> None:
        plan = self.write_packet({"R-0001": {"add_tag": ["d3"]}, "R-0002": {"add_project": ["sampletool"]}})
        code, out, err = self.run_cli("relabel", "--plan", plan, "--reason", "batch plan")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.validate(), [])
        files = self.snapshot()
        self.assertIn("- Tags: chunking, d3, retrieval", files["notes/rag-search/chunking.md"])
        self.assertIn("- Projects: cross-project, sampletool", files["notes/data-visualization/layout.md"])
        self.assertEqual(self.run_cli("relabel", "R-0001", "--plan", plan, "--reason", "x")[0], 2)
        bad = self.write_packet({"R-0001": {"add_tags": ["x"]}})
        self.assertEqual(self.run_cli("relabel", "--plan", bad, "--reason", "x")[0], 2)

    def add_second_layout_record(self) -> None:
        extra = packet(**{"Source title": "Radial layout", "Source URL": "https://example.org/radial", "Domain": "data-visualization", "Topic": "layout", "Tags": ["d3"], "Projects": ["cross-project"]})
        self.assertEqual(self.run_cli("add", self.write_packet(extra))[0], 0)

    def test_queue_lists_due_web_sources_in_batches(self) -> None:
        directory = self.root.parent / f"{self.root.name}-batches"
        self.addCleanup(lambda: [path.unlink() for path in directory.glob("*.json")] or directory.rmdir())
        code, out, _ = self.run_cli("queue", "--output-dir", str(directory), "--batch-size", "1")
        self.assertEqual(code, 0)
        self.assertIn("due: 2 records", out)
        batches = sorted(directory.glob("batch-*.json"))
        self.assertEqual(len(batches), 2)
        item = json.loads(batches[0].read_text())[0]
        self.assertEqual({"id", "url", "title", "claim", "authority", "access", "checked", "tranche"}, set(item))

    def test_recheck_advances_checked_only_on_a_successful_read(self) -> None:
        today = date.today().isoformat()
        results = self.write_packet([{"id": "R-0001", "outcome": "inspected", "note": "quoted passage found"}, {"id": "R-0002", "outcome": "dead", "note": "404 twice"}])
        code, out, err = self.run_cli("recheck", results, "--date", today)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.validate(), [])
        files = self.snapshot()
        self.assertIn(f"| PRIMARY | {today} |", files["sources.md"])
        self.assertIn("| SECONDARY | UNKNOWN |", files["sources.md"])
        self.assertNotIn("- Attempted", files["notes/rag-search/chunking.md"])
        self.assertIn(f"- Attempted: {today}", files["notes/data-visualization/layout.md"])
        self.assertIn(f"History: {today} — Recheck by WebFetch: page loaded with on-topic content and a quoted passage consistent with the claim topic; claim details not individually verified; quoted passage found", files["notes/rag-search/chunking.md"])
        self.assertIn("domain unreachable after retry", files["notes/data-visualization/layout.md"])
        code, out, _ = self.run_cli("queue")
        self.assertIn("due: 0 records", out)

    def test_recheck_refuses_unknown_outcome_without_writing(self) -> None:
        before = self.snapshot()
        code, _, err = self.run_cli("recheck", self.write_packet([{"id": "R-0001", "outcome": "fine"}]))
        self.assertEqual(code, 2)
        self.assertIn("outcome", err)
        self.assertEqual(self.snapshot(), before)

    def test_retire_archives_then_removes_every_home(self) -> None:
        self.add_second_layout_record()
        archive = self.root.parent / f"{self.root.name}-archive"
        self.addCleanup(lambda: [path.unlink() for path in archive.glob("*")] or archive.rmdir())
        plan = self.write_packet([{"id": "R-0002", "reason": "dead endpoint, no retained value", "evidence": "404 twice"}])
        code, out, err = self.run_cli("retire", plan, "--archive-dir", str(archive))
        self.assertEqual(code, 0, err)
        self.assertIn("deleted 1 records", out)
        self.assertEqual(self.validate(), [])
        files = self.snapshot()
        self.assertNotIn("R-0002", files["sources.md"])
        self.assertNotIn("## R-0002", files["notes/data-visualization/layout.md"])
        self.assertNotIn("r-0002", files["notes/data-visualization/index.md"])
        self.assertNotIn("r-0002", files["projects.md"])
        entry = json.loads((archive / "retired-records.jsonl").read_text().splitlines()[0])
        self.assertEqual(entry["id"], "R-0002")
        self.assertIn("## R-0002", entry["section"])
        self.assertIn("Graph layout", (archive / "report.md").read_text())

    def test_retire_skips_cited_records_and_dry_run_writes_nothing(self) -> None:
        self.add_second_layout_record()
        archive = self.root.parent / f"{self.root.name}-archive-2"
        (self.root / "reports").mkdir()
        (self.root / "reports" / "decision.md").write_text("# Decision\n\nRelies on R-0001.\n", encoding="utf-8")
        before = self.snapshot()
        plan = self.write_packet([{"id": "R-0001", "reason": "x"}, {"id": "R-0002", "reason": "y"}])
        code, out, _ = self.run_cli("retire", plan, "--archive-dir", str(archive), "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("would delete 1 records; skipped 1", out)
        self.assertIn("skipped R-0001: cited in reports/decision.md", out)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(archive.exists())

    def test_relabel_keeps_one_project(self) -> None:
        code, _, err = self.run_cli("relabel", "R-0002", "--remove-project", "cross-project", "--reason", "x")
        self.assertEqual(code, 2)
        self.assertIn("at least one", err)


if __name__ == "__main__":
    unittest.main()
