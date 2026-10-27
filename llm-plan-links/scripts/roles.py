import argparse
import json
import re
import sys
from datetime import date
from itertools import islice
from os.path import normpath
from pathlib import Path
from urllib.parse import unquote, urlsplit


SECTIONS = ("Current work", "Current references", "Deferred", "Superseded", "Complete")
COLUMNS = ("Role", "State", "Priority", "Updated", "Plan / folder", "Brief summary")
SECTION_NAMES = dict(zip(("current", "references", "deferred", "superseded", "complete"), SECTIONS))
STATES = {"in_progress", "blocked", "reference", "deferred", "superseded", "complete"}
PRIORITIES = {"now": 0, "next": 1, "later": 2, "-": 3}
PROJECT_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SHARED_BUNDLE = re.compile(r"(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LINK = re.compile(r"\[([^\[\]]+)\]\(([^()]+)\)\Z")
FIELD = re.compile(r"^([A-Za-z_][\w-]*):(.*)$")
EMPTY_POINTERS = {"", "null", "~"}


def table_cells(line):
    if not line.startswith("|") or not line.endswith("|"):
        raise ValueError("Table rows must start and end with a pipe")
    return [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", line[1:-1])]


def read_index(path):
    rows = []
    seen = []
    section = None
    phase = None
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("## "):
            if section is not None and phase in {"header", "separator"}:
                raise ValueError(f"Missing table in {section}: {path}:{number}")
            heading = stripped[3:].strip()
            section = heading if heading in SECTIONS else None
            phase = "header" if section else None
            if section:
                if section in seen:
                    raise ValueError(f"Duplicate section {section}: {path}:{number}")
                seen.append(section)
            continue
        if not stripped:
            if phase == "rows":
                phase = "closed"
            continue
        if stripped.startswith("|"):
            if section is None or phase == "closed":
                raise ValueError(f"Row outside section table: {path}:{number}")
            cells = table_cells(stripped)
            if phase == "header":
                if tuple(cells) != COLUMNS:
                    raise ValueError(f"Wrong columns in {section}: {path}:{number}")
                phase = "separator"
                continue
            if phase == "separator":
                if len(cells) != len(COLUMNS) or any(not re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    raise ValueError(f"Malformed table separator: {path}:{number}")
                phase = "rows"
                continue
            if len(cells) != len(COLUMNS) or any(not cell for cell in cells):
                raise ValueError(f"Malformed row: {path}:{number}")
            role, state, priority, updated, pointer, summary = cells
            link = LINK.fullmatch(pointer)
            if link is None:
                raise ValueError(f"Expected one Markdown target: {path}:{number}")
            if state not in STATES or priority not in PRIORITIES:
                raise ValueError(f"Invalid state or priority: {path}:{number}")
            if updated != "UNKNOWN":
                try:
                    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated):
                        raise ValueError
                    date.fromisoformat(updated)
                except ValueError:
                    raise ValueError(f"Invalid Updated date: {path}:{number}") from None
            target = link.group(2)
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = unquote(target)
            rows.append(dict(role=role, state=state, priority=priority, updated=updated, target=target, summary=summary, line=number, section=section))
        elif section is not None:
            if phase in {"header", "separator", "rows"}:
                raise ValueError(f"Malformed table in {section}: {path}:{number}")
            if "|" in stripped:
                raise ValueError(f"Row outside section table: {path}:{number}")
    if section is not None and phase in {"header", "separator"}:
        raise ValueError(f"Missing table in {section}: {path}")
    if tuple(seen) != SECTIONS:
        raise ValueError(f"Missing or out-of-order sections: {path}")
    return rows


def index_counts(rows):
    return {name: sum(row["section"] == section for row in rows) for name, section in SECTION_NAMES.items()}


def counts_line(rows):
    return "Counts: " + "; ".join(f"{name}={count}" for name, count in index_counts(rows).items()) + "."


def continuation_line(rows):
    count = sum(row["section"] in SECTIONS[:2] and row["line"] > 100 for row in rows)
    return f"Continuation: {count} current/reference entries beyond line 100."


def row_sort_key(row):
    updated = 0 if row["updated"] == "UNKNOWN" else -date.fromisoformat(row["updated"]).toordinal()
    key = (updated, row["role"].casefold(), row["target"])
    return (PRIORITIES[row["priority"]],) + key if row["section"] == "Current work" else key


def read_registry(root):
    registry = json.loads((root / "projects.json").read_text(encoding="utf-8"))
    if not isinstance(registry, dict):
        raise ValueError("Invalid project registry")
    entries = registry.get("projects", [])
    if not isinstance(entries, list):
        raise ValueError("Invalid project registry")
    projects = {}
    directories = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Invalid project registry entry")
        project_id = entry.get("id", "")
        directory = entry.get("plan_directory", "")
        if not isinstance(project_id, str) or not PROJECT_ID.fullmatch(project_id):
            raise ValueError("Unsafe registered project id")
        if not isinstance(directory, str) or not PROJECT_ID.fullmatch(directory):
            raise ValueError(f"Unsafe registered project directory: {project_id}")
        if project_id in projects or directory in directories:
            raise ValueError(f"Duplicate registered project: {project_id}")
        project = root / directory
        if project.resolve() != project or not project.is_dir():
            raise ValueError(f"Missing or unsafe project directory: {project_id}")
        projects[project_id] = entry
        directories.add(directory)
    temporary_shared_bundles(root, projects, registry)
    return projects


def temporary_shared_bundles(root, projects, registry=None):
    if registry is None:
        registry = json.loads((root / "projects.json").read_text(encoding="utf-8"))
    entries = registry.get("temporary_shared_bundles", [])
    if not isinstance(entries, list) or (entries and registry.get("schema_version") != 1):
        raise ValueError("Invalid temporary_shared_bundles registry")
    bundles = {}
    directories = {entry["plan_directory"] for entry in projects.values()}
    for entry in entries:
        required = {"directory", "coordinator_project", "purpose"}
        if not isinstance(entry, dict) or not required <= set(entry) or set(entry) - required - {"combined_entrypoint"}:
            raise ValueError("Invalid temporary shared bundle entry")
        combined = entry.get("combined_entrypoint")
        if "combined_entrypoint" in entry and (not isinstance(combined, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*\.md", combined)):
            raise ValueError("Unsafe temporary shared bundle combined entrypoint")
        directory = entry["directory"]
        match = SHARED_BUNDLE.fullmatch(directory) if isinstance(directory, str) else None
        if match is None:
            raise ValueError("Unsafe temporary shared bundle directory")
        try:
            date.fromisoformat(match.group(1))
        except ValueError:
            raise ValueError(f"Invalid temporary shared bundle date: {directory}") from None
        if directory in directories or directory in bundles:
            raise ValueError(f"Duplicate or colliding temporary shared bundle: {directory}")
        coordinator = entry["coordinator_project"]
        if not isinstance(coordinator, str) or coordinator not in projects:
            raise ValueError(f"Unknown temporary shared bundle coordinator: {directory}")
        if not isinstance(entry["purpose"], str) or not entry["purpose"].strip():
            raise ValueError(f"Missing temporary shared bundle purpose: {directory}")
        bundle = root / directory
        if bundle.is_symlink() or bundle.resolve() != bundle or not bundle.is_dir():
            raise ValueError(f"Missing or unsafe temporary shared bundle directory: {directory}")
        bundles[directory] = dict(projects[coordinator], plan_directory=directory, coordinator_project=coordinator)
        if combined is not None:
            bundles[directory]["combined_entrypoint"] = combined
    return bundles


def project_entry(projects, project_id):
    if not PROJECT_ID.fullmatch(project_id) or project_id not in projects:
        raise ValueError(f"Unknown or unsafe project: {project_id}")
    return projects[project_id]


def registered_owner(root, projects, path):
    for entry in [*projects.values(), *temporary_shared_bundles(root, projects).values()]:
        if path.is_relative_to(root / entry["plan_directory"]):
            return entry
    raise ValueError(f"Unsafe path outside registered project folders: {path}")


def safe_target(root, projects, entry, target):
    parsed = urlsplit(target)
    relative = Path(target)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or relative.is_absolute() or "\\" in target or not target or any(ord(char) < 32 for char in target):
        raise ValueError(f"Unsafe target: {target!r}")
    parts = relative.parts
    if ".." in parts and (parts[0] != ".." or parts.count("..") != 1 or len(parts) < 3):
        raise ValueError(f"Unsafe target traversal: {target}")
    lexical = root / entry["plan_directory"] / relative
    resolved = lexical.resolve()
    normalized = Path(normpath(lexical))
    for directory in temporary_shared_bundles(root, projects):
        bundle = root / directory
        if normalized.is_relative_to(bundle) and not resolved.is_relative_to(bundle):
            raise ValueError(f"Unsafe target outside temporary shared bundle: {target}")
    owner = registered_owner(root, projects, resolved)
    if not resolved.exists():
        raise ValueError(f"Missing target: {resolved}")
    return resolved, owner


def index_path(root, projects, entry):
    entry = projects[entry.get("coordinator_project", entry["id"])]
    path, owner = safe_target(root, projects, entry, "ROLES.md")
    if owner["id"] != entry["id"] or not path.is_file():
        raise ValueError(f"Unsafe ROLES.md: {path}")
    return path


def main_entrypoint(root, projects, entry, target):
    path, owner = safe_target(root, projects, entry, target)
    if path.is_dir():
        if not re.match(r"\d{4}-\d{2}-\d{2}-", path.name):
            raise ValueError(f"Directory navigation target is not a plan entrypoint: {path}")
        candidate = path / "plan.md"
        if not candidate.is_file():
            raise ValueError(f"Directory target needs an explicit main plan entrypoint: {path}")
        path, owner = safe_target(root, projects, owner, candidate.relative_to(root / owner["plan_directory"]).as_posix())
    if not path.is_file() or path.suffix.lower() != ".md":
        raise ValueError(f"Target is not a Markdown plan entrypoint: {path}")
    return path, owner


def read_plan(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].rstrip() != "---":
        raise ValueError(f"Missing plan frontmatter: {path}")
    fields = {}
    for number, line in enumerate(lines[1:], 1):
        if line.rstrip() == "---":
            if fields.get("status") not in {"in_progress", "complete", "superseded"}:
                raise ValueError(f"Invalid plan status: {path}")
            return fields, lines[number + 1:]
        match = FIELD.match(line)
        if match:
            name, value = match.groups()
            if name in fields:
                raise ValueError(f"Duplicate frontmatter field: {path}")
            fields[name] = value.strip().strip("\"'")
    raise ValueError(f"Unclosed plan frontmatter: {path}")


def next_action(lines, summary):
    in_status = False
    first = None
    for line in lines:
        if line.startswith("## "):
            in_status = bool(re.fullmatch(r"##\s+(?:\d+[.)]\s+)?Status\s*", line))
        elif in_status and line.strip():
            if first is None:
                first = line.strip()
            match = re.search(r"\bNext(?: step| action)?:\s*(.+)", line, re.I)
            if match:
                return match.group(1)
    return first or summary


def resolved_state(fields, owner, path, root):
    if fields["status"] in {"complete", "superseded"}:
        return fields["status"]
    relative = path.relative_to(root / owner["plan_directory"])
    if relative.parts[:2] == ("complete", "deferred"):
        return "deferred"
    if relative.parts[0] == "complete":
        if relative.as_posix() not in owner.get("live_in_complete", []):
            raise ValueError(f"Undesignated live plan inside complete/: {path}")
        return "reference"
    return "in_progress"


def resolve_role(root, projects, entry, role, runtime):
    rows = read_index(index_path(root, projects, entry))
    matches = [row for row in rows if row["role"].casefold() == role.casefold()]
    current = [row for row in matches if row["section"] in SECTIONS[:2]]
    candidates = current or matches
    if not candidates:
        raise ValueError(f"Unknown role: {role}")
    if len(candidates) != 1:
        raise ValueError(f"Ambiguous role: {role}")
    selected = candidates[0]
    path, owner = main_entrypoint(root, projects, entry, selected["target"])
    chain = []
    while True:
        if str(path) in chain:
            raise ValueError(f"Successor cycle: {path}")
        chain.append(str(path))
        fields, body = read_plan(path)
        successor = fields.get("succeeded_by", "")
        if fields["status"] == "superseded" and successor in EMPTY_POINTERS:
            raise ValueError(f"Superseded plan has no successor: {path}")
        if fields["status"] not in {"complete", "superseded"} or successor in EMPTY_POINTERS:
            break
        path, owner = main_entrypoint(root, projects, owner, unquote(successor))
    state = resolved_state(fields, owner, path, root)
    summary = selected["summary"]
    owner_rows = rows if owner["id"] == entry["id"] else read_index(index_path(root, projects, owner))
    index_owner = projects[owner.get("coordinator_project", owner["id"])]
    final_rows = []
    for row in owner_rows:
        target, _ = safe_target(root, projects, index_owner, row["target"])
        if target == path or target.is_dir() and target / "plan.md" == path:
            final_rows.append(row)
    final_rows.sort(key=lambda row: row["section"] not in SECTIONS[:2])
    final_row = selected if len(chain) == 1 else next(iter(final_rows), None)
    if final_row:
        summary = final_row["summary"]
        if state == "in_progress" and final_row["state"] in {"in_progress", "blocked", "reference"}:
            state = final_row["state"]
    elif len(chain) > 1:
        summary = next((line.strip() for line in body if line.strip() and not line.startswith("#")), "Successor plan.")
    instruction = "CLAUDE.md" if runtime == "claude" else "AGENTS.md"
    counterpart = "AGENTS.md" if runtime == "claude" else "CLAUDE.md"
    instruction_owners = [entry, owner] if "coordinator_project" in owner and entry["id"] != owner["id"] else [owner]
    source_instructions = []
    missing_source_instructions = []
    for instruction_owner in instruction_owners:
        source_root = instruction_owner.get("source_root")
        if not isinstance(source_root, str) or not source_root:
            raise ValueError(f"Missing or invalid source_root: {instruction_owner['id']}")
        source_path = Path(source_root).expanduser()
        source_path = source_path if source_path.is_absolute() else (root / source_path).resolve()
        candidates = [source_path / name for name in (instruction, counterpart)]
        available = [candidate for candidate in candidates if candidate.is_file()]
        source_instructions.extend(available)
        if not available:
            missing_source_instructions.extend(str(candidate) for candidate in candidates)
    library_reading = [root / instruction, root / "README.md"]
    for candidate in library_reading:
        if not candidate.is_file():
            raise ValueError(f"Missing library reading entrypoint: {candidate}")
    reading = source_instructions + library_reading + [index_path(root, projects, owner), path]
    if "coordinator_project" in owner:
        reading.insert(len(source_instructions) + len(library_reading), index_path(root, projects, entry))
    bundle_readme = path.parent / "README.md"
    if "combined_entrypoint" in owner:
        bundle_readme = root / owner["plan_directory"] / owner["combined_entrypoint"]
    if "coordinator_project" in owner or (path.parent != root / owner["plan_directory"] and bundle_readme.is_file() and bundle_readme != path):
        safe_readme, _ = safe_target(root, projects, owner, bundle_readme.relative_to(root / owner["plan_directory"]).as_posix())
        if not safe_readme.is_file():
            raise ValueError(f"Missing bundle README.md: {bundle_readme}")
        reading.append(safe_readme)
    result = dict(project=owner["id"], role=selected["role"], main_plan=str(path), plan_folder=str(path.parent), state=state, summary=summary, next_action=next_action(body, summary), reading_entrypoints=list(dict.fromkeys(str(item) for item in reading)), missing_source_instructions=missing_source_instructions, successor_chain=chain, recorded_successor=fields.get("succeeded_by") or None)
    if "coordinator_project" in owner:
        result.update(project=entry["id"], coordinator_project=owner["coordinator_project"])
    return result


def nonnegative(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a nonnegative integer") from None
    if number < 0:
        raise argparse.ArgumentTypeError("must be a nonnegative integer")
    return number


def page_limit(value):
    number = nonnegative(value)
    if not 1 <= number <= 100:
        raise argparse.ArgumentTypeError("must be between 1 and 100")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read project plan roles without changing the library.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    commands = parser.add_subparsers(dest="command", required=True)
    head_parser = commands.add_parser("head", help="Print the first 100 physical index lines.")
    head_parser.add_argument("project")
    list_parser = commands.add_parser("list", help="Read one bounded page of role entries.")
    list_parser.add_argument("project")
    list_parser.add_argument("--section", choices=SECTION_NAMES, default="current")
    list_parser.add_argument("--offset", type=nonnegative, default=0)
    list_parser.add_argument("--limit", type=page_limit, default=100)
    list_parser.add_argument("--json", action="store_true")
    resolve_parser = commands.add_parser("resolve", help="Resolve a stable role to its main plan and reading paths.")
    resolve_parser.add_argument("project")
    resolve_parser.add_argument("--role", required=True)
    resolve_parser.add_argument("--runtime", choices=("claude", "codex"), default="codex")
    resolve_parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        root = arguments.root.resolve()
        projects = read_registry(root)
        entry = project_entry(projects, arguments.project)
        if arguments.command == "head":
            with index_path(root, projects, entry).open(encoding="utf-8") as stream:
                sys.stdout.write("".join(islice(stream, 100)))
        elif arguments.command == "list":
            rows = read_index(index_path(root, projects, entry))
            rows = [row for row in rows if row["section"] == SECTION_NAMES[arguments.section]]
            page = rows[arguments.offset:arguments.offset + arguments.limit]
            targets = [safe_target(root, projects, entry, row["target"])[0] for row in page]
            following = arguments.offset + len(page)
            result = dict(entries=page, total=len(rows), next_offset=following if following < len(rows) else None)
            if arguments.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"Entries: {len(page)}; total: {len(rows)}; next_offset: {result['next_offset']}")
                for row, target in zip(page, targets):
                    print(f"{row['role']} | {row['state']} | {row['priority']} | {row['updated']} | {target} | {row['summary']}")
        else:
            result = resolve_role(root, projects, entry, arguments.role, arguments.runtime)
            if arguments.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                for key in ("role", "project", "main_plan", "plan_folder", "state", "summary", "next_action"):
                    print(f"{key}: {result[key]}")
                for path in result["reading_entrypoints"]:
                    print(f"Read: {path}")
                if result["missing_source_instructions"]:
                    print("Missing source instructions: " + ", ".join(result["missing_source_instructions"]))
                if len(result["successor_chain"]) > 1:
                    print("Successor chain: " + " -> ".join(result["successor_chain"]))
                if result["recorded_successor"]:
                    print(f"Recorded successor: {result['recorded_successor']}")
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
