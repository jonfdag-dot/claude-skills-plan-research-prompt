import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("plan_validator", Path(__file__).resolve().parents[1] / "scripts/validate.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

PREMISE = "This plan exercises the validator, and it is done when the assertion holds.\n"
SECTIONS = "\n## Decisions\n\n## Discoveries\n\n## Status\n"


def plan_text(status, created, completed, body=PREMISE, extra=""):
    return f"---\nstatus: {status}\ncreated: {created}\ncompleted: {completed}\n{extra}---\n\n# Title\n\n{body}"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PlanLibraryValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "library"
        self.source_root = self.base / "source-repo"
        self.source_root.mkdir()
        self.project = self.root / "example"
        for subdirectory in ("complete/deferred", "eval-runs", "reviews", ".session/runtime-inbox", "archive"):
            (self.project / subdirectory).mkdir(parents=True)
        for folder in ("migration", "scripts", "tests"):
            (self.root / folder).mkdir()
        (self.project / "ROLES.md").write_text("# Plan roles: example\n")
        self.write("archive/loose notes.md", "Unstructured legacy notes.\n")
        self.write("2026-09-20-active-work.md", plan_text("in_progress", "2026-09-20", "", body=PREMISE + SECTIONS))
        self.write("complete/2026-09-15-finished-work.md", plan_text("complete", "2026-09-15", "2026-09-16"))
        self.write("complete/2026-01-01-legacy-work.md", plan_text("complete", "2026-01-01", "2026-01-05", body="- a list, not a premise\n"))
        self.write("complete/2026-01-02-live-carrier.md", plan_text("in_progress", "2026-01-02", ""))
        self.write("complete/deferred/2026-01-03-parked-work.md", plan_text("in_progress", "2026-01-03", ""))
        self.write("2026-09-21-bundle-work/plan.md", plan_text("in_progress", "2026-09-21", "", body=PREMISE + SECTIONS))
        self.write("2026-09-21-bundle-work/evidence.json", "{}\n")
        self.write("eval-runs/20260920-101500Z-dev-0123abcd-smoke-check-89abcdef/receipt.json", "{}\n")
        for name in ("CLAUDE.md", "AGENTS.md"):
            (self.root / name).write_text("Instruction.\n" * 95)
        old_plans = str(self.base / "old-plans")
        self.registry = {"schema_version": 1, "canonical_root": "/canonical/library", "canonical_subdirectories": ["complete", "eval-runs", "reviews", ".session"], "projects": [{"id": "example", "source_root": str(self.source_root), "plan_directory": "example", "imports": [{"source": old_plans, "destination": "example", "kind": "tree", "disposition": "migrated"}], "legacy_subtrees": ["archive"], "live_in_complete": ["complete/2026-01-02-live-carrier.md"]}]}
        legacy = self.project / "complete/2026-01-01-legacy-work.md"
        self.record = {"project": "example", "source": old_plans + "/complete/2026-01-01-legacy-work.md", "destination": "example/complete/2026-01-01-legacy-work.md", "source_sha256": sha256(legacy), "destination_sha256": sha256(legacy), "redactions": []}
        self.manifest = {"schema_version": 1, "canonical_root": "/canonical/library", "imports": [{"project": "example", "source": old_plans, "destination": "example", "kind": "tree", "file_count": 1}], "files": [self.record]}
        self.moves = []
        self.save()

    def save(self):
        (self.root / "projects.json").write_text(json.dumps(self.registry))
        (self.root / "migration/manifest.json").write_text(json.dumps(self.manifest))
        (self.root / "migration/moves.json").write_text(json.dumps(self.moves))

    def write(self, relative, text):
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def errors(self, check_manifest=False):
        self.write_roles()
        return VALIDATOR.validate(self.root, check_manifest)

    def write_roles(self, additional_rows=()):
        rows = []
        for path in VALIDATOR.primary_plans(self.project, self.registry["projects"][0]):
            fields, _ = VALIDATOR.parse_frontmatter(path.read_text())
            if fields is None:
                continue
            target = path.relative_to(self.project).as_posix()
            location = VALIDATOR.location_of(Path(target))
            if fields.get("status") == "superseded":
                state, section, priority = "superseded", "Superseded", "-"
            elif fields.get("status") == "complete":
                state, section, priority = "complete", "Complete", "-"
            elif location == "deferred":
                state, section, priority = "deferred", "Deferred", "-"
            else:
                state, section, priority = "in_progress", "Current work", "later"
            rows.append(dict(role=target, state=state, section=section, priority=priority, updated="UNKNOWN", target=target, summary="Fixture plan."))
        rows.extend(additional_rows)
        lines = ["# Plan roles: example", "", "COUNTS", "CONTINUATION", ""]
        for section in VALIDATOR.ROLES.SECTIONS:
            lines.extend(["## " + section, "", "| " + " | ".join(VALIDATOR.ROLES.COLUMNS) + " |", "|---|---|---|---|---|---|"])
            for row in sorted((row for row in rows if row["section"] == section), key=VALIDATOR.ROLES.row_sort_key):
                cells = [row["role"], row["state"], row["priority"], row["updated"], f"[plan]({row['target']})", row["summary"]]
                lines.append("| " + " | ".join(cells) + " |")
            lines.append("")
        index = self.project / "ROLES.md"
        index.write_text("\n".join(lines))
        parsed = VALIDATOR.ROLES.read_index(index)
        lines[2] = VALIDATOR.ROLES.counts_line(parsed)
        lines[3] = VALIDATOR.ROLES.continuation_line(parsed)
        index.write_text("\n".join(lines))

    def index_error(self, fragment, change):
        self.write_roles()
        index = self.project / "ROLES.md"
        index.write_text(change(index.read_text()))
        errors = VALIDATOR.validate(self.root)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_superseded_unfinished_plan_passes(self):
        self.write("complete/2026-09-22-obsolete.md", plan_text("superseded", "2026-09-22", "", body=PREMISE + SECTIONS, extra="superseded_on: 2026-09-23\nsucceeded_by: 2026-09-20-active-work.md\n"))
        self.assertEqual(self.errors(), [])

    def test_reference_requires_resolvable_plan_frontmatter(self):
        self.write("support.md", "# Supporting evidence\n")
        self.index_error("ROLES target needs plan frontmatter", lambda text: text.replace("2026-09-20-active-work.md", "support.md"))

    def test_superseded_plan_with_prior_verified_completion_passes(self):
        self.write("complete/2026-09-22-obsolete.md", plan_text("superseded", "2026-09-22", "2026-09-23", body=PREMISE + SECTIONS, extra="superseded_on: 2026-09-24\nsucceeded_by: 2026-09-20-active-work.md\n"))
        self.assertEqual(self.errors(), [])

    def test_superseded_plan_requires_replacement(self):
        self.write("complete/2026-09-22-obsolete.md", plan_text("superseded", "2026-09-22", "", body=PREMISE + SECTIONS, extra="superseded_on: 2026-09-23\n"))
        self.assert_error("Superseded plan requires succeeded_by")

    def test_superseded_plan_requires_closure_date(self):
        self.write("complete/2026-09-22-obsolete.md", plan_text("superseded", "2026-09-22", "", body=PREMISE + SECTIONS, extra="succeeded_by: 2026-09-20-active-work.md\n"))
        self.assert_error("Superseded date")

    def test_superseded_completion_cannot_follow_supersession(self):
        self.write("complete/2026-09-22-obsolete.md", plan_text("superseded", "2026-09-22", "2026-09-24", body=PREMISE + SECTIONS, extra="superseded_on: 2026-09-23\nsucceeded_by: 2026-09-20-active-work.md\n"))
        self.assert_error("Invalid prior completion date")

    def test_superseded_plan_must_be_in_complete(self):
        self.write("2026-09-22-obsolete.md", plan_text("superseded", "2026-09-22", "", body=PREMISE + SECTIONS, extra="superseded_on: 2026-09-23\nsucceeded_by: 2026-09-20-active-work.md\n"))
        self.assert_error("superseded plan outside complete/")

    def test_successor_self_cycle_fails(self):
        self.write("complete/2026-09-22-obsolete.md", plan_text("superseded", "2026-09-22", "", body=PREMISE + SECTIONS, extra="superseded_on: 2026-09-23\nsucceeded_by: complete/2026-09-22-obsolete.md\n"))
        self.assert_error("Cyclic succeeded_by")

    def test_successor_two_plan_cycle_fails(self):
        for name, other in (("first", "second"), ("second", "first")):
            self.write(f"complete/2026-09-22-{name}.md", plan_text("superseded", "2026-09-22", "", body=PREMISE + SECTIONS, extra=f"superseded_on: 2026-09-23\nsucceeded_by: complete/2026-09-22-{other}.md\n"))
        self.assert_error("Cyclic succeeded_by")

    def test_successor_outside_registered_projects_fails(self):
        self.write("complete/2026-09-22-obsolete.md", plan_text("superseded", "2026-09-22", "", body=PREMISE + SECTIONS, extra="superseded_on: 2026-09-23\nsucceeded_by: ../../outside.md\n"))
        self.assert_error("Unsafe succeeded_by")

    def test_roles_incorrect_counts_fail(self):
        self.index_error("ROLES summary", lambda text: text.replace("Counts: current=", "Counts: current=9"))

    def test_roles_incorrect_continuation_fails(self):
        self.index_error("ROLES summary", lambda text: text.replace("Continuation: 0 ", "Continuation: 8 "))

    def test_roles_missing_current_main_file_fails(self):
        self.index_error("Current plan missing from ROLES", lambda text: "\n".join(line for line in text.splitlines() if not line.startswith("| 2026-09-20-active-work.md |")) + "\n")

    def test_roles_priority_order_fails(self):
        self.index_error("ROLES ordering", lambda text: text.replace("| 2026-09-21-bundle-work/plan.md | in_progress | later |", "| 2026-09-21-bundle-work/plan.md | in_progress | now |"))

    def test_roles_completed_current_row_fails(self):
        self.index_error("ROLES status mismatch", lambda text: text.replace("[plan](2026-09-20-active-work.md)", "[plan](complete/2026-09-15-finished-work.md)"))

    def test_roles_unsafe_target_fails(self):
        self.index_error("Unsafe ROLES target", lambda text: text.replace("[plan](2026-09-20-active-work.md)", "[plan](../../outside.md)"))

    def test_roles_missing_target_fails(self):
        self.index_error("Unresolved ROLES target", lambda text: text.replace("[plan](2026-09-20-active-work.md)", "[plan](2026-09-20-missing.md)"))

    def test_roles_duplicate_current_alias_fails(self):
        self.index_error("Duplicate current role", lambda text: text.replace("| 2026-09-21-bundle-work/plan.md |", "| 2026-09-20-active-work.md |"))

    def test_roles_new_primary_bundle_needs_index_entry(self):
        self.write_roles()
        self.write("2026-09-22-new-bundle/plan.md", plan_text("in_progress", "2026-09-22", "", body=PREMISE + SECTIONS))
        self.assertTrue(any("Current plan missing from ROLES" in error for error in VALIDATOR.validate(self.root)))

    def add_shared_bundle(self, section="Current work", indexed=True, combined=False):
        directory = "2026-10-18-shared-migration"
        bundle = self.root / directory
        bundle.mkdir()
        main_name = "claude.md" if combined else "plan.md"
        (bundle / main_name).write_text(plan_text("in_progress", "2026-10-18", "", body=PREMISE + SECTIONS))
        if not combined:
            (bundle / "README.md").write_text("Read the shared migration plan.\n")
        self.registry["temporary_shared_bundles"] = [dict(directory=directory, coordinator_project="example", purpose="Temporary migration workspace.")]
        if combined:
            self.registry["temporary_shared_bundles"][0]["combined_entrypoint"] = main_name
        self.save()
        state, priority = ("reference", "-") if section == "Current references" else ("in_progress", "later")
        rows = [dict(role="shared migration", state=state, section=section, priority=priority, updated="UNKNOWN", target=f"../{directory}/{main_name}", summary="Complete the shared migration.")]
        self.write_roles(rows if indexed else [])
        return bundle

    def test_shared_combined_entrypoint_preserves_plan_and_index_validation(self):
        bundle = self.add_shared_bundle(combined=True)
        main = bundle / "claude.md"
        self.assertEqual(VALIDATOR.validate(self.root), [])
        original = main.read_text()
        main.write_text("# Missing plan fields\n")
        self.assertTrue(any("Missing frontmatter" in error for error in VALIDATOR.validate(self.root)))
        main.write_text(original)
        self.write_roles()
        self.assertTrue(any("Temporary shared plan missing from coordinator ROLES" in error for error in VALIDATOR.validate(self.root)))

    def test_shared_combined_entrypoint_requires_safe_existing_file(self):
        bundle = self.add_shared_bundle(combined=True)
        main = bundle / "claude.md"
        main.unlink()
        self.assertTrue(any(f"Temporary shared bundle {bundle.name}/claude.md:" in error for error in VALIDATOR.validate(self.root)))
        outside = self.base / "outside.md"
        outside.write_text("PRIVATE SENTINEL")
        main.symlink_to(outside)
        errors = VALIDATOR.validate(self.root)
        self.assertTrue(any("Unsafe" in error or "unsafe" in error for error in errors), errors)
        self.assertNotIn("PRIVATE SENTINEL", "\n".join(errors))

    def test_shared_combined_entrypoint_rejects_unsafe_registry_names(self):
        self.add_shared_bundle(combined=True)
        for name in (None, 1, "", "../claude.md", "/tmp/claude.md", "nested/claude.md", "claude.md#status", "claude.txt"):
            with self.subTest(name=name):
                self.registry["temporary_shared_bundles"][0]["combined_entrypoint"] = name
                self.save()
                self.assertTrue(any("Unsafe temporary shared bundle combined entrypoint" in error for error in VALIDATOR.validate(self.root)))

    def test_declared_shared_bundle_passes_with_coordinator_index(self):
        bundle = self.add_shared_bundle()
        self.assertEqual(VALIDATOR.validate(self.root), [])
        self.assertFalse((bundle / "ROLES.md").exists())

    def test_shared_bundle_can_be_a_coordinator_current_reference(self):
        self.add_shared_bundle(section="Current references")
        self.assertEqual(VALIDATOR.validate(self.root), [])

    def test_shared_bundle_requires_coordinator_current_index(self):
        self.add_shared_bundle(indexed=False)
        errors = VALIDATOR.validate(self.root)
        self.assertTrue(any("Temporary shared plan missing from coordinator ROLES" in error for error in errors), errors)

    def test_undeclared_root_bundle_remains_unregistered(self):
        bundle = self.add_shared_bundle()
        self.registry.pop("temporary_shared_bundles")
        self.save()
        errors = VALIDATOR.validate(self.root)
        self.assertIn(f"Unregistered folder: {bundle.name}", errors)
        self.assertTrue(any("Unsafe ROLES target" in error for error in errors), errors)

    def test_shared_bundle_requires_plan_and_readme(self):
        bundle = self.add_shared_bundle()
        for name in ("plan.md", "README.md"):
            with self.subTest(name=name):
                path = bundle / name
                original = path.read_text()
                path.unlink()
                errors = VALIDATOR.validate(self.root)
                self.assertTrue(any(f"Temporary shared bundle {bundle.name}/{name}:" in error for error in errors), errors)
                path.write_text(original)

    def test_shared_bundle_uses_current_plan_rules(self):
        bundle = self.add_shared_bundle()
        cases = [
            ("# No frontmatter\n", "Missing frontmatter"),
            (plan_text("invalid", "2026-10-18", "", body=PREMISE + SECTIONS), "Invalid status"),
            (plan_text("in_progress", "invalid", "", body=PREMISE + SECTIONS), "Created date invalid"),
            (plan_text("in_progress", "2026-10-18", "2026-10-18", body=PREMISE + SECTIONS), "Completed date must stay empty"),
            (plan_text("in_progress", "2026-10-18", "", body=SECTIONS), "Missing premise"),
            (plan_text("in_progress", "2026-10-18", ""), "Missing Status section"),
            (plan_text("complete", "2026-10-18", "2026-10-18", body=PREMISE + SECTIONS), "Placement: complete plan outside complete/"),
        ]
        for text, fragment in cases:
            with self.subTest(fragment=fragment):
                (bundle / "plan.md").write_text(text)
                errors = VALIDATOR.validate(self.root)
                self.assertTrue(any(fragment in error for error in errors), errors)

    def test_shared_bundle_goal_limit_applies(self):
        bundle = self.add_shared_bundle()
        for length in (4000, 4001):
            with self.subTest(length=length):
                (bundle / "goal.md").write_text("g" * length)
                errors = VALIDATOR.validate(self.root)
                self.assertEqual(any("Goal over 4000" in error for error in errors), length > 4000, errors)

    def test_shared_bundle_rejects_outside_file_symlinks_without_reading(self):
        bundle = self.add_shared_bundle()
        outside = self.base / "outside.md"
        outside.write_text("PRIVATE SENTINEL")
        for name in ("plan.md", "README.md", "goal.md"):
            with self.subTest(name=name):
                path = bundle / name
                original = path.read_text() if path.exists() else None
                if path.exists():
                    path.unlink()
                path.symlink_to(outside)
                errors = VALIDATOR.validate(self.root)
                self.assertTrue(any("Unsafe" in error or "unsafe" in error for error in errors), errors)
                self.assertNotIn("PRIVATE SENTINEL", "\n".join(errors))
                path.unlink()
                if original is not None:
                    path.write_text(original)

    def test_shared_bundle_rejects_root_symlinks(self):
        bundle = self.add_shared_bundle()
        moved = self.base / bundle.name
        bundle.rename(moved)
        bundle.symlink_to(moved, target_is_directory=True)
        errors = VALIDATOR.validate(self.root)
        self.assertTrue(any("unsafe temporary shared bundle directory" in error for error in errors), errors)

    def test_shared_bundle_rejects_outside_support_symlinks(self):
        bundle = self.add_shared_bundle()
        (bundle / "support").symlink_to(self.source_root, target_is_directory=True)
        errors = VALIDATOR.validate(self.root)
        self.assertTrue(any("Unsafe temporary shared bundle symlink" in error for error in errors), errors)

    def test_shared_bundle_registry_rejects_malformed_entries(self):
        self.add_shared_bundle()
        entry = self.registry["temporary_shared_bundles"][0]
        malformed = [None, {}, [None], [{}], [dict(entry, extra="unexpected")], [dict(entry, purpose=" ")], [dict(entry, purpose=1)], [dict(entry, coordinator_project="unknown")], [dict(entry, coordinator_project=[])], [entry, entry]]
        for entries in malformed:
            with self.subTest(entries=entries):
                self.registry["temporary_shared_bundles"] = entries
                self.save()
                self.assertTrue(VALIDATOR.validate(self.root))

    def test_shared_bundle_registry_rejects_unsafe_or_invalid_names(self):
        self.add_shared_bundle()
        entry = self.registry["temporary_shared_bundles"][0]
        for directory in ("../2026-10-18-escape", "nested/2026-10-18-escape", "/tmp/2026-10-18-escape", "2026-02-30-invalid", "2026-10-18-UPPER", "undated", None):
            with self.subTest(directory=directory):
                self.registry["temporary_shared_bundles"] = [dict(entry, directory=directory)]
                self.save()
                self.assertTrue(VALIDATOR.validate(self.root))

    def test_shared_bundle_cannot_collide_with_a_registered_project(self):
        bundle = self.add_shared_bundle()
        self.registry["projects"].append(dict(id="collision", plan_directory=bundle.name))
        self.save()
        errors = VALIDATOR.validate(self.root)
        self.assertTrue(any("colliding temporary shared bundle" in error for error in errors), errors)

    def test_shared_role_rejects_extra_traversal(self):
        bundle = self.add_shared_bundle()
        index = self.project / "ROLES.md"
        index.write_text(index.read_text().replace(f"../{bundle.name}/plan.md", f"../{bundle.name}/../{bundle.name}/plan.md"))
        errors = VALIDATOR.validate(self.root)
        self.assertTrue(any("Unsafe ROLES target" in error for error in errors), errors)

    def assert_error(self, fragment, check_manifest=False):
        errors = self.errors(check_manifest)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_library_passes(self):
        self.assertEqual(self.errors(), [])

    def test_manifest_receipt_passes(self):
        self.assertEqual(self.errors(True), [])

    def test_nonconforming_plan_name_fails(self):
        self.write("Random Plan Name.md", plan_text("in_progress", "2026-09-20", ""))
        self.assert_error("Plan name")

    def test_missing_frontmatter_fails(self):
        self.write("2026-09-22-no-header.md", "# Title\n\n" + PREMISE)
        self.assert_error("Missing frontmatter")

    def test_unknown_status_fails(self):
        self.write("2026-09-22-odd-status.md", plan_text("shipped", "2026-09-22", ""))
        self.assert_error("Invalid status")

    def test_invalid_created_date_fails(self):
        self.write("2026-09-22-bad-created.md", plan_text("in_progress", "September", ""))
        self.assert_error("Created date")

    def test_in_progress_with_completed_date_fails(self):
        self.write("2026-09-22-early-stamp.md", plan_text("in_progress", "2026-09-22", "2026-09-23"))
        self.assert_error("Completed date")

    def test_null_completed_value_fails(self):
        self.write("2026-09-22-null-stamp.md", plan_text("in_progress", "2026-09-22", "null"))
        self.assert_error("Completed date")

    def test_complete_without_completed_date_fails(self):
        self.write("complete/2026-09-22-unstamped.md", plan_text("complete", "2026-09-22", ""))
        self.assert_error("Completed date")

    def test_completed_before_created_fails(self):
        self.write("complete/2026-09-22-backwards.md", plan_text("complete", "2026-09-22", "2026-09-01"))
        self.assert_error("Completed date")

    def test_complete_plan_at_root_fails(self):
        self.write("2026-09-22-done-but-active.md", plan_text("complete", "2026-09-22", "2026-09-23"))
        self.assert_error("Placement")

    def test_in_progress_plan_in_complete_fails(self):
        self.write("complete/2026-09-22-not-done.md", plan_text("in_progress", "2026-09-22", ""))
        self.assert_error("Placement")

    def test_complete_plan_in_deferred_fails(self):
        self.write("complete/deferred/2026-09-22-done-parked.md", plan_text("complete", "2026-09-22", "2026-09-23"))
        self.assert_error("Placement")

    def test_new_plan_without_premise_fails(self):
        self.write("2026-09-22-no-premise.md", plan_text("in_progress", "2026-09-22", "", body="- only a list\n"))
        self.assert_error("Missing premise")

    def test_new_plan_without_discoveries_fails(self):
        self.write("2026-09-22-no-discoveries.md", plan_text("in_progress", "2026-09-22", "", body=PREMISE + "\n## Decisions\n\n## Status\n"))
        self.assert_error("Missing Discoveries section")

    def test_numbered_sections_pass(self):
        self.write("2026-09-22-numbered-sections.md", plan_text("in_progress", "2026-09-22", "", body=PREMISE + "\n## 1. Decisions\n\n## 2. Discoveries\n\n## 3. Status\n"))
        self.assertEqual(self.errors(), [])

    def test_plan_before_section_cutoff_passes(self):
        self.write("2026-09-16-no-sections.md", plan_text("in_progress", "2026-09-16", ""))
        self.assertEqual(self.errors(), [])

    def test_new_bundle_without_plan_fails(self):
        self.write("2026-09-22-loose-bundle/notes.md", "Notes.\n")
        self.assert_error("Bundle without plan.md")

    def test_handoff_goal_over_limit_fails(self):
        self.write("2026-10-13-demo-handoff/plan.md", plan_text("in_progress", "2026-10-13", "", body=PREMISE + SECTIONS))
        self.write("2026-10-13-demo-handoff/goal.md", "g" * 4001)
        self.assert_error("Goal over 4000 characters")

    def test_handoff_goal_at_limit_passes(self):
        self.write("2026-10-13-demo-handoff/plan.md", plan_text("in_progress", "2026-10-13", "", body=PREMISE + SECTIONS))
        self.write("2026-10-13-demo-handoff/goal.md", "g" * 4000)
        self.assertEqual(self.errors(), [])

    def test_goal_in_bundle_before_handoff_cutoff_passes(self):
        self.write("2026-10-11-early-bundle/plan.md", plan_text("in_progress", "2026-10-11", "", body=PREMISE + SECTIONS))
        self.write("2026-10-11-early-bundle/goal.md", "g" * 5000)
        self.assertEqual(self.errors(), [])

    def test_legacy_bundle_without_plan_passes(self):
        self.write("complete/2026-01-04-old-bundle/notes.md", "Notes.\n")
        self.assertEqual(self.errors(), [])

    def test_new_eval_run_name_fails(self):
        self.write("eval-runs/run-latest/receipt.json", "{}\n")
        self.assert_error("Eval run name")

    def test_legacy_eval_run_name_passes(self):
        self.write("complete/eval-runs/20260910-1856-run-001-parity/receipt.json", "{}\n")
        self.assertEqual(self.errors(), [])

    def test_undeclared_subtree_fails(self):
        self.write("scratch/notes.md", "Notes.\n")
        self.assert_error("Undeclared subtree")

    def test_unresolved_succeeded_by_fails(self):
        self.write("complete/2026-09-22-replaced.md", plan_text("complete", "2026-09-22", "2026-09-23", extra="succeeded_by: complete/2026-09-30-missing.md\n"))
        self.assert_error("Unresolved succeeded_by")

    def test_resolved_succeeded_by_passes(self):
        self.write("complete/2026-09-22-replaced.md", plan_text("complete", "2026-09-22", "2026-09-23", body=PREMISE + SECTIONS, extra="succeeded_by: 2026-09-20-active-work.md\n"))
        self.assertEqual(self.errors(), [])

    def test_instruction_mismatch_fails(self):
        (self.root / "AGENTS.md").write_text("Different.\n" * 95)
        self.assert_error("CLAUDE.md and AGENTS.md differ")

    def test_instruction_line_count_fails(self):
        for name in ("CLAUDE.md", "AGENTS.md"):
            (self.root / name).write_text("Too long.\n" * 201)
        self.assert_error("at most 200")

    def test_missing_roles_file_fails(self):
        (self.project / "ROLES.md").unlink()
        errors = VALIDATOR.validate(self.root)
        self.assertTrue(any("Missing ROLES.md" in error for error in errors), errors)

    def test_missing_canonical_directory_fails(self):
        (self.project / "reviews").rmdir()
        self.assert_error("Missing canonical directory")

    def test_unregistered_folder_fails(self):
        (self.root / "stray-project").mkdir()
        self.assert_error("Unregistered folder")

    def test_repository_plans_directory_fails(self):
        (self.source_root / "plans").mkdir()
        self.assert_error("Repository plan store")

    def test_repository_docs_plans_directory_fails(self):
        (self.source_root / "docs/plans").mkdir(parents=True)
        self.assert_error("Repository plan store")

    def test_runtime_inbox_symlink_passes(self):
        (self.source_root / "plans").symlink_to(self.project / ".session/runtime-inbox")
        self.assertEqual(self.errors(), [])

    def test_other_plans_symlink_fails(self):
        (self.source_root / "plans").symlink_to(self.project / "reviews")
        self.assert_error("Repository plan store")

    def test_ds_store_fails(self):
        self.write(".DS_Store", "")
        self.assert_error(".DS_Store")

    def test_manifest_checks_skip_without_flag(self):
        self.record["destination_sha256"] = "0" * 64
        self.save()
        self.assertEqual(self.errors(), [])

    def test_manifest_hash_mismatch_fails(self):
        self.record["destination_sha256"] = "0" * 64
        self.record["source_sha256"] = "0" * 64
        self.save()
        self.assert_error("Manifest hash mismatch", True)

    def test_manifest_missing_destination_fails(self):
        (self.project / "complete/2026-01-01-legacy-work.md").unlink()
        self.assert_error("Missing manifest destination", True)

    def test_manifest_move_chain_resolves(self):
        old = self.project / "complete/2026-01-01-legacy-work.md"
        new = self.project / "complete/2026-01-01-renamed-legacy-work.md"
        before = sha256(old)
        old.rename(new)
        new.write_text(new.read_text().replace("# Title", "# Renamed"))
        self.moves.append({"from": "example/complete/2026-01-01-legacy-work.md", "to": "example/complete/2026-01-01-renamed-legacy-work.md", "sha256_before": before, "sha256_after": sha256(new), "reason": "normalized name"})
        self.save()
        self.assertEqual(self.errors(True), [])

    def test_manifest_in_place_edit_resolves(self):
        legacy = self.project / "complete/2026-01-01-legacy-work.md"
        before = sha256(legacy)
        legacy.write_text(legacy.read_text().replace("# Title", "# Edited"))
        self.moves.append({"from": "example/complete/2026-01-01-legacy-work.md", "to": "example/complete/2026-01-01-legacy-work.md", "sha256_before": before, "sha256_after": sha256(legacy), "reason": "frontmatter normalized"})
        self.save()
        self.assertEqual(self.errors(True), [])

    def test_manifest_removed_file_passes(self):
        old = self.project / "complete/2026-01-01-legacy-work.md"
        self.moves.append({"from": "example/complete/2026-01-01-legacy-work.md", "to": None, "sha256_before": sha256(old), "sha256_after": None, "reason": "duplicate"})
        old.unlink()
        self.save()
        self.assertEqual(self.errors(True), [])

    def test_manifest_broken_move_hash_fails(self):
        old = self.project / "complete/2026-01-01-legacy-work.md"
        new = self.project / "complete/2026-01-01-renamed-legacy-work.md"
        old.rename(new)
        self.moves.append({"from": "example/complete/2026-01-01-legacy-work.md", "to": "example/complete/2026-01-01-renamed-legacy-work.md", "sha256_before": "0" * 64, "sha256_after": sha256(new), "reason": "normalized name"})
        self.save()
        self.assert_error("Move chain hash mismatch", True)

    def test_unsafe_manifest_destination_fails(self):
        self.record["destination"] = "../escape.md"
        self.save()
        self.assert_error("Unsafe destination", True)

    def test_unexplained_content_change_fails(self):
        self.record["source_sha256"] = "0" * 64
        self.save()
        self.assert_error("Unexplained content change", True)

    def test_registry_import_mismatch_fails(self):
        self.manifest["imports"][0]["destination"] = "elsewhere"
        self.save()
        self.assert_error("Registry and manifest import mappings differ", True)


if __name__ == "__main__":
    unittest.main()
