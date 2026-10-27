import argparse
import fnmatch
import hashlib
import importlib.util
import json
import re
from datetime import date
from pathlib import Path


CUTOFF = "2026-09-14"
SECTION_CUTOFF = "2026-09-17"
HANDOFF_CUTOFF = "2026-10-12"
GOAL_LIMIT = 4000
REQUIRED_SECTIONS = ("Status", "Decisions", "Discoveries")
STATUSES = {"in_progress", "complete", "superseded"}
ROOT_FOLDERS = {"migration", "scripts", "tests"}
EMPTY_POINTERS = {"", "null", "~"}
PLAN_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$")
BUNDLE_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*$")
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EVAL_RUN_NAME = re.compile(r"^\d{8}-\d{6}Z-[a-z0-9]+-[0-9a-f]{8}-[a-z0-9]+(-[a-z0-9]+)*-[0-9a-f]{8}$")
EVAL_RUN_DATE = re.compile(r"^(\d{8})")
FIELD = re.compile(r"^([A-Za-z_][\w-]*):(.*)$")
NUMBERED = re.compile(r"^\d+[.)]\s")
SECTION = re.compile(r"^##\s+(?:\d+[.)]\s+)?(.+?)\s*$", re.M)
NON_PROSE = ("- ", "* ", "+ ", "|", ">", "```", "<", "![")

ROLES_SPEC = importlib.util.spec_from_file_location("plan_roles", Path(__file__).with_name("roles.py"))
ROLES = importlib.util.module_from_spec(ROLES_SPEC)
ROLES_SPEC.loader.exec_module(ROLES)


def parse_date(value):
    if not DATE.match(value or ""):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def parse_frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].rstrip() == "---":
            fields = {}
            for line in lines[1:index]:
                match = FIELD.match(line)
                if match:
                    fields[match.group(1)] = match.group(2).strip().strip("\"'")
            return fields, "\n".join(lines[index + 1:])
    return None, text


def has_premise(body):
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return not stripped.startswith(NON_PROSE) and not NUMBERED.match(stripped)
    return False


def location_of(relative):
    parts = relative.parts
    if parts[0] != "complete":
        return "root"
    return "deferred" if len(parts) > 2 and parts[1] == "deferred" else "complete"


def registered_owner(root, target):
    try:
        entry = ROLES.registered_owner(root, ROLES.read_registry(root), target.resolve())
    except ValueError:
        return None
    return root / entry["plan_directory"]


def successor_errors(project, relative, fields):
    successor = fields.get("succeeded_by", "")
    if successor in EMPTY_POINTERS:
        return []
    root = project.parent
    label = f"{project.name}/{relative.as_posix()}"
    seen = {(project / relative).resolve()}
    while successor not in EMPTY_POINTERS:
        if Path(successor).is_absolute():
            return [f"Unsafe succeeded_by: {label}"]
        target = (project / successor).resolve()
        owner = registered_owner(root, target)
        if owner is None:
            return [f"Unsafe succeeded_by: {label}"]
        if target in seen:
            return [f"Cyclic succeeded_by: {label}"]
        if not target.is_file():
            return [f"Unresolved succeeded_by: {label}"]
        seen.add(target)
        target_fields, _ = parse_frontmatter(target.read_text(encoding="utf-8", errors="replace"))
        if target_fields is None or target_fields.get("status") not in STATUSES:
            return [f"Invalid succeeded_by entrypoint: {label}"]
        project = owner
        successor = target_fields.get("succeeded_by", "")
    return []


