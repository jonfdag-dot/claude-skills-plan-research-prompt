import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import date
import posixpath
from pathlib import Path
import re
from typing import Mapping
from urllib.parse import unquote, urlsplit

SOURCE_COLUMNS = ("ID", "Source", "Useful for", "Authority", "Checked", "Evidence note")
REQUIRED_FIELDS = ("Claim", "Status", "Basis", "Applies to", "Evidence", "Access", "Origin", "Recheck", "Corroboration")
ENUMS = {
    "Status": {"VERIFIED", "VENDOR CLAIM", "INFERENCE", "UNKNOWN", "PROPOSED"},
    "Basis": {"DOCUMENTED", "AUTHENTICATED", "MEASURED", "UNKNOWN"},
    "Access": {"INSPECTED", "PARTIAL", "UNAVAILABLE"},
    "State": {"current", "superseded", "rejected"},
}
ID_PATTERN = re.compile(r"R-[0-9]{4}")
LINK_PATTERN = re.compile(r"\[([^\]\n]+)\]\(([^)\n]+)\)")


@dataclass(frozen=True)
class Snapshot:
    root: str
    documents: Mapping[str, str]
    local_targets: Mapping[str, str | None]


def valid_date(value: str, allow_unknown: bool = True) -> bool:
    if allow_unknown and value == "UNKNOWN":
        return True
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def target_path(root: str, document: str, target: str) -> tuple[str, str]:
    parsed = urlsplit(target.strip("<>"))
    base = posixpath.join(root, posixpath.dirname(document))
    path = unquote(parsed.path)
    line_pointer = re.search(r":([0-9]+)$", path) if not parsed.scheme and not parsed.netloc else None
    if line_pointer is not None and int(line_pointer.group(1)) > 0:
        path = path[:line_pointer.start()]
    absolute = posixpath.normpath(posixpath.join(base, path)) if path else posixpath.join(root, document)
    return absolute, unquote(parsed.fragment)


