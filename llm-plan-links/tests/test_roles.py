import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "roles.py"
SPEC = importlib.util.spec_from_file_location("roles", SCRIPT)
ROLES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ROLES)


def row(role="active work", target="2026-10-04-active-work.md", section="Current work", state="in_progress", priority="now", updated="2026-10-04", summary="Finish the requested work."):
    return dict(role=role, target=target, section=section, state=state, priority=priority, updated=updated, summary=summary)


def index_text(rows, prefix=None):
    lines = list(prefix or ["# Plan roles: example", "", "COUNTS", "CONTINUATION", ""])
    for section in ROLES.SECTIONS:
        lines.extend([f"## {section}", "", "| " + " | ".join(ROLES.COLUMNS) + " |", "|---|---|---|---|---|---|"])
        for entry in rows:
            if entry["section"] == section:
                cells = [entry["role"], entry["state"], entry["priority"], entry["updated"], f"[Main plan]({entry['target']})", entry["summary"]]
                lines.append("| " + " | ".join(cell.replace("|", r"\|") for cell in cells) + " |")
                entry["line"] = len(lines)
        lines.append("")
    lines.extend(["## Directory meanings", "", "- Project folder root: active plans."])
    return ("\n".join(lines) + "\n").replace("COUNTS", ROLES.counts_line(rows)).replace("CONTINUATION", ROLES.continuation_line(rows))


def plan_text(status="in_progress", successor=None, created="2026-10-04"):
    fields = f"status: {status}\ncreated: {created}\ncompleted: {'2026-10-04' if status == 'complete' else ''}\n"
    if successor is not None:
        fields += f"succeeded_by: {successor}\n"
    return "---\n" + fields + "---\n\n# Work\n\nDeliver the requested result.\n\n## Status\n\nCurrent milestone: M2.\n\nNext: Run the acceptance check.\n"


class RolesReaderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "library"
        self.project = self.root / "example"
        self.project.mkdir(parents=True)
        self.source = self.base / "source"
        self.source.mkdir()
        for directory in (self.root, self.source):
            for name in ("AGENTS.md", "CLAUDE.md", "README.md"):
                (directory / name).write_text(f"Read {name}.\n", encoding="utf-8")
        self.registry = {"projects": [dict(id="example", source_root=str(self.source), plan_directory="example", live_in_complete=[])]}
        self.save_registry()
        self.plan = self.write_plan("2026-10-04-active-work.md")
        self.index = self.project / "ROLES.md"
        self.write_index([row()])

    def save_registry(self):
        (self.root / "projects.json").write_text(json.dumps(self.registry), encoding="utf-8")

    def write_index(self, rows, project=None, prefix=None):
        path = (project or self.project) / "ROLES.md"
        path.write_text(index_text(rows, prefix), encoding="utf-8")
        return path

    def write_plan(self, relative, status="in_progress", successor=None, project=None, created="2026-10-04"):
        path = (project or self.project) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(plan_text(status, successor, created), encoding="utf-8")
        return path

    def add_project(self, name):
        project = self.root / name
        project.mkdir()
        source = self.base / f"{name}-source"
        source.mkdir()
        for instruction in ("AGENTS.md", "CLAUDE.md"):
            (source / instruction).write_text("Read this instruction.\n", encoding="utf-8")
        self.registry["projects"].append(dict(id=name, source_root=str(source), plan_directory=name, live_in_complete=[]))
        self.save_registry()
        self.write_index([], project)
        return project, source

    def cli(self, *arguments, code=0):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--root", str(self.root), *arguments], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def resolve(self, role="active work", runtime="codex"):
        return json.loads(self.cli("resolve", "example", "--role", role, "--runtime", runtime, "--json").stdout)

    def snapshot(self):
        return {str(path.relative_to(self.base)): (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns, path.stat().st_mode) for path in self.base.rglob("*") if path.is_file()}

    def test_parser_fields_counts_and_empty_sections(self):
        rows = ROLES.read_index(self.index)
        self.assertEqual(rows, [dict(row(), line=10)])
        self.assertEqual(ROLES.index_counts(rows), dict(current=1, references=0, deferred=0, superseded=0, complete=0))
        self.assertEqual(ROLES.counts_line(rows), "Counts: current=1; references=0; deferred=0; superseded=0; complete=0.")
        self.assertEqual(ROLES.continuation_line(rows), "Continuation: 0 current/reference entries beyond line 100.")

    def test_parser_escaped_pipe_in_summary(self):
        self.write_index([row(summary="Choose A | B after review.")])
        self.assertEqual(ROLES.read_index(self.index)[0]["summary"], "Choose A | B after review.")

    def test_parser_rejects_malformed_indexes(self):
        original = self.index.read_text(encoding="utf-8")
        mutations = {
            "missing section": original.replace("## Deferred", "## Missing"),
            "wrong columns": original.replace("| Brief summary |", "| Notes |", 1),
            "missing separator": original.replace("|---|---|---|---|---|---|", "|---|---|", 1),
            "two links": original.replace("[Main plan](2026-10-04-active-work.md)", "[Main](first.md), [Other](second.md)"),
            "bare target": original.replace("[Main plan](2026-10-04-active-work.md)", "`2026-10-04-active-work.md`"),
            "invalid date": original.replace("| 2026-10-04 |", "| 2026-02-30 |"),
            "invalid state": original.replace("| in_progress |", "| done |"),
            "invalid priority": original.replace("| now |", "| urgent |"),
            "missing cell": original.replace("| Finish the requested work. |", "|"),
            "outside table": original + "\n| stray | row | now | UNKNOWN | [Plan](file.md) | Bad row. |\n",
            "separated row": original.replace("| active work |", "\n| active work |"),
            "missing leading pipe": original.replace("| active work |", "active work |"),
            "missing table": original.replace("## Complete\n\n| Role | State | Priority | Updated | Plan / folder | Brief summary |\n|---|---|---|---|---|---|", "## Complete"),
            "duplicate section": original + "\n## Complete\n\n| Role | State | Priority | Updated | Plan / folder | Brief summary |\n|---|---|---|---|---|---|\n",
        }
        for name, text in mutations.items():
            with self.subTest(name=name):
                self.index.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    ROLES.read_index(self.index)

    def test_sort_priority_then_recency_and_unknown_last(self):
        entries = [row("unknown", updated="UNKNOWN"), row("old", updated="2026-09-01"), row("new next", priority="next"), row("new"), row("alpha", updated="2026-09-01")]
        self.assertEqual([entry["role"] for entry in sorted(entries, key=ROLES.row_sort_key)], ["new", "alpha", "old", "unknown", "new next"])
        for entry in entries:
            entry["section"] = "Current references"
            entry["priority"] = "-"
        self.assertEqual([entry["role"] for entry in sorted(entries, key=ROLES.row_sort_key)], ["new", "new next", "alpha", "old", "unknown"])

    def test_head_exact_physical_boundary_and_continuation(self):
        entries = [row(f"role {number:03d}") for number in range(105)]
        self.write_index(entries)
        expected = "".join(self.index.read_text(encoding="utf-8").splitlines(keepends=True)[:100])
        output = self.cli("head", "example").stdout
        self.assertEqual(output, expected)
        self.assertEqual(len(output.splitlines()), 100)
        self.assertIn("Continuation: 14 current/reference entries beyond line 100.", output)
        self.assertIn("role 090", output)
        self.assertNotIn("role 091", output)

    def test_head_never_invokes_full_index_parser(self):
        self.index.write_text("line\n" * 100 + "INVALID AFTER BOUNDARY\n", encoding="utf-8")
        with patch.object(ROLES, "read_index", side_effect=AssertionError("read beyond head")):
            with patch("sys.stdout") as output:
                self.assertEqual(ROLES.main(["--root", str(self.root), "head", "example"]), 0)
        output.write.assert_called_once_with("line\n" * 100)

    def test_short_head_returns_file_exactly(self):
        self.assertEqual(self.cli("head", "example").stdout, self.index.read_text(encoding="utf-8"))

    def test_pagination_returns_remaining_rows_and_final_null(self):
        self.write_index([row(f"role {number:03d}") for number in range(105)])
        first = json.loads(self.cli("list", "example", "--json").stdout)
        self.assertEqual((len(first["entries"]), first["total"], first["next_offset"]), (100, 105, 100))
        second = json.loads(self.cli("list", "example", "--offset", "100", "--limit", "7", "--json").stdout)
        self.assertEqual((len(second["entries"]), second["total"], second["next_offset"]), (5, 105, None))
        beyond = json.loads(self.cli("list", "example", "--offset", "500", "--json").stdout)
        self.assertEqual(beyond, dict(entries=[], total=105, next_offset=None))

    def test_list_section_and_direct_text_paths(self):
        self.write_index([row(), row("reference", section="Current references", state="reference", priority="-")])
        result = json.loads(self.cli("list", "example", "--section", "references", "--json").stdout)
        self.assertEqual([entry["role"] for entry in result["entries"]], ["reference"])
        self.assertIn(str(self.plan), self.cli("list", "example").stdout)
        empty = json.loads(self.cli("list", "example", "--section", "deferred", "--json").stdout)
        self.assertEqual(empty, dict(entries=[], total=0, next_offset=None))

    def test_resolve_case_insensitive_role_runtime_and_next_action(self):
        result = self.resolve("ACTIVE WORK")
        self.assertEqual(result["main_plan"], str(self.plan))
        self.assertEqual(result["plan_folder"], str(self.project))
        self.assertEqual(result["state"], "in_progress")
        self.assertEqual(result["next_action"], "Run the acceptance check.")
        self.assertEqual(result["reading_entrypoints"], [str(self.source / "AGENTS.md"), str(self.source / "CLAUDE.md"), str(self.root / "AGENTS.md"), str(self.root / "README.md"), str(self.index), str(self.plan)])
        self.assertEqual(result["missing_source_instructions"], [])
        self.assertEqual(self.resolve(runtime="claude")["reading_entrypoints"][:2], [str(self.source / "CLAUDE.md"), str(self.source / "AGENTS.md")])
        text = self.cli("resolve", "example", "--role", "active work").stdout
        for path in result["reading_entrypoints"]:
            self.assertIn(path, text)

    def test_missing_native_source_instruction_uses_existing_counterpart(self):
        for runtime, missing, fallback in (("codex", "AGENTS.md", "CLAUDE.md"), ("claude", "CLAUDE.md", "AGENTS.md")):
            with self.subTest(runtime=runtime):
                (self.source / missing).unlink()
                result = self.resolve(runtime=runtime)
                self.assertEqual(result["reading_entrypoints"][0], str(self.source / fallback))
                self.assertNotIn(str(self.source / missing), result["reading_entrypoints"])
                self.assertEqual(result["missing_source_instructions"], [])
                self.assertTrue(all(Path(path).is_file() for path in result["reading_entrypoints"]))
                (self.source / missing).write_text("Read this instruction.\n", encoding="utf-8")

    def test_only_native_source_instruction_is_returned(self):
        (self.source / "CLAUDE.md").unlink()
        result = self.resolve()
        self.assertEqual(result["reading_entrypoints"][0], str(self.source / "AGENTS.md"))
        self.assertNotIn(str(self.source / "CLAUDE.md"), result["reading_entrypoints"])
        self.assertEqual(result["missing_source_instructions"], [])

    def test_absent_source_instructions_are_explicit_metadata(self):
        for name in ("AGENTS.md", "CLAUDE.md"):
            (self.source / name).unlink()
        result = self.resolve()
        missing = [str(self.source / "AGENTS.md"), str(self.source / "CLAUDE.md")]
        self.assertEqual(result["missing_source_instructions"], missing)
        self.assertFalse(set(missing) & set(result["reading_entrypoints"]))
        self.assertTrue(all(Path(path).is_file() for path in result["reading_entrypoints"]))
        text = self.cli("resolve", "example", "--role", "active work").stdout
        self.assertIn("Missing source instructions: " + ", ".join(missing), text)
        self.assertNotIn("Read: " + missing[0], text)

    def test_missing_library_reading_entrypoints_fail(self):
        for runtime, missing in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md"), ("codex", "README.md")):
            with self.subTest(runtime=runtime, missing=missing):
                (self.root / missing).unlink()
                result = self.cli("resolve", "example", "--role", "active work", "--runtime", runtime, "--json", code=1)
                self.assertIn(f"Missing library reading entrypoint: {self.root / missing}", result.stderr)
                self.assertEqual(result.stdout, "")
                (self.root / missing).write_text("Read this entrypoint.\n", encoding="utf-8")

    def test_resolve_prefers_current_alias_over_historical_alias(self):
        historic = self.write_plan("complete/2026-01-01-old.md", "complete")
        self.write_index([row(), row("ACTIVE WORK", str(historic.relative_to(self.project)), "Complete", "complete", "-")])
        self.assertEqual(self.resolve()["main_plan"], str(self.plan))

    def test_resolve_rejects_ambiguous_current_and_historical_aliases(self):
        for section, state, priority in (("Current work", "in_progress", "now"), ("Complete", "complete", "-")):
            with self.subTest(section=section):
                self.write_index([row(section=section, state=state, priority=priority), row("ACTIVE WORK", section=section, state=state, priority=priority)])
                self.assertIn("Ambiguous role", self.cli("resolve", "example", "--role", "active work", code=1).stderr)

    def test_resolve_exact_role_does_not_fuzzy_match(self):
        self.assertIn("Unknown role", self.cli("resolve", "example", "--role", "active", code=1).stderr)

    def test_bundle_directory_and_explicit_legacy_entrypoints(self):
        bundle = self.write_plan("2026-10-04-bundle/plan.md")
        readme = bundle.parent / "README.md"
        readme.write_text("Start with the plan.\n", encoding="utf-8")
        legacy = self.write_plan("2026-08-01-legacy/01-plan.md", created="2026-08-01")
        self.write_index([row("bundle", "2026-10-04-bundle/"), row("legacy", str(legacy.relative_to(self.project)))])
        result = self.resolve("bundle")
        self.assertEqual(result["main_plan"], str(bundle))
        self.assertEqual(result["plan_folder"], str(bundle.parent))
        self.assertIn(str(readme), result["reading_entrypoints"])
        self.assertEqual(self.resolve("legacy")["main_plan"], str(legacy))

    def add_shared_bundle(self, coordinator="coordinator", combined=False):
        project, source = self.add_project(coordinator)
        directory = "2026-10-18-shared-migration"
        bundle = self.root / directory
        bundle.mkdir()
        plan = self.write_plan("claude.md" if combined else "plan.md", project=bundle, created="2026-10-18")
        if not combined:
            (bundle / "README.md").write_text("Read the shared migration plan.\n", encoding="utf-8")
        self.registry["schema_version"] = 1
        self.registry["temporary_shared_bundles"] = [dict(directory=directory, coordinator_project=coordinator, purpose="Temporary migration workspace.")]
        if combined:
            self.registry["temporary_shared_bundles"][0]["combined_entrypoint"] = plan.name
        self.save_registry()
        self.write_index([row("shared migration", f"../{directory}/{plan.name}", section="Current references", state="reference", priority="-")], project)
        self.write_index([row(target=f"../{directory}/{plan.name}")])
        return bundle, project, source, plan

    def test_shared_combined_entrypoint_resolves_file_and_successor(self):
        bundle, coordinator, _, plan = self.add_shared_bundle(combined=True)
        old = self.write_plan("complete/2026-10-04-old.md", "superseded", f"../{bundle.name}/claude.md")
        for target in (f"../{bundle.name}/claude.md", str(old.relative_to(self.project))):
            self.write_index([row(target=target)])
            for runtime in ("codex", "claude"):
                with self.subTest(target=target, runtime=runtime):
                    result = self.resolve(runtime=runtime)
                    self.assertEqual(result["main_plan"], str(plan))
                    self.assertEqual(result["reading_entrypoints"].count(str(plan)), 1)
                    self.assertNotIn(str(bundle / "README.md"), result["reading_entrypoints"])
                    self.assertIn(str(coordinator / "ROLES.md"), result["reading_entrypoints"])
                    self.assertTrue(all(Path(path).is_file() for path in result["reading_entrypoints"]))

    def test_shared_combined_entrypoint_rejects_missing_file_and_outside_symlink(self):
        _, _, _, plan = self.add_shared_bundle(combined=True)
        plan.unlink()
        self.assertIn("Missing target", self.cli("resolve", "example", "--role", "active work", code=1).stderr)
        outside = self.base / "private.md"
        outside.write_text("PRIVATE SENTINEL", encoding="utf-8")
        plan.symlink_to(outside)
        result = self.cli("resolve", "example", "--role", "active work", code=1)
        self.assertIn("Unsafe", result.stderr)
        self.assertNotIn("PRIVATE SENTINEL", result.stdout + result.stderr)

    def test_shared_role_preserves_source_project_and_adds_coordinator_reading(self):
        bundle, coordinator, source, plan = self.add_shared_bundle()
        for runtime, instruction in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(runtime=runtime):
                result = self.resolve(runtime=runtime)
                self.assertEqual(result["project"], "example")
                self.assertEqual(result["coordinator_project"], "coordinator")
                self.assertEqual(result["main_plan"], str(plan))
                self.assertEqual(result["plan_folder"], str(bundle))
                for path in (self.source / instruction, source / instruction, self.index, coordinator / "ROLES.md", bundle / "README.md", self.root / instruction, plan):
                    self.assertIn(str(path), result["reading_entrypoints"])
                self.assertTrue(all(Path(path).is_file() for path in result["reading_entrypoints"]))
                self.assertFalse((bundle / "ROLES.md").exists())

    def test_coordinator_can_resolve_its_shared_reference(self):
        bundle, coordinator, source, plan = self.add_shared_bundle()
        result = json.loads(self.cli("resolve", "coordinator", "--role", "shared migration", "--json").stdout)
        self.assertEqual(result["project"], "coordinator")
        self.assertEqual(result["state"], "reference")
        self.assertEqual(result["main_plan"], str(plan))
        self.assertIn(str(source / "AGENTS.md"), result["reading_entrypoints"])
        self.assertIn(str(coordinator / "ROLES.md"), result["reading_entrypoints"])
        self.assertIn(str(bundle / "README.md"), result["reading_entrypoints"])

    def test_shared_resolution_handles_coordinator_index_with_local_plans(self):
        bundle, coordinator, _, plan = self.add_shared_bundle()
        local_plan = self.write_plan("2026-10-04-coordinator-work.md", project=coordinator)
        self.write_index([
            row("coordinator work", local_plan.name),
            row("shared migration", f"../{bundle.name}/plan.md", section="Current references", state="reference", priority="-"),
        ], coordinator)
        for project, role in (("example", "active work"), ("coordinator", "shared migration")):
            with self.subTest(project=project):
                result = json.loads(self.cli("resolve", project, "--role", role, "--json").stdout)
                self.assertEqual(result["main_plan"], str(plan))
                self.assertEqual(result["project"], project)
                self.assertEqual(result["coordinator_project"], "coordinator")
                self.assertIn(str(coordinator / "ROLES.md"), result["reading_entrypoints"])

    def test_shared_role_keeps_source_instruction_absence_explicit(self):
        _, _, source, _ = self.add_shared_bundle()
        for name in ("AGENTS.md", "CLAUDE.md"):
            (self.source / name).unlink()
        result = self.resolve()
        self.assertEqual(result["missing_source_instructions"], [str(self.source / name) for name in ("AGENTS.md", "CLAUDE.md")])
        self.assertIn(str(source / "AGENTS.md"), result["reading_entrypoints"])

    def test_normal_resolution_does_not_add_coordinator_metadata(self):
        self.assertNotIn("coordinator_project", self.resolve())

    def test_shared_role_rejects_undeclared_siblings_and_traversal(self):
        bundle, _, _, _ = self.add_shared_bundle()
        target = f"../{bundle.name}/plan.md"
        for value in (f"../{bundle.name}/../{bundle.name}/plan.md", f"../../library/{bundle.name}/plan.md"):
            with self.subTest(target=value):
                self.write_index([row(target=value)])
                self.assertIn("Unsafe", self.cli("resolve", "example", "--role", "active work", code=1).stderr)
        self.registry.pop("temporary_shared_bundles")
        self.save_registry()
        self.write_index([row(target=target)])
        self.assertIn("Unsafe", self.cli("resolve", "example", "--role", "active work", code=1).stderr)

    def test_shared_role_rejects_missing_readme(self):
        bundle, _, _, _ = self.add_shared_bundle()
        (bundle / "README.md").unlink()
        self.assertIn("Missing target", self.cli("resolve", "example", "--role", "active work", code=1).stderr)

    def test_shared_role_rejects_outside_symlinks_without_reading(self):
        bundle, _, _, _ = self.add_shared_bundle()
        outside = self.base / "private.md"
        outside.write_text("PRIVATE SENTINEL", encoding="utf-8")
        for name in ("plan.md", "README.md"):
            with self.subTest(name=name):
                path = bundle / name
                original = path.read_text(encoding="utf-8")
                path.unlink()
                path.symlink_to(outside)
                result = self.cli("resolve", "example", "--role", "active work", code=1)
                self.assertIn("Unsafe", result.stderr)
                self.assertNotIn("PRIVATE SENTINEL", result.stdout + result.stderr)
                path.unlink()
                path.write_text(original, encoding="utf-8")

    def test_successor_can_resolve_to_a_declared_shared_plan(self):
        bundle, _, _, final = self.add_shared_bundle()
        old = self.write_plan("complete/2026-10-04-old.md", "superseded", f"../{bundle.name}/plan.md")
        self.write_index([row(target=str(old.relative_to(self.project)), section="Superseded", state="superseded", priority="-")])
        result = self.resolve()
        self.assertEqual(result["successor_chain"], [str(old), str(final)])
        self.assertEqual(result["project"], "example")
        self.assertEqual(result["coordinator_project"], "coordinator")

    def test_directory_navigation_is_not_a_plan(self):
        self.write_index([row("active plans", "./", "Current references", "reference", "-")])
        self.assertEqual(ROLES.read_index(self.index)[0]["target"], "./")
        self.assertIn("not a plan entrypoint", self.cli("resolve", "example", "--role", "active plans", code=1).stderr)

    def test_legacy_bundle_requires_explicit_main_file(self):
        self.write_plan("2026-08-01-legacy/01-plan.md", created="2026-08-01")
        self.write_index([row(target="2026-08-01-legacy/")])
        self.assertIn("explicit main plan", self.cli("resolve", "example", "--role", "active work", code=1).stderr)

    def test_official_successor_chain_and_owner_rootfiles(self):
        other, source = self.add_project("other")
        final = self.write_plan("2026-10-04-final/plan.md", project=other)
        self.write_index([row("new work", "2026-10-04-final/plan.md", state="blocked", summary="Wait for the named dependency.")], other)
        middle = self.write_plan("complete/2026-09-01-middle.md", "complete", "../other/2026-10-04-final/plan.md")
        old = self.write_plan("complete/2026-08-01-old.md", "superseded", str(middle.relative_to(self.project)))
        self.write_index([row("old work", str(old.relative_to(self.project)), "Superseded", "superseded", "-")])
        result = self.resolve("old work")
        self.assertEqual(result["main_plan"], str(final))
        self.assertEqual(result["successor_chain"], [str(old), str(middle), str(final)])
        self.assertEqual(result["project"], "other")
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(result["summary"], "Wait for the named dependency.")
        self.assertIn(str(other / "ROLES.md"), result["reading_entrypoints"])
        self.assertIn(str(source / "AGENTS.md"), result["reading_entrypoints"])

    def test_partial_replacement_retains_in_progress_carrier(self):
        self.plan.write_text(plan_text(successor="future-missing-replacement.md"), encoding="utf-8")
        result = self.resolve()
        self.assertEqual(result["main_plan"], str(self.plan))
        self.assertEqual(result["successor_chain"], [str(self.plan)])
        self.assertEqual(result["recorded_successor"], "future-missing-replacement.md")
        self.assertIn("Recorded successor: future-missing-replacement.md", self.cli("resolve", "example", "--role", "active work").stdout)

    def test_designated_live_in_complete_is_reference(self):
        live = self.write_plan("complete/2026-07-01-live.md", created="2026-07-01")
        self.registry["projects"][0]["live_in_complete"].append(str(live.relative_to(self.project)))
        self.save_registry()
        self.write_index([row(target=str(live.relative_to(self.project)), section="Current references", state="reference", priority="-")])
        self.assertEqual(self.resolve()["state"], "reference")

    def test_undesignated_live_in_complete_fails(self):
        live = self.write_plan("complete/2026-07-01-live.md", created="2026-07-01")
        self.write_index([row(target=str(live.relative_to(self.project)))])
        self.assertIn("Undesignated live", self.cli("resolve", "example", "--role", "active work", code=1).stderr)

    def test_deferred_and_complete_resolution_keep_historical_state(self):
        for relative, status, expected in (("complete/deferred/2026-08-01-later.md", "in_progress", "deferred"), ("complete/2026-08-01-done.md", "complete", "complete")):
            with self.subTest(expected=expected):
                self.write_plan(relative, status)
                self.write_index([row(target=relative, section=expected.capitalize(), state=expected, priority="-")])
                self.assertEqual(self.resolve()["state"], expected)

    def test_percent_encoded_legacy_path(self):
        target = self.write_plan("legacy notes/01-plan.md", created="2026-08-01")
        self.write_index([row(target="legacy%20notes/01-plan.md")])
        self.assertEqual(ROLES.read_index(self.index)[0]["target"], "legacy notes/01-plan.md")
        self.assertEqual(self.resolve()["main_plan"], str(target))

    def test_percent_encoding_is_decoded_once(self):
        target = self.write_plan("literal%20notes/01-plan.md", created="2026-08-01")
        self.write_index([row(target="literal%2520notes/01-plan.md")])
        self.assertEqual(self.resolve()["main_plan"], str(target))

    def test_missing_and_cyclic_successors_fail(self):
        for successor, fragment in (("missing.md", "Missing target"), ("2026-10-04-active-work.md", "Successor cycle"), (None, "no successor")):
            with self.subTest(successor=successor):
                self.plan.write_text(plan_text("superseded", successor), encoding="utf-8")
                self.assertIn(fragment, self.cli("resolve", "example", "--role", "active work", code=1).stderr)

    def test_multihop_cycle_fails(self):
        self.plan.write_text(plan_text("superseded", "complete/2026-01-01-old.md"), encoding="utf-8")
        self.write_plan("complete/2026-01-01-old.md", "superseded", "2026-10-04-active-work.md")
        self.assertIn("Successor cycle", self.cli("resolve", "example", "--role", "active work", code=1).stderr)

    def test_unsafe_targets_and_successors_fail(self):
        targets = ("../../source/AGENTS.md", "/etc/passwd", "https://example.com/plan.md", "a/../2026-10-04-active-work.md", "..%2F..%2Fsource/AGENTS.md", "../unknown/plan.md")
        for target in targets:
            for successor in (False, True):
                with self.subTest(target=target, successor=successor):
                    self.plan.write_text(plan_text("superseded", target) if successor else plan_text(), encoding="utf-8")
                    self.write_index([row(target="2026-10-04-active-work.md" if successor else target)])
                    self.assertIn("Unsafe", self.cli("resolve", "example", "--role", "active work", code=1).stderr)

    def test_unsafe_symlinks_fail_before_reading_content(self):
        outside = self.base / "outside.md"
        outside.write_text("PRIVATE SENTINEL", encoding="utf-8")
        link = self.project / "escaped.md"
        link.symlink_to(outside)
        self.write_index([row(target="escaped.md")])
        result = self.cli("resolve", "example", "--role", "active work", code=1)
        self.assertIn("Unsafe", result.stderr)
        self.assertNotIn("PRIVATE SENTINEL", result.stdout + result.stderr)
        self.assertIn("Unsafe", self.cli("list", "example", "--json", code=1).stderr)

    def test_unsafe_index_symlink_fails_for_head(self):
        self.index.unlink()
        self.index.symlink_to(self.source / "AGENTS.md")
        self.assertIn("Unsafe", self.cli("head", "example", code=1).stderr)

    def test_project_traversal_unknown_projects_and_limits(self):
        for project in ("../example", "unknown", str(self.project)):
            with self.subTest(project=project):
                self.assertIn("Unknown or unsafe project", self.cli("head", project, code=1).stderr)
        for flag, value in (("--offset", "-1"), ("--offset", "x"), ("--limit", "0"), ("--limit", "101")):
            with self.subTest(flag=flag, value=value):
                self.cli("list", "example", flag, value, code=2)

    def test_malformed_frontmatter_fails_without_traceback(self):
        for text in ("# Not a plan\n", "---\nstatus: in_progress\n", "---\nstatus: invalid\n---\n"):
            with self.subTest(text=text):
                self.plan.write_text(text, encoding="utf-8")
                result = self.cli("resolve", "example", "--role", "active work", code=1)
                self.assertNotIn("Traceback", result.stderr)

    def test_commands_preserve_all_fixture_files_and_metadata(self):
        before = self.snapshot()
        self.cli("head", "example")
        self.cli("list", "example", "--json")
        self.cli("resolve", "example", "--role", "active work", "--json")
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