def plan_errors(project, relative, text, live):
    label = f"{project.name}/{relative.as_posix()}"
    fields, body = parse_frontmatter(text)
    if fields is None:
        return [f"Missing frontmatter: {label}"]
    errors = []
    status = fields.get("status")
    created = parse_date(fields.get("created"))
    if status not in STATUSES:
        errors.append(f"Invalid status: {label}")
    if created is None:
        errors.append(f"Created date invalid: {label}")
    if "completed" not in fields:
        errors.append(f"Completed date field missing: {label}")
    elif status == "in_progress" and fields["completed"] != "":
        errors.append(f"Completed date must stay empty while in_progress: {label}")
    elif status == "complete":
        completed = parse_date(fields["completed"])
        if completed is None or (created is not None and completed < created):
            errors.append(f"Completed date must be a date on or after created: {label}")
    if status == "superseded":
        superseded = parse_date(fields.get("superseded_on"))
        completed = parse_date(fields.get("completed"))
        if superseded is None or (created is not None and superseded < created):
            errors.append(f"Superseded date must be a date on or after created: {label}")
        if fields.get("completed", "") and (completed is None or (created is not None and completed < created) or (superseded is not None and completed > superseded)):
            errors.append(f"Invalid prior completion date on superseded plan: {label}")
        if fields.get("succeeded_by", "") in EMPTY_POINTERS:
            errors.append(f"Superseded plan requires succeeded_by: {label}")
    location = location_of(relative)
    if status in {"complete", "superseded"} and location != "complete":
        errors.append(f"Placement: {status} plan outside complete/: {label}")
    if status == "in_progress" and location == "complete" and relative.as_posix() not in live:
        errors.append(f"Placement: in_progress plan inside complete/: {label}")
    legacy = created is not None and created.isoformat() < CUTOFF
    if not legacy and not has_premise(body):
        errors.append(f"Missing premise: {label}")
    if created is not None and created.isoformat() >= SECTION_CUTOFF:
        headings = set(SECTION.findall(body))
        errors.extend(f"Missing {section} section: {label}" for section in REQUIRED_SECTIONS if section not in headings)
    errors.extend(successor_errors(project, relative, fields))
    return errors


def primary_plans(project, entry):
    targets = set()
    for base in (project, project / "complete", project / "complete" / "deferred"):
        if not base.is_dir():
            continue
        for item in base.iterdir():
            if not DATED.match(item.name):
                continue
            target = item / "plan.md" if item.is_dir() else item
            if target.is_file() and target.suffix == ".md":
                targets.add(target.resolve())
    targets.update((project / relative).resolve() for relative in entry.get("live_in_complete", []))
    return targets