def anchors(content: str) -> set[str]:
    result = set()
    counts: Counter[str] = Counter()
    for heading in re.findall(r"^#{1,6} (.+)$", content, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        index = counts[slug]
        counts[slug] += 1
        result.add(slug if index == 0 else f"{slug}-{index}")
    result.update(re.findall(r'<a\s+id=["\x27]([^"\x27]+)', content))
    return result


def sections(content: str) -> list[tuple[str, dict[str, str]]]:
    result = []
    for match in re.finditer(r"^## (R-[0-9]{4})\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL):
        fields = {}
        for field, value in re.findall(r"^- ([A-Za-z ]+):\s*(.*)$", match.group(2), re.MULTILINE):
            if field in fields and field != "History":
                fields[f"Duplicate {field}"] = value
            fields[field] = value.strip()
        result.append((match.group(1), fields))
    return result


def validate(snapshot: Snapshot) -> list[str]:
    errors: list[str] = []
    source_text = snapshot.documents.get("sources.md")
    if source_text is None:
        return ["sources.md: missing source register"]
    rows = [tuple(cell.strip() for cell in line.strip().strip("|").split("|")) for line in source_text.splitlines() if line.startswith("|")]
    if not rows or rows[0] != SOURCE_COLUMNS:
        errors.append("sources.md: incorrect table columns")
    source_ids: list[str] = []
    evidence_targets: dict[str, str] = {}
    source_titles: dict[str, str] = {}
    for row in rows[1:]:
        if all(re.fullmatch(r":?-+:?", cell) for cell in row):
            continue
        if len(row) != len(SOURCE_COLUMNS):
            errors.append("sources.md: row must have six columns")
            continue
        source_id, source, useful, authority, checked, evidence = row
        source_ids.append(source_id)
        if ID_PATTERN.fullmatch(source_id) is None:
            errors.append(f"sources.md: invalid ID {source_id}")
        if not useful:
            errors.append(f"{source_id}: missing Useful for")
        if authority not in {"PRIMARY", "FIRST_PARTY", "SECONDARY", "DISCOVERY"}:
            errors.append(f"{source_id}: invalid Authority {authority}")
        if not valid_date(checked):
            errors.append(f"{source_id}: invalid Checked date {checked}")
        source_match = LINK_PATTERN.fullmatch(source)
        if source_match is None:
            errors.append(f"{source_id}: Source must be a titled Markdown link")
        elif not source_match.group(1).strip() or not source_match.group(2).strip():
            errors.append(f"{source_id}: empty Source link")
        else:
            source_titles[source_id] = source_match.group(1)
        note_match = LINK_PATTERN.fullmatch(evidence)
        if note_match is None:
            errors.append(f"{source_id}: missing evidence note link")
        else:
            evidence_targets[source_id] = note_match.group(2)
            expected = rf"notes/(?:[a-z0-9]+(?:-[a-z0-9]+)*/)?[^/#]+\.md#{source_id.lower()}"
            if re.fullmatch(expected, note_match.group(2)) is None:
                errors.append(f"{source_id}: evidence note must target its canonical notes fragment")
    registered = set(source_ids)
    if source_ids != sorted(source_ids):
        errors.append("sources.md: source IDs must be sorted numerically")
    for source_id, count in Counter(source_ids).items():
        if count > 1:
            errors.append(f"{source_id}: duplicate source ID")
    found_sections: Counter[str] = Counter()
    replacements: dict[str, str] = {}
    domains = set(re.findall(r"^## ([a-z0-9]+(?:-[a-z0-9]+)*)$", snapshot.documents.get("taxonomy.md", ""), re.MULTILINE))
    domain_records: dict[str, list[tuple[str, str, str]]] = {}
    project_records: dict[str, set[str]] = {}
    target_anchors = {path: anchors(body) for path, body in snapshot.local_targets.items() if body is not None}
    for document, content in snapshot.documents.items():
        citation_text = re.sub(r"`[^`\n]+`", "", content)
        citation_text = re.sub(r"(^- Origin: IMPORTED[^\n]*?\boriginal ID )[^;\n]*", r"\1", citation_text, flags=re.MULTILINE)
        for citation in re.findall(r"\bR-[0-9]{4}\b", citation_text):
            if citation not in registered:
                errors.append(f"{document}: unknown citation {citation}")
        for title, target in LINK_PATTERN.findall(content):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme:
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    errors.append(f"{document}: invalid source link {target}")
                continue
            line_pointer = re.search(r":(-?[0-9]+)$", unquote(parsed.path)) if not parsed.netloc else None
            if line_pointer is not None and int(line_pointer.group(1)) <= 0:
                errors.append(f"{document}: local line pointer must be positive {target}")
                continue
            absolute, fragment = target_path(snapshot.root, document, target)
            if absolute not in snapshot.local_targets:
                errors.append(f"{document}: broken local link {target}")
            elif fragment:
                if fragment not in target_anchors.get(absolute, set()):
                    errors.append(f"{document}: broken local anchor {target}")
        if not document.startswith("notes/"):
            continue
        for malformed in re.findall(r"^## (R-[^\n]+)$", content, re.MULTILINE):
            if ID_PATTERN.fullmatch(malformed) is None:
                errors.append(f"{document}: malformed evidence heading {malformed}")
        for source_id, fields in sections(content):
            found_sections[source_id] += 1
            if evidence_targets.get(source_id) != f"{document}#{source_id.lower()}":
                errors.append(f"{source_id}: canonical evidence section mismatches register")
            for field in REQUIRED_FIELDS:
                if not fields.get(field):
                    errors.append(f"{source_id}: missing field {field}")
            parts = document.split("/")
            if len(parts) > 2:
                domain = parts[1]
                if len(parts) != 3 or parts[-1] == "index.md":
                    errors.append(f"{source_id}: canonical evidence must use notes/<domain>/<topic>.md")
                if domain not in domains:
                    errors.append(f"{document}: unknown domain {domain}")
                domain_records.setdefault(domain, []).append((parts[-1].removesuffix(".md").casefold(), source_titles.get(source_id, "").casefold(), source_id))
                for field in ("Tags", "Projects", "Use when", "Canonical owner"):
                    if not fields.get(field):
                        errors.append(f"{source_id}: missing field {field}")
                owner = fields.get("Canonical owner", "")
                owner_link = LINK_PATTERN.fullmatch(owner)
                if owner != "this library" and (owner_link is None or not owner_link.group(1).strip() or not owner_link.group(2).strip()):
                    errors.append(f"{source_id}: Canonical owner must be this library or a titled Markdown link")
                for field in ("Tags", "Projects"):
                    values = [value.strip() for value in fields.get(field, "").split(",")]
                    if any(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) is None for value in values):
                        errors.append(f"{source_id}: {field} must be comma-separated normalized slugs")
                    if values != sorted(set(values)):
                        errors.append(f"{source_id}: {field} must be unique and alphabetically sorted")
                for project in fields.get("Projects", "").split(","):
                    if project.strip():
                        project_records.setdefault(project.strip(), set()).add(source_id)
            for field in fields:
                if field.startswith("Duplicate "):
                    errors.append(f"{source_id}: duplicate field {field[10:]}")
            for field, allowed in ENUMS.items():
                if field in fields and fields[field] not in allowed:
                    errors.append(f"{source_id}: invalid {field} {fields[field]}")
            origin = fields.get("Origin", "")
            if not re.match(r"^(IMPORTED|LIVE)(?:;|$)", origin):
                errors.append(f"{source_id}: invalid Origin")
            if origin.startswith("IMPORTED"):
                for marker in ("original ID", "path ", "revision ", "original checked "):
                    if marker not in origin:
                        errors.append(f"{source_id}: Origin missing {marker.strip()}")
                original_date = re.search(r"original checked (UNKNOWN|[0-9-]+)", origin)
                if original_date is None or not valid_date(original_date.group(1)):
                    errors.append(f"{source_id}: invalid original checked date")
            if "Attempted" in fields and not valid_date(fields["Attempted"], False):
                errors.append(f"{source_id}: invalid Attempted date")
            replacement = fields.get("Replacement")
            if fields.get("State") == "superseded" and not replacement:
                errors.append(f"{source_id}: superseded record needs Replacement")
            if replacement is not None:
                if replacement not in registered or replacement == source_id:
                    errors.append(f"{source_id}: invalid Replacement {replacement}")
                else:
                    replacements[source_id] = replacement
            for history in re.findall(r"^- History:\s*(.*)$", content.split(f"## {source_id}\n", 1)[1].split("\n## ", 1)[0], re.MULTILINE):
                if not valid_date(history[:10], False):
                    errors.append(f"{source_id}: invalid History date")
    for source_id in registered:
        if found_sections[source_id] == 0:
            errors.append(f"{source_id}: missing canonical evidence section")
        elif found_sections[source_id] > 1:
            errors.append(f"{source_id}: duplicate evidence ID")
    for source_id in replacements:
        seen = {source_id}
        current = replacements[source_id]
        while current in replacements:
            if current in seen:
                errors.append(f"{source_id}: Replacement cycle")
                break
            seen.add(current)
            current = replacements[current]
    indexed_domains = {document.split("/")[1] for document in snapshot.documents if re.fullmatch(r"notes/[^/]+/index\.md", document)}
    for domain in sorted(set(domain_records) | indexed_domains):
        records = domain_records.get(domain, [])
        document = f"notes/{domain}/index.md"
        if domain not in domains:
            errors.append(f"{document}: unknown domain {domain}")
        if not records:
            errors.append(f"{document}: domain index has no canonical evidence")
        content = snapshot.documents.get(document)
        if content is None:
            errors.append(f"{document}: missing domain index")
            continue
        indexed = []
        for title, target in LINK_PATTERN.findall(content):
            absolute, fragment = target_path(snapshot.root, document, target)
            if re.fullmatch(r"r-[0-9]{4}", fragment):
                source_id = fragment.upper()
                indexed.append(source_id)
                expected_target = evidence_targets.get(source_id)
                if expected_target is None or (absolute, fragment) != target_path(snapshot.root, "sources.md", expected_target):
                    errors.append(f"{document}: noncanonical index target {target}")
        expected_ids = [record[2] for record in sorted(records)]
        if Counter(indexed) != Counter(expected_ids):
            errors.append(f"{document}: index records do not match domain evidence")
        elif indexed != expected_ids:
            errors.append(f"{document}: index records must sort by topic, source title, then ID")
    if domain_records:
        content = snapshot.documents.get("projects.md")
        if content is None:
            errors.append("projects.md: missing project index")
        else:
            indexed_projects: dict[str, list[str]] = {}
            for match in re.finditer(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL):
                project = match.group(1)
                if project in indexed_projects:
                    errors.append(f"projects.md: duplicate project heading {project}")
                indexed = indexed_projects.setdefault(project, [])
                for title, target in LINK_PATTERN.findall(match.group(2)):
                    absolute, fragment = target_path(snapshot.root, "projects.md", target)
                    if re.fullmatch(r"r-[0-9]{4}", fragment):
                        source_id = fragment.upper()
                        indexed.append(source_id)
                        expected_target = evidence_targets.get(source_id)
                        if expected_target is None or (absolute, fragment) != target_path(snapshot.root, "sources.md", expected_target):
                            errors.append(f"projects.md: noncanonical index target {target}")
            for project in sorted(set(project_records) | set(indexed_projects)):
                if Counter(indexed_projects.get(project, [])) != Counter(project_records.get(project, set())):
                    errors.append(f"projects.md: index records do not match project {project}")
    return sorted(set(errors))


def read_snapshot(root: Path) -> Snapshot | list[str]:
    documents = {}
    targets: dict[str, str | None] = {}
    try:
        root = root.resolve()
        if not root.is_dir():
            return [f"{root}: library root is not a directory"]
        for path in sorted(root.rglob("*.md")):
            if ".git" in path.relative_to(root).parts:
                continue
            text = path.read_text(encoding="utf-8")
            documents[path.relative_to(root).as_posix()] = text
            targets[str(path)] = text
        for document, content in documents.items():
            for title, target in LINK_PATTERN.findall(content):
                if urlsplit(target.strip("<>")).scheme:
                    continue
                absolute, fragment = target_path(str(root), document, target)
                path = Path(absolute)
                if absolute not in targets and path.exists():
                    targets[absolute] = path.read_text(encoding="utf-8") if fragment and path.is_file() else None
    except (OSError, UnicodeError, ValueError) as error:
        return [f"cannot read library: {error}"]
    return Snapshot(str(root), documents, targets)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check research library structure without fetching external sources.")
    parser.add_argument("root", type=Path)
    arguments = parser.parse_args()
    loaded = read_snapshot(arguments.root)
    diagnostics = loaded if isinstance(loaded, list) else validate(loaded)
    for diagnostic in diagnostics:
        print(diagnostic)
    if diagnostics:
        print(f"FAIL: {len(diagnostics)} integrity diagnostics")
        return 1
    print("PASS: source and evidence integrity; factual truth and external availability not checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