def roles_errors(root, entry, projects):
    project = root / entry["plan_directory"]
    index = project / "ROLES.md"
    if not index.is_file():
        return []
    try:
        rows = ROLES.read_index(index)
    except ValueError as error:
        return [f"ROLES format: {entry['id']}: {error}"]
    errors = []
    text = index.read_text()
    for expected in (ROLES.counts_line(rows), ROLES.continuation_line(rows)):
        if text.splitlines().count(expected) != 1:
            errors.append(f"ROLES summary: {entry['id']}: expected {expected}")
    targets = set()
    current_roles = set()
    identities = set()
    allowed = {
        "Current work": {"in_progress", "blocked"},
        "Current references": {"reference"},
        "Deferred": {"deferred"},
        "Superseded": {"superseded"},
        "Complete": {"complete"},
    }
    for row in rows:
        label = f"{entry['id']}/ROLES.md:{row['line']}"
        identity = (row["role"].casefold(), row["target"], row["section"])
        if identity in identities:
            errors.append(f"Duplicate ROLES entry: {label}")
        identities.add(identity)
        if row["section"] in {"Current work", "Current references"}:
            role = row["role"].casefold()
            if role in current_roles:
                errors.append(f"Duplicate current role: {label}")
            current_roles.add(role)
        if row["state"] not in allowed[row["section"]]:
            errors.append(f"ROLES state/section mismatch: {label}")
        priorities = {"now", "next", "later"} if row["section"] == "Current work" else {"-"}
        if row["priority"] not in priorities:
            errors.append(f"ROLES priority: {label}")
        if row["updated"] != "UNKNOWN" and parse_date(row["updated"]) is None:
            errors.append(f"ROLES updated date: {label}")
        if not row["role"] or not row["summary"]:
            errors.append(f"Empty ROLES role/summary: {label}")
        try:
            target, owner_entry = ROLES.safe_target(root, projects, entry, row["target"])
        except ValueError as error:
            kind = "Unresolved" if str(error).startswith("Missing target:") else "Unsafe"
            errors.append(f"{kind} ROLES target: {label}")
            continue
        owner = root / owner_entry["plan_directory"]
        if target.is_dir():
            target = target / "plan.md"
            if not target.is_file():
                errors.append(f"ROLES target needs a main file: {label}")
                continue
        fields, _ = parse_frontmatter(target.read_text(encoding="utf-8", errors="replace"))
        location = location_of(target.relative_to(owner))
        status = (fields or {}).get("status")
        if status not in STATUSES:
            errors.append(f"ROLES target needs plan frontmatter: {label}")
        if row["section"] in {"Current work", "Current references"}:
            targets.add(target.resolve())
        if row["state"] in {"in_progress", "blocked"} and status != "in_progress":
            errors.append(f"ROLES status mismatch: {label}")
        if row["state"] == "deferred" and (status != "in_progress" or location != "deferred"):
            errors.append(f"ROLES deferred placement: {label}")
        if row["state"] == "complete" and (status != "complete" or location != "complete"):
            errors.append(f"ROLES complete placement: {label}")
        if row["state"] == "superseded" and (location != "complete" or not (status == "superseded" or status == "complete" and fields.get("succeeded_by", "") not in EMPTY_POINTERS)):
            errors.append(f"ROLES superseded placement: {label}")
        if row["state"] == "reference" and status == "superseded":
            errors.append(f"Superseded plan cannot be a current reference: {label}")
    for section in ROLES.SECTIONS:
        group = [row for row in rows if row["section"] == section]
        if group != sorted(group, key=ROLES.row_sort_key):
            errors.append(f"ROLES ordering: {entry['id']}/{section}")
    for target in primary_plans(project, entry):
        fields, _ = parse_frontmatter(target.read_text(encoding="utf-8", errors="replace"))
        if (fields or {}).get("status") == "in_progress" and location_of(target.relative_to(project)) != "deferred" and target not in targets:
            errors.append(f"Current plan missing from ROLES: {entry['id']}/{target.relative_to(project)}")
    for item in project.iterdir():
        dated = DATED.match(item.name)
        if item.is_dir() and dated and dated.group(1) < CUTOFF and not (item / "plan.md").is_file() and not any(target.is_relative_to(item.resolve()) for target in targets):
            errors.append(f"Legacy current bundle missing from ROLES: {entry['id']}/{item.name}")
    for directory, owner in ROLES.temporary_shared_bundles(root, projects).items():
        main_file = root / directory / owner.get("combined_entrypoint", "plan.md")
        if owner["id"] == entry["id"] and main_file.resolve() not in targets:
            errors.append(f"Temporary shared plan missing from coordinator ROLES: {entry['id']}/{directory}/{main_file.name}")
    return errors


def shared_bundle_errors(root, entry, projects):
    bundle = root / entry["plan_directory"]
    errors = []
    for path in bundle.rglob("*"):
        if path.is_symlink() and not path.resolve().is_relative_to(bundle):
            errors.append(f"Unsafe temporary shared bundle symlink: {path.relative_to(root)}")
    files = {}
    main_name = entry.get("combined_entrypoint", "plan.md")
    required = (main_name,) if "combined_entrypoint" in entry else ("plan.md", "README.md")
    for name in (*required, "goal.md"):
        if name == "goal.md" and not (bundle / name).exists() and not (bundle / name).is_symlink():
            continue
        try:
            target, _ = ROLES.safe_target(root, projects, entry, name)
            if not target.is_file():
                raise ValueError(f"Missing file: {name}")
            files[name] = target
        except ValueError as error:
            errors.append(f"Temporary shared bundle {bundle.name}/{name}: {error}")
    if main_name in files:
        errors.extend(plan_errors(bundle, Path(main_name), files[main_name].read_text(encoding="utf-8", errors="replace"), set()))
    if bundle.name[:10] >= HANDOFF_CUTOFF and "goal.md" in files:
        length = len(files["goal.md"].read_text(encoding="utf-8", errors="replace"))
        if length > GOAL_LIMIT:
            errors.append(f"Goal over {GOAL_LIMIT} characters ({length}): {bundle.name}/goal.md")
    return errors


def bundle_errors(project, bundle, relative, bundle_date, live):
    label = f"{project.name}/{relative}"
    legacy = bundle_date < CUTOFF
    errors = []
    if not legacy and not BUNDLE_NAME.match(bundle.name):
        errors.append(f"Plan name: {label}")
    plan = bundle / "plan.md"
    if plan.is_file():
        errors.extend(plan_errors(project, Path(relative) / "plan.md", plan.read_text(encoding="utf-8", errors="replace"), live))
    elif not legacy:
        errors.append(f"Bundle without plan.md: {label}")
    goal = bundle / "goal.md"
    if bundle_date >= HANDOFF_CUTOFF and goal.is_file():
        length = len(goal.read_text(encoding="utf-8", errors="replace"))
        if length > GOAL_LIMIT:
            errors.append(f"Goal over {GOAL_LIMIT} characters ({length}): {label}/goal.md")
    return errors


def eval_run_errors(project):
    errors = []
    for runs in (project / "eval-runs", project / "complete" / "eval-runs"):
        if not runs.is_dir():
            continue
        for entry in sorted(runs.iterdir()):
            if not entry.is_dir() or entry.name.startswith(".") or EVAL_RUN_NAME.match(entry.name):
                continue
            run_date = EVAL_RUN_DATE.match(entry.name)
            if not (run_date and run_date.group(1) < CUTOFF.replace("-", "")):
                errors.append(f"Eval run name: {project.name}/{entry.relative_to(project).as_posix()}")
    return errors


def project_errors(root, entry, canonical):
    project = root / entry["plan_directory"]
    if not project.is_dir():
        return [f"Missing project folder: {entry['id']}"]
    errors = []
    if not (project / "ROLES.md").is_file():
        errors.append(f"Missing ROLES.md: {entry['id']}")
    for subdirectory in canonical:
        if not (project / subdirectory).is_dir():
            errors.append(f"Missing canonical directory: {entry['id']}/{subdirectory}")
    legacy_subtrees = entry.get("legacy_subtrees", [])
    live = set(entry.get("live_in_complete", []))
    levels = [(project, set(canonical)), (project / "complete", {"deferred", "eval-runs"}), (project / "complete" / "deferred", set())]
    for level, allowed in levels:
        if not level.is_dir():
            continue
        for item in sorted(level.iterdir()):
            relative = item.relative_to(project).as_posix()
            if item.is_dir():
                if item.name in allowed or any(fnmatch.fnmatchcase(relative, pattern) for pattern in legacy_subtrees):
                    continue
                dated = DATED.match(item.name)
                if dated:
                    errors.extend(bundle_errors(project, item, relative, dated.group(1), live))
                else:
                    errors.append(f"Undeclared subtree: {entry['id']}/{relative}")
            elif item.suffix == ".md" and not (level == project and item.name == "ROLES.md"):
                if not PLAN_NAME.match(item.name):
                    errors.append(f"Plan name: {entry['id']}/{relative}")
                errors.extend(plan_errors(project, Path(relative), item.read_text(encoding="utf-8", errors="replace"), live))
    errors.extend(eval_run_errors(project))
    if any(True for _ in project.rglob(".DS_Store")):
        errors.append(f"Excluded .DS_Store file found: {entry['id']}")
    return errors


def source_errors(root, entry):
    source = entry.get("source_root")
    if not source:
        return []
    inbox = (root / entry["plan_directory"] / ".session" / "runtime-inbox").resolve()
    errors = []
    source_path = Path(source).expanduser()
    source_path = source_path if source_path.is_absolute() else (root / source_path).resolve()
    for candidate in (source_path / "plans", source_path / "docs" / "plans"):
        if candidate.is_symlink():
            if candidate.resolve() != inbox:
                errors.append(f"Repository plan store: {candidate}")
        elif candidate.exists():
            errors.append(f"Repository plan store: {candidate}")
    return errors


def manifest_errors(root, registry):
    manifest = json.loads((root / "migration/manifest.json").read_text())
    moves_path = root / "migration/moves.json"
    moves = json.loads(moves_path.read_text()) if moves_path.is_file() else []
    errors = []
    if manifest.get("schema_version") != 1:
        errors.append("Unsupported manifest schema version")
    if manifest.get("canonical_root") != registry.get("canonical_root"):
        errors.append("Canonical root mismatch")
    by_source = {}
    for move in moves:
        if move["from"] in by_source:
            errors.append(f"Duplicate move source: {move['from']}")
        by_source[move["from"]] = move
    destinations = set()
    for record in manifest["files"]:
        destination = record["destination"]
        relative = Path(destination)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"Unsafe destination: {destination}")
            continue
        if destination in destinations:
            errors.append(f"Duplicate destination: {destination}")
        destinations.add(destination)
        if not record["redactions"] and record["source_sha256"] != record["destination_sha256"]:
            errors.append(f"Unexplained content change: {destination}")
        current, expected, seen, cycle = destination, record["destination_sha256"], set(), False
        while current is not None and current in by_source:
            if current in seen:
                cycle = True
                break
            seen.add(current)
            move = by_source[current]
            if move["sha256_before"] != expected:
                errors.append(f"Move chain hash mismatch: {current}")
            if move["to"] == current:
                expected = move["sha256_after"]
                break
            current, expected = move["to"], move["sha256_after"]
        if cycle:
            errors.append(f"Move chain cycle: {destination}")
            continue
        if current is None:
            continue
        target = root / current
        if target.is_symlink() or not target.is_file():
            errors.append(f"Missing manifest destination: {current}")
            continue
        data = target.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            errors.append(f"Manifest hash mismatch: {current}")
        for redaction in record["redactions"]:
            if redaction["replacement"].encode() not in data:
                errors.append(f"Missing redaction marker: {current}")
    expected_imports = [(project["id"], mapping["source"], mapping["destination"], mapping["kind"]) for project in registry["projects"] for mapping in project.get("imports", [])]
    actual_imports = [(mapping["project"], mapping["source"], mapping["destination"], mapping["kind"]) for mapping in manifest["imports"]]
    if expected_imports != actual_imports:
        errors.append("Registry and manifest import mappings differ")
    return errors


def validate(root, check_manifest=False):
    errors = []
    registry = json.loads((root / "projects.json").read_text())
    if registry.get("schema_version") != 1:
        errors.append("Unsupported schema version")
    instructions = [(root / name).read_bytes() for name in ("CLAUDE.md", "AGENTS.md")]
    if instructions[0] != instructions[1]:
        errors.append("CLAUDE.md and AGENTS.md differ")
    if any(len(data.splitlines()) > 200 or not data.endswith(b"\n") for data in instructions):
        errors.append("Instruction files must each have at most 200 newline-terminated lines")
    projects = registry["projects"]
    identifiers = [project["id"] for project in projects]
    if len(set(identifiers)) != len(identifiers):
        errors.append("Duplicate project IDs")
    try:
        registered_projects = ROLES.read_registry(root)
        shared = ROLES.temporary_shared_bundles(root, registered_projects, registry)
    except ValueError as error:
        return errors + [str(error)]
    folders = {project["plan_directory"] for project in projects} | ROOT_FOLDERS | set(shared)
    for item in sorted(root.iterdir()):
        if item.is_dir() and not item.name.startswith(".") and item.name not in folders:
            errors.append(f"Unregistered folder: {item.name}")
    for project in projects:
        errors.extend(project_errors(root, project, registry["canonical_subdirectories"]))
        errors.extend(roles_errors(root, project, registered_projects))
        errors.extend(source_errors(root, project))
    for entry in shared.values():
        errors.extend(shared_bundle_errors(root, entry, registered_projects))
    if check_manifest:
        errors.extend(manifest_errors(root, registry))
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--check-manifest", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        errors = validate(root, args.check_manifest)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Validation could not complete: {type(error).__name__}: {error}")
        return 1
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validation passed; manifest checks {'enabled' if args.check_manifest else 'disabled'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
