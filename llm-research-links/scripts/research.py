import argparse
from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
import difflib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

SPEC = importlib.util.spec_from_file_location("research_validate", Path(__file__).with_name("validate.py"))
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("validator module unavailable")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

KINDS = ("domain", "tag", "project", "authority", "status", "basis", "access", "state")
LABEL_KINDS = ("domain", "tag", "project")
AUTHORITIES = ("PRIMARY", "FIRST_PARTY", "SECONDARY", "DISCOVERY")
MAX_ENTITIES = 3
MIN_LIMIT = 1
MAX_LIMIT = 25
GENERIC_TAGS = {"evidence", "historical-research", "references", "shared", "source-list", "stacks"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SECTION_ORDER = ("Claim", "Status", "Basis", "Applies to", "Evidence", "Access", "Origin", "Recheck", "Corroboration", "Limitations", "Attempted", "State", "Replacement", "Tags", "Projects", "Use when", "Canonical owner")
REGISTER_KEYS = ("Source title", "Source URL", "Useful for", "Authority", "Checked", "Domain", "Topic")
VOLATILE_TERMS = ("pricing", "price", "rate limit", "rate-limit", "quota", "retention")
OUTCOMES = ("inspected", "changed", "partial", "blocked", "dead", "empty")
ADVANCING = ("inspected", "changed")
OUTCOME_TEXT = {
    "inspected": "page loaded with on-topic content and a quoted passage consistent with the claim topic; claim details not individually verified",
    "changed": "page loaded but its content differs from the retained claim; record not rewritten, review before reuse",
    "partial": "page loaded but the retained claim could not be confirmed; Checked not advanced",
    "blocked": "fetch blocked, paywalled or rate limited; Checked not advanced",
    "dead": "page not found or domain unreachable after retry; Checked not advanced",
    "empty": "page loaded without usable content (empty, login wall, parked or unrelated); Checked not advanced",
}
WEIGHTS = {"title": 3, "Claim": 2, "Use when": 2, "Tags": 2, "useful": 1, "Applies to": 1, "Evidence": 1}


class LibraryError(Exception):
    pass


@dataclass
class Record:
    id: str
    title: str
    url: str
    useful: str
    authority: str
    checked: str
    document: str = ""
    fields: dict[str, str] = field(default_factory=dict)

    @property
    def domain(self) -> str:
        parts = self.document.split("/")
        return parts[1] if len(parts) == 3 else ""

    @property
    def tags(self) -> list[str]:
        return split_labels(self.fields.get("Tags", ""))

    @property
    def projects(self) -> list[str]:
        return split_labels(self.fields.get("Projects", ""))

    @property
    def state(self) -> str:
        return self.fields.get("State", "current")

    def labels(self, kind: str) -> list[str]:
        if kind == "domain":
            return [self.domain] if self.domain else []
        if kind == "tag":
            return self.tags
        if kind == "project":
            return self.projects
        if kind == "authority":
            return [self.authority]
        if kind == "state":
            return [self.state]
        value = self.fields.get(kind.capitalize())
        return [value] if value else []


@dataclass
class Entity:
    text: str
    matches: list[tuple[str, str]]

    def accepts(self, record: Record) -> bool:
        return any(value.casefold() in {label.casefold() for label in record.labels(kind)} for kind, value in self.matches)

    def describe(self) -> str:
        return " or ".join(f"{kind}:{value}" for kind, value in self.matches)


@dataclass
class Topic:
    name: str
    entities: list[str]
    terms: list[str]
    use_for: str


@dataclass
class Library:
    root: Path
    snapshot: object
    records: dict[str, Record]
    domains: list[str]
    aliases: dict[str, list[str]]
    topics: dict[str, Topic] = field(default_factory=dict)

    def vocabulary(self, kind: str) -> Counter:
        counts: Counter = Counter()
        for record in self.records.values():
            counts.update(record.labels(kind))
        if kind == "domain":
            counts.update({domain: 0 for domain in self.domains})
        if kind == "authority":
            counts.update({value: 0 for value in AUTHORITIES})
        if kind in ("status", "basis", "access", "state"):
            counts.update({value: 0 for value in VALIDATOR.ENUMS[kind.capitalize()]})
        return counts


def split_labels(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def register_rows(text: str) -> list[tuple[str, ...]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("| R-"):
            continue
        rows.append(tuple(cell.strip() for cell in line.strip().strip("|").split("|")))
    return rows


def load(root: Path) -> Library:
    loaded = VALIDATOR.read_snapshot(root)
    if isinstance(loaded, list):
        raise LibraryError("; ".join(loaded))
    documents = loaded.documents
    if "sources.md" not in documents:
        raise LibraryError("sources.md: missing source register")
    records: dict[str, Record] = {}
    for row in register_rows(documents["sources.md"]):
        if len(row) != 6:
            continue
        source_id, source, useful, authority, checked, _ = row
        link = VALIDATOR.LINK_PATTERN.fullmatch(source)
        title, url = (link.group(1), link.group(2).strip("<>")) if link else (source, "")
        records[source_id] = Record(source_id, title, url, useful, authority, checked)
    for document, content in documents.items():
        if not document.startswith("notes/") or document.endswith(("README.md", "index.md")):
            continue
        for source_id, fields in VALIDATOR.sections(content):
            if source_id in records:
                records[source_id].document = document
                records[source_id].fields = fields
    taxonomy = documents.get("taxonomy.md", "")
    domains = re.findall(r"^## ([a-z0-9]+(?:-[a-z0-9]+)*)$", taxonomy, re.MULTILINE)
    aliases: dict[str, list[str]] = {}
    alias_line = re.search(r"^Aliases:\s*(.+)$", taxonomy, re.MULTILINE)
    for entry in (alias_line.group(1).split(";") if alias_line else []):
        if "→" not in entry:
            continue
        name, targets = entry.split("→", 1)
        aliases[name.strip().casefold()] = [domain for domain in domains if re.search(rf"\b{re.escape(domain)}\b", targets)]
    topics: dict[str, Topic] = {}
    for line in documents.get("topics.md", "").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not line.startswith("| ") or len(cells) != 4 or "/" not in cells[0] or cells[0].startswith("-"):
            continue
        topics[cells[0]] = Topic(cells[0], split_labels(cells[1]), split_labels(cells[2]), cells[3])
    return Library(root.resolve(), loaded, records, domains, aliases, topics)


def suggestions(library: Library, text: str) -> list[str]:
    labels = []
    for kind in LABEL_KINDS:
        labels.extend(f"{kind}:{value}" for value in library.vocabulary(kind))
    bare = [label.split(":", 1)[1] for label in labels]
    close = difflib.get_close_matches(text.casefold(), bare, n=6, cutoff=0.6)
    contained = [value for value in bare if text.casefold() in value or value in text.casefold()][:6]
    picked = list(dict.fromkeys(close + contained))[:8]
    return [label for label in labels if label.split(":", 1)[1] in picked][:8]


def resolve(library: Library, text: str) -> Entity:
    text = text.strip()
    if ":" in text and text.split(":", 1)[0].casefold() in KINDS:
        kind, value = text.split(":", 1)
        kind = kind.casefold()
        vocabulary = library.vocabulary(kind)
        exact = [label for label in vocabulary if label.casefold() == value.strip().casefold()]
        if kind == "domain" and not exact and value.strip().casefold() in library.aliases:
            exact = library.aliases[value.strip().casefold()]
        if not exact:
            close = difflib.get_close_matches(value.strip(), list(vocabulary), n=6, cutoff=0.5)
            raise LibraryError(f"unknown {kind} '{value.strip()}'; closest: {', '.join(close) or 'none'}; run labels --kind {kind}")
        return Entity(text, [(kind, label) for label in exact])
    lowered = text.casefold()
    matches: list[tuple[str, str]] = []
    if lowered in library.aliases:
        matches.extend(("domain", domain) for domain in library.aliases[lowered])
    for kind in LABEL_KINDS:
        if lowered in {label.casefold() for label in library.vocabulary(kind)}:
            matches.append((kind, lowered))
    if not matches:
        raise LibraryError(f"unknown entity '{text}'; closest labels: {', '.join(suggestions(library, text)) or 'none'}; run labels")
    return Entity(text, list(dict.fromkeys(matches)))


def topic_entities(library: Library, name: str | None) -> tuple[list[str], list[str]]:
    if not name:
        return [], []
    topic = library.topics.get(name)
    if topic is None:
        close = difflib.get_close_matches(name, list(library.topics), n=5, cutoff=0.4)
        raise LibraryError(f"unknown topic '{name}'; closest: {', '.join(close) or 'none'}; run topics")
    return topic.entities, topic.terms


def resolve_all(library: Library, texts: list[str], minimum: int) -> list[Entity]:
    if not minimum <= len(texts) <= MAX_ENTITIES:
        raise LibraryError(f"pick {minimum} to {MAX_ENTITIES} entities with --entity or --topic (a topic counts its entities); got {len(texts)}")
    return [resolve(library, text) for text in texts]


def pool(library: Library, entities: list[Entity], include_retired: bool, checked_before: str | None = None) -> list[Record]:
    result = []
    for record in library.records.values():
        if not include_retired and record.state in ("superseded", "rejected"):
            continue
        if checked_before and record.checked != "UNKNOWN" and record.checked >= checked_before:
            continue
        if all(entity.accepts(record) for entity in entities):
            result.append(record)
    return result


def score(record: Record, terms: list[str], require_all: bool = True) -> int:
    texts = {"title": record.title, "useful": record.useful}
    texts.update({name: record.fields.get(name, "") for name in WEIGHTS if name not in texts})
    total = 0
    for term in terms:
        hits = sum(weight for name, weight in WEIGHTS.items() if term in texts[name].casefold())
        if hits == 0 and require_all:
            return 0
        total += hits
    return total


def rank(records: list[Record], terms: list[str], require_all: bool) -> list[Record]:
    scored = [(score(record, terms, require_all), record) for record in records]
    return [record for value, record in sorted(scored, key=lambda item: (-item[0], -int(item[1].id[2:]))) if value > 0]


def limit_value(text: str) -> int:
    value = int(text)
    if not MIN_LIMIT <= value <= MAX_LIMIT:
        raise argparse.ArgumentTypeError(f"limit must be {MIN_LIMIT}-{MAX_LIMIT}; narrow the pool instead of printing more")
    return value


def clip(text: str, size: int) -> str:
    return text if len(text) <= size else text[: size - 1].rstrip() + "…"


def print_record(record: Record) -> None:
    state = "" if record.state == "current" else f" STATE={record.state}->{record.fields.get('Replacement', '?')}"
    status = "/".join(record.fields.get(name, "?") for name in ("Status", "Basis", "Access"))
    print(f"{record.id}  {record.authority}  checked {record.checked}  {status}  {record.domain}{state}")
    print(f"  {clip(record.title, 160)}")
    print(f"  claim: {clip(record.fields.get('Claim', ''), 240)}")
    print(f"  use when: {clip(record.fields.get('Use when', ''), 200)}")
    print(f"  tags: {', '.join(record.tags)} | projects: {', '.join(record.projects)}")
    print(f"  open: {record.document}#{record.id.lower()}")


def next_entities(records: list[Record], entities: list[Entity], limit: int) -> list[str]:
    used = {(kind, value.casefold()) for entity in entities for kind, value in entity.matches}
    counts: Counter = Counter()
    for record in records:
        for kind in LABEL_KINDS:
            counts.update(f"{kind}:{label}" for label in record.labels(kind) if (kind, label.casefold()) not in used)
    redundant = {f"tag:{domain}" for record in records for domain in [record.domain]} | {f"tag:{tag}" for tag in GENERIC_TAGS}
    return [f"{label} ({count})" for label, count in counts.most_common() if count < len(records) and label not in redundant][:limit]


def command_find(library: Library, args: argparse.Namespace) -> int:
    extra, topic_terms = topic_entities(library, args.topic)
    entities = resolve_all(library, extra + args.entity, 1)
    candidates = pool(library, entities, args.include_retired, args.checked_before)
    terms = [term.casefold() for term in args.terms]
    stale = f" checked before {args.checked_before} or UNKNOWN" if args.checked_before else ""
    print(f"pool: {len(candidates)} records for {' AND '.join(entity.describe() for entity in entities)}{stale}")
    if terms:
        hits = rank(candidates, terms, True)
        print(f"matches for all terms {' + '.join(terms)}: {len(hits)}")
        if not hits:
            hits = rank(candidates, terms, False)
            print(f"fallback, matches for any term: {len(hits)}")
    elif topic_terms:
        matched = rank(candidates, [term.casefold() for term in topic_terms], False)
        matched_ids = {record.id for record in matched}
        rest = [record for record in candidates if record.id not in matched_ids]
        hits = matched + sorted(rest, key=lambda record: record.id, reverse=True)
        print(f"ranked by topic terms {', '.join(topic_terms)}: {len(matched)} match")
    else:
        hits = sorted(candidates, key=lambda record: (record.checked if record.checked != "UNKNOWN" else "", record.id), reverse=True)
    for record in hits[: args.limit]:
        print()
        print_record(record)
    if len(hits) > args.limit:
        print()
        print(f"{len(hits) - args.limit} more; narrow with terms or swap in a sharper entity: {', '.join(next_entities(hits, entities, 8))}")
    if not hits:
        print("no records in this pool; relaxing one entity at a time:")
        for position, entity in enumerate(entities):
            others = entities[:position] + entities[position + 1:]
            relaxed = pool(library, others, args.include_retired, args.checked_before)
            count = len(rank(relaxed, terms, True) or rank(relaxed, terms, False)) if terms else len(relaxed)
            kept = " AND ".join(other.describe() for other in others) or "whole library"
            print(f"  drop {entity.describe()}: {count} matches in {kept}")
        print("rerun with the relaxed entities, or a sibling label from: python3 -B scripts/research.py labels --entity <kept entity>")
    return 0


def command_labels(library: Library, args: argparse.Namespace) -> int:
    entities = resolve_all(library, topic_entities(library, args.topic)[0] + args.entity, 0)
    records = pool(library, entities, args.include_retired)
    kinds = [args.kind] if args.kind else list(KINDS)
    if entities:
        print(f"pool: {len(records)} records for {' AND '.join(entity.describe() for entity in entities)}")
    for kind in kinds:
        counts: Counter = Counter()
        for record in records:
            counts.update(record.labels(kind))
        if not entities:
            counts.update({label: 0 for label in library.vocabulary(kind)})
        items = [(label, count) for label, count in counts.most_common() if not args.match or args.match.casefold() in label.casefold()]
        shown = items[: args.limit]
        print(f"\n{kind} ({len(items)} labels{', showing ' + str(len(shown)) if len(shown) < len(items) else ''})")
        print("  " + ", ".join(f"{label} {count}" for label, count in shown))
    if not entities and not args.kind:
        print("\naliases: " + "; ".join(f"{name} → {' | '.join(targets)}" for name, targets in sorted(library.aliases.items())))
    return 0


def command_show(library: Library, args: argparse.Namespace) -> int:
    documents = library.snapshot.documents
    status = 0
    for key in args.keys:
        matches = [library.records[key.upper()]] if key.upper() in library.records else [record for record in library.records.values() if record.url.rstrip("/") == key.rstrip("/")]
        if not matches and not re.fullmatch(r"R-[0-9]+", key.upper()):
            partial = sorted((record for record in library.records.values() if key.casefold() in record.url.casefold()), key=lambda record: record.id, reverse=True)
            if partial:
                print(f"{key}: no exact source; {len(partial)} registered URLs contain it")
                for record in partial[:MAX_LIMIT]:
                    print(f"  {record.id}  {record.domain}  {clip(record.title, 90)}  {record.url}")
                if len(partial) > MAX_LIMIT:
                    print(f"  {len(partial) - MAX_LIMIT} more; use a longer URL fragment")
                print()
                continue
        if not matches:
            print(f"{key}: no register record")
            status = 1
            continue
        for record in matches:
            print(f"| {record.id} | [{record.title}]({record.url}) | {record.useful} | {record.authority} | {record.checked} |")
            content = documents.get(record.document, "")
            section = re.search(rf"^## {record.id}\n.*?(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
            print(section.group(0).rstrip() if section else f"{record.id}: missing canonical section")
            replacement = record.fields.get("Replacement")
            if replacement:
                print(f"-> replacement {replacement}: python3 -B scripts/research.py show {replacement}")
            print()
    return status


def require_text(item: dict, key: str, cell: bool = False) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise LibraryError(f"missing {key}")
    if "\n" in value or (cell and "|" in value):
        raise LibraryError(f"{key} must be one line{' without |' if cell else ''}")
    return value.strip()


def label_list(item: dict, key: str) -> list[str]:
    value = item.get(key)
    values = split_labels(value) if isinstance(value, str) else value
    if not isinstance(values, list) or not values or not all(isinstance(entry, str) for entry in values):
        raise LibraryError(f"{key} must be a non-empty list of slugs")
    values = sorted({entry.strip() for entry in values})
    bad = [entry for entry in values if SLUG.fullmatch(entry) is None]
    if bad:
        raise LibraryError(f"{key} not normalized slugs: {', '.join(bad)}")
    return values


def check_new_labels(library: Library, kind: str, values: list[str], allowed: bool) -> None:
    known = set(library.vocabulary(kind))
    new = [value for value in values if value not in known]
    if new and not allowed:
        hints = "; ".join(f"{value} ~ {', '.join(difflib.get_close_matches(value, list(known), n=4, cutoff=0.5)) or 'none'}" for value in new)
        raise LibraryError(f"new {kind} labels {', '.join(new)} (closest existing: {hints}); reuse an existing label or pass --new-label")


def index_key(library: Library, line: str, pending: dict[str, str]) -> tuple[str, str, str]:
    match = re.search(r"\]\(([^)#]+)\.md#(r-[0-9]{4})\)", line)
    if match is None:
        return ("", "", "")
    source_id = match.group(2).upper()
    title = pending.get(source_id) or (library.records[source_id].title if source_id in library.records else "")
    return (Path(match.group(1)).name.casefold(), title.casefold(), source_id)


def insert_index(library: Library, content: str, line: str, pending: dict[str, str]) -> str:
    lines = content.rstrip("\n").split("\n")
    bullets = [position for position, text in enumerate(lines) if text.startswith("- [")]
    if not bullets:
        return content.rstrip("\n") + "\n\n" + line + "\n"
    keys = [index_key(library, lines[position], pending) for position in bullets]
    slot = bisect_right(keys, index_key(library, line, pending))
    position = bullets[slot] if slot < len(bullets) else bullets[-1] + 1
    lines.insert(position, line)
    return "\n".join(lines) + "\n"


def add_project_pointer(content: str, project: str, line: str) -> str:
    headings = list(re.finditer(r"^## ([^\n]+)$", content, re.MULTILINE))
    for heading in headings:
        if heading.group(1) == project:
            insert_at = heading.end() + 1
            if content[insert_at:insert_at + 1] == "\n":
                insert_at += 1
            return content[:insert_at] + line + "\n" + content[insert_at:]
    names = [heading.group(1) for heading in headings]
    slot = bisect_right(names, project)
    block = f"## {project}\n\n{line}\n\n"
    if slot < len(headings):
        start = headings[slot].start()
        return content[:start] + block + content[start:]
    return content.rstrip("\n") + "\n\n" + block.rstrip("\n") + "\n"


def remove_project_pointer(content: str, project: str, source_id: str) -> str:
    match = re.search(rf"^## {re.escape(project)}\n.*?(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
    if match is None:
        return content
    body = re.sub(rf"^- \[[^\n]*\]\([^)\n]*#{source_id.lower()}\)\n", "", match.group(0), flags=re.MULTILINE)
    return content[: match.start()] + body + content[match.end():]


def commit(library: Library, changes: dict[str, str], dry_run: bool) -> list[str]:
    snapshot = library.snapshot
    baseline = set(VALIDATOR.validate(snapshot))
    documents = dict(snapshot.documents)
    targets = dict(snapshot.local_targets)
    for document, text in changes.items():
        documents[document] = text
        targets[str(library.root / document)] = text
    after = set(VALIDATOR.validate(VALIDATOR.Snapshot(snapshot.root, documents, targets)))
    introduced = sorted(after - baseline)
    if introduced:
        raise LibraryError("write refused, it would introduce integrity diagnostics:\n" + "\n".join(introduced))
    if not dry_run:
        for document, text in changes.items():
            path = library.root / document
            temporary = path.with_name(f".{path.name}.tmp")
            temporary.write_text(text, encoding="utf-8")
            os.replace(temporary, path)
    if baseline:
        print(f"note: {len(baseline)} pre-existing diagnostics unchanged; run scripts/validate.py")
    return sorted(changes)


def section_text(source_id: str, item: dict, tags: list[str], projects: list[str]) -> str:
    lines = [f"## {source_id}", ""]
    for name in SECTION_ORDER:
        if name == "Tags":
            lines.append(f"- Tags: {', '.join(tags)}")
        elif name == "Projects":
            lines.append(f"- Projects: {', '.join(projects)}")
        elif name in item:
            lines.append(f"- {name}: {require_text(item, name)}")
    history = item.get("History", [])
    for entry in [history] if isinstance(history, str) else history:
        lines.append(f"- History: {entry.strip()}")
    return "\n".join(lines) + "\n"


def command_add(library: Library, args: argparse.Namespace) -> int:
    try:
        payload = json.loads(Path(args.packet).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise LibraryError(f"cannot read packet: {error}")
    items = payload.get("records") if isinstance(payload, dict) and "records" in payload else payload
    items = [items] if isinstance(items, dict) else items
    if not isinstance(items, list) or not items:
        raise LibraryError("packet must be a record object, a list, or {\"records\": [...]}")
    documents = library.snapshot.documents
    changes: dict[str, str] = {}
    pending: dict[str, str] = {}
    next_number = max((int(source_id[2:]) for source_id in library.records), default=0) + 1
    rows = []
    project_lines: list[tuple[str, str]] = []
    seen_urls: dict[str, str] = {}
    for position, item in enumerate(items, 1):
        if not isinstance(item, dict):
            raise LibraryError(f"record {position}: must be an object")
        try:
            title, url, useful = (require_text(item, key, True) for key in REGISTER_KEYS[:3])
            authority, checked, domain, topic = (require_text(item, key, True) for key in REGISTER_KEYS[3:])
            for name in VALIDATOR.REQUIRED_FIELDS + ("Use when", "Canonical owner"):
                require_text(item, name)
            tags, projects = label_list(item, "Tags"), label_list(item, "Projects")
        except LibraryError as error:
            raise LibraryError(f"record {position}: {error}")
        if domain not in library.domains and len(library.aliases.get(domain.casefold(), [])) == 1:
            domain = library.aliases[domain.casefold()][0]
        if domain not in library.domains:
            raise LibraryError(f"record {position}: unknown domain {domain}; choose from {', '.join(library.domains)}")
        if SLUG.fullmatch(topic) is None or topic in ("index", "readme"):
            raise LibraryError(f"record {position}: Topic must be a descriptive lowercase slug filename without .md")
        if authority not in AUTHORITIES:
            raise LibraryError(f"record {position}: Authority must be one of {', '.join(AUTHORITIES)}")
        duplicates = [record.id for record in library.records.values() if record.url.rstrip("/") == url.rstrip("/")]
        if url.rstrip("/") in seen_urls:
            duplicates.append(seen_urls[url.rstrip("/")])
        if duplicates and not args.allow_same_source:
            raise LibraryError(f"record {position}: source already registered as {', '.join(duplicates)}; reuse it (show {duplicates[0]}) or pass --allow-same-source for a distinct claim scope")
        check_new_labels(library, "tag", tags, args.new_label)
        check_new_labels(library, "project", projects, args.new_label)
        source_id = f"R-{next_number:04d}"
        next_number += 1
        seen_urls[url.rstrip("/")] = source_id
        pending[source_id] = title
        document = f"notes/{domain}/{topic}.md"
        current = changes.get(document, documents.get(document))
        if current is None:
            heading = item.get("Topic title")
            summary = item.get("Topic summary")
            if not isinstance(heading, str) or not isinstance(summary, str) or not heading.strip() or not summary.strip():
                raise LibraryError(f"record {position}: new topic {document} needs Topic title and Topic summary")
            current = f"# {heading.strip()}\n\n{summary.strip()}\n"
        changes[document] = current.rstrip("\n") + "\n\n" + section_text(source_id, item, tags, projects)
        rows.append(f"| {source_id} | [{title}]({url}) | {useful} | {authority} | {checked} | [Evidence]({document}#{source_id.lower()}) |")
        index = f"notes/{domain}/index.md"
        changes[index] = insert_index(library, changes.get(index, documents.get(index, f"# {domain}\n")), f"- [{title} — {source_id}]({topic}.md#{source_id.lower()})", pending)
        project_lines.extend((project, f"- [{title} — {source_id}]({document}#{source_id.lower()})") for project in projects)
    changes["sources.md"] = documents["sources.md"].rstrip("\n") + "\n" + "\n".join(rows) + "\n"
    projects_text = documents.get("projects.md", "# Browse by project\n")
    for project, line in reversed(project_lines):
        projects_text = add_project_pointer(projects_text, project, line)
    changes["projects.md"] = projects_text
    written = commit(library, changes, args.dry_run)
    print(f"{'DRY RUN, nothing written; would save' if args.dry_run else 'saved'} {', '.join(pending)}")
    print(f"files ({len(written)}): " + (", ".join(written) if len(written) <= 10 else ", ".join(written[:10]) + ", ..."))
    return 0


def relabel_one(library: Library, record: Record, change: dict[str, list[str]], reason: str, documents: dict[str, str]) -> str:
    tags = sorted((set(record.tags) | set(change["add_tag"])) - set(change["remove_tag"]))
    projects = sorted((set(record.projects) | set(change["add_project"])) - set(change["remove_project"]))
    if not tags or not projects:
        raise LibraryError(f"{record.id}: a record keeps at least one tag and one project")
    if tags == record.tags and projects == record.projects:
        return ""
    content = documents[record.document]
    match = re.search(rf"^## {record.id}\n.*?(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
    if match is None:
        raise LibraryError(f"{record.id}: section not found")
    body = re.sub(r"^- Tags:.*$", f"- Tags: {', '.join(tags)}", match.group(0), count=1, flags=re.MULTILINE)
    body = re.sub(r"^- Projects:.*$", f"- Projects: {', '.join(projects)}", body, count=1, flags=re.MULTILINE)
    delta = [f"+tag {value}" for value in sorted(set(tags) - set(record.tags))] + [f"-tag {value}" for value in sorted(set(record.tags) - set(tags))]
    delta += [f"+project {value}" for value in sorted(set(projects) - set(record.projects))] + [f"-project {value}" for value in sorted(set(record.projects) - set(projects))]
    body = body.rstrip("\n") + f"\n- History: {date.today().isoformat()} — Relabeled {', '.join(delta)}; {reason}\n"
    trailing = "\n" if match.end() < len(content) else ""
    documents[record.document] = content[: match.start()] + body + trailing + content[match.end():]
    projects_text = documents.get("projects.md", "")
    line = f"- [{record.title} — {record.id}]({record.document}#{record.id.lower()})"
    for project in sorted(set(record.projects) - set(projects)):
        projects_text = remove_project_pointer(projects_text, project, record.id)
    for project in sorted(set(projects) - set(record.projects)):
        projects_text = add_project_pointer(projects_text, project, line)
    documents["projects.md"] = projects_text
    return ", ".join(delta)


CHANGE_KEYS = ("add_tag", "remove_tag", "add_project", "remove_project")


def relabel_changes(args: argparse.Namespace) -> dict[str, dict[str, list[str]]]:
    flags = {key: getattr(args, key) for key in CHANGE_KEYS}
    if args.plan:
        if args.ids or any(flags.values()):
            raise LibraryError("--plan replaces IDs and label flags; pass one or the other")
        try:
            plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise LibraryError(f"cannot read plan: {error}")
        if not isinstance(plan, dict) or not plan:
            raise LibraryError("plan must map R-IDs to {add_tag, remove_tag, add_project, remove_project} lists")
        changes = {}
        for key, change in plan.items():
            if not isinstance(change, dict) or set(change) - set(CHANGE_KEYS) or not all(isinstance(value, list) and all(isinstance(item, str) for item in value) for value in change.values()):
                raise LibraryError(f"{key}: plan entry must use only {', '.join(CHANGE_KEYS)} string lists")
            changes[key.upper()] = {name: change.get(name, []) for name in CHANGE_KEYS}
        return changes
    if not args.ids:
        raise LibraryError("pass record IDs or --plan")
    return {key.upper(): flags for key in args.ids}


def command_relabel(library: Library, args: argparse.Namespace) -> int:
    changes_by_id = relabel_changes(args)
    for kind in ("tag", "project"):
        values = sorted({value for change in changes_by_id.values() for value in change[f"add_{kind}"]})
        bad = [value for value in values if SLUG.fullmatch(value) is None]
        if bad:
            raise LibraryError(f"{kind} not normalized slugs: {', '.join(bad)}")
        check_new_labels(library, kind, values, args.new_label)
    records = []
    for key in changes_by_id:
        record = library.records.get(key)
        if record is None or not record.document:
            raise LibraryError(f"{key}: no canonical record")
        records.append(record)
    documents = dict(library.snapshot.documents)
    changed = {}
    for record in records:
        delta = relabel_one(library, record, changes_by_id[record.id], args.reason.strip(), documents)
        if delta:
            changed[record.id] = delta
        else:
            print(f"{record.id}: labels unchanged")
    if not changed:
        return 0
    changes = {document: text for document, text in documents.items() if text != library.snapshot.documents.get(document)}
    written = commit(library, changes, args.dry_run)
    verb = "DRY RUN, nothing written; would relabel" if args.dry_run else "relabeled"
    shown = list(changed.items()) if len(changed) <= 25 else list(changed.items())[:10]
    for source_id, delta in shown:
        print(f"{verb} {source_id}: {delta}")
    if len(shown) < len(changed):
        print(f"... and {len(changed) - len(shown)} more ({verb} {len(changed)} records)")
    print(f"files ({len(written)}): " + (", ".join(written) if len(written) <= 10 else ", ".join(written[:10]) + ", ..."))
    return 0


def command_topics(library: Library, args: argparse.Namespace) -> int:
    failures = 0
    names = [name for name in library.topics if not args.project or name.startswith(f"{args.project}/")]
    if not names:
        raise LibraryError(f"no topics{' for ' + args.project if args.project else ''} in topics.md")
    for name in names:
        topic = library.topics[name]
        try:
            entities = resolve_all(library, topic.entities, 1)
        except LibraryError as error:
            failures += 1
            print(f"{name}: BROKEN {error}")
            continue
        candidates = pool(library, entities, False)
        matched = rank(candidates, [term.casefold() for term in topic.terms], False)
        problem = "EMPTY POOL" if not candidates else "NO TERM MATCH" if topic.terms and not matched else ""
        failures += bool(problem)
        print(f"{name:42} pool {len(candidates):4}  term hits {len(matched):4}  {problem or clip(topic.use_for, 70)}")
    if args.check and failures:
        print(f"FAIL: {failures} topics need repair in topics.md")
        return 1
    return 0


def command_audit(library: Library, args: argparse.Namespace) -> int:
    projects = args.project or sorted(set(library.vocabulary("project")))
    print("project            records  generic-use-when  status-unknown  weak-tags  distinct-tags  single-use-tags")
    for project in projects:
        records = [record for record in library.records.values() if project in record.projects and record.state == "current"]
        total = max(len(records), 1)
        boiler = sum("Consult this scoped source" in record.fields.get("Use when", "") for record in records)
        unknown = sum(record.fields.get("Status") == "UNKNOWN" for record in records)
        weak = sum(all(tag in library.domains or tag in GENERIC_TAGS for tag in record.tags) for record in records)
        tags = Counter(tag for record in records for tag in record.tags)
        single = sum(1 for count in tags.values() if count == 1)
        print(f"{project:18} {len(records):7}  {boiler * 100 // total:15}%  {unknown * 100 // total:13}%  {weak * 100 // total:8}%  {len(tags):13}  {single:15}")
    print("weak-tags = only domain-name or generic tags; improve labels with relabel when real work uses a record")
    return 0


def command_template(library: Library, args: argparse.Namespace) -> int:
    record = {key: "" for key in REGISTER_KEYS}
    record.update({"Authority": "|".join(AUTHORITIES), "Checked": "YYYY-MM-DD|UNKNOWN", "Domain": "|".join(library.domains), "Topic": "descriptive-topic-slug"})
    for name in VALIDATOR.REQUIRED_FIELDS:
        record[name] = "|".join(sorted(VALIDATOR.ENUMS[name])) if name in VALIDATOR.ENUMS else ""
    record["Origin"] = "LIVE; <retrieval method> YYYY-MM-DD; <task and how it informed it>"
    record.update({"Tags": ["existing-tag"], "Projects": ["cross-project|example-project|..."], "Use when": "", "Canonical owner": "this library"})
    record.update({"Limitations": "optional", "Topic title": "only for a new topic file", "Topic summary": "only for a new topic file"})
    print(json.dumps({"records": [record]}, indent=2, ensure_ascii=False))
    return 0


def recheck_tranche(record: Record) -> int:
    text = " ".join((record.title, record.fields.get("Use when", ""), record.fields.get("Claim", ""), " ".join(record.tags))).casefold()
    if any(term in text for term in VOLATILE_TERMS):
        return 1
    return 2 if record.checked != "UNKNOWN" else 3


def command_queue(library: Library, args: argparse.Namespace) -> int:
    today = date.today().isoformat()
    due = []
    for record in library.records.values():
        if record.state != "current" or not record.url.startswith("http"):
            continue
        if record.checked == today or record.fields.get("Attempted") == today:
            continue
        tranche = recheck_tranche(record)
        if args.tranche and tranche != args.tranche:
            continue
        due.append((tranche, urlsplit(record.url).netloc.casefold(), record.id, record))
    due.sort(key=lambda item: item[:3])
    counts = Counter(item[0] for item in due)
    print(f"due: {len(due)} records; tranche 1 volatile {counts[1]}, tranche 2 dated {counts[2]}, tranche 3 never inspected {counts[3]}")
    if not args.output_dir:
        return 0
    directory = Path(args.output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    batches = [due[start:start + args.batch_size] for start in range(0, len(due), args.batch_size)]
    for number, batch in enumerate(batches, 1):
        items = [{"id": record.id, "url": record.url, "title": clip(record.title, 120), "claim": clip(record.fields.get("Claim", ""), 300), "authority": record.authority, "access": record.fields.get("Access", ""), "checked": record.checked, "tranche": tranche} for tranche, _, _, record in batch]
        (directory / f"batch-{number:04d}.json").write_text(json.dumps(items, indent=0, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {len(batches)} batches of up to {args.batch_size} to {directory}")
    return 0


def one_line(text: object, size: int) -> str:
    return clip(" ".join(str(text).split()), size)


def set_field(body: str, name: str, value: str, after: str) -> str:
    pattern = re.compile(rf"^- {name}:.*$", re.MULTILINE)
    if pattern.search(body):
        return pattern.sub(lambda match: f"- {name}: {value}", body, count=1)
    anchor = re.search(rf"^- {after}:.*$", body, re.MULTILINE)
    if anchor is None:
        raise LibraryError(f"cannot place {name}: missing {after}")
    return body[: anchor.end()] + f"\n- {name}: {value}" + body[anchor.end():]


def set_register_checked(text: str, source_id: str, day: str) -> str:
    pattern = re.compile(rf"^\| {source_id} \|.*$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        raise LibraryError(f"{source_id}: register row not found")
    cells = match.group(0).strip().strip("|").split("|")
    cells[4] = f" {day} "
    return text[: match.start()] + "|" + "|".join(cells) + "|" + text[match.end():]


def load_json(path: str, label: str) -> object:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise LibraryError(f"cannot read {label} {path}: {error}")


def command_recheck(library: Library, args: argparse.Namespace) -> int:
    day = args.date or date.today().isoformat()
    if not VALIDATOR.valid_date(day, False):
        raise LibraryError(f"invalid date {day}")
    results = []
    for path in args.results:
        loaded = load_json(path, "results")
        results.extend(loaded if isinstance(loaded, list) else [loaded])
    documents = dict(library.snapshot.documents)
    counts: Counter = Counter()
    seen: set[str] = set()
    for item in results:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or item.get("outcome") not in OUTCOMES:
            raise LibraryError(f"result needs id and outcome in {', '.join(OUTCOMES)}: {one_line(item, 120)}")
        source_id = item["id"].upper()
        record = library.records.get(source_id)
        if record is None or not record.document or source_id in seen:
            counts["skipped"] += 1
            continue
        seen.add(source_id)
        outcome = item["outcome"]
        content = documents[record.document]
        match = re.search(rf"^## {source_id}\n.*?(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
        if match is None:
            raise LibraryError(f"{source_id}: section not found")
        body = match.group(0)
        if outcome in ADVANCING:
            documents["sources.md"] = set_register_checked(documents["sources.md"], source_id, day)
        else:
            body = set_field(body, "Attempted", day, "Access")
        note = one_line(item.get("note", ""), 200)
        history = f"- History: {day} — Recheck by WebFetch: {OUTCOME_TEXT[outcome]}" + (f"; {note}" if note else "") + "\n"
        body = body.rstrip("\n") + "\n" + history
        trailing = "\n" if match.end() < len(content) else ""
        documents[record.document] = content[: match.start()] + body + trailing + content[match.end():]
        counts[outcome] += 1
    changes = {document: text for document, text in documents.items() if text != library.snapshot.documents.get(document)}
    written = commit(library, changes, args.dry_run) if changes else []
    print(f"{'DRY RUN, nothing written; ' if args.dry_run else ''}applied: " + ", ".join(f"{name} {count}" for name, count in sorted(counts.items())))
    print(f"files ({len(written)})")
    return 0


def archive_entry(library: Library, record: Record, item: dict, day: str, documents: dict[str, str]) -> dict:
    content = documents[record.document]
    section = re.search(rf"^## {record.id}\n.*?(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
    row = re.search(rf"^\| {record.id} \|.*$", documents["sources.md"], re.MULTILINE)
    marker = f"#{record.id.lower()})"
    index = f"notes/{record.domain}/index.md"
    return {
        "id": record.id, "retired_on": day, "reason": item["reason"], "evidence": item.get("evidence", ""),
        "title": record.title, "url": record.url, "useful_for": record.useful, "authority": record.authority, "checked": record.checked,
        "domain": record.domain, "document": record.document, "tags": record.tags, "projects": record.projects,
        "status": record.fields.get("Status", ""), "basis": record.fields.get("Basis", ""), "access": record.fields.get("Access", ""),
        "claim": record.fields.get("Claim", ""), "use_when": record.fields.get("Use when", ""),
        "register_row": row.group(0) if row else "", "section": section.group(0).rstrip("\n") if section else "",
        "index_lines": [line for line in documents.get(index, "").splitlines() if marker in line],
        "project_lines": [line for line in documents.get("projects.md", "").splitlines() if marker in line],
    }


def citing_documents(documents: dict[str, str], record: Record) -> list[str]:
    marker = f"#{record.id.lower()})"
    pattern = re.compile(rf"\b{record.id}\b")
    found = []
    for document, content in documents.items():
        text = content
        if document == "sources.md":
            text = re.sub(rf"^\| {record.id} \|.*$", "", text, flags=re.MULTILINE)
        elif document == record.document:
            text = re.sub(rf"^## {record.id}\n.*?(?=^## |\Z)", "", text, flags=re.MULTILINE | re.DOTALL)
        elif document in (f"notes/{record.domain}/index.md", "projects.md"):
            text = "\n".join(line for line in text.splitlines() if marker not in line)
        if pattern.search(text):
            found.append(document)
    return found


def remove_record(documents: dict[str, str], record: Record) -> None:
    marker = f"#{record.id.lower()})"
    documents["sources.md"] = re.sub(rf"^\| {record.id} \|.*\n", "", documents["sources.md"], flags=re.MULTILINE)
    content = documents[record.document]
    documents[record.document] = re.sub(rf"^## {record.id}\n.*?(?=^## |\Z)", "", content, flags=re.MULTILINE | re.DOTALL).rstrip("\n") + "\n"
    for document in (f"notes/{record.domain}/index.md", "projects.md"):
        if document in documents:
            documents[document] = "".join(line for line in documents[document].splitlines(keepends=True) if marker not in line)


def write_report(directory: Path) -> None:
    entries = [json.loads(line) for line in (directory / "retired-records.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    retained_path = directory / "retained-records.jsonl"
    retained = [json.loads(line) for line in retained_path.read_text(encoding="utf-8").splitlines() if line.strip()] if retained_path.exists() else []
    lines = ["# Research library recheck: deleted sources", "", f"Deleted records: {len(entries)}. Full records (register row, evidence section, index and project pointers) are in `retired-records.jsonl` in this folder; restore by reinserting them.", ""]
    for title, counter in (("By reason", Counter(entry["reason"] for entry in entries)), ("By domain", Counter(entry["domain"] for entry in entries)), ("By project", Counter(project for entry in entries for project in entry["projects"]))):
        lines += [f"## {title}", ""] + [f"- {name}: {count}" for name, count in counter.most_common()] + [""]
    lines += ["## Deleted records", "", "| ID | Source | URL | Authority | Last checked | Projects | Reason |", "|---|---|---|---|---|---|---|"]
    for entry in sorted(entries, key=lambda entry: entry["id"]):
        lines.append("| " + " | ".join([entry["id"], entry["title"].replace("|", "/"), entry["url"], entry["authority"], entry["checked"], ", ".join(entry["projects"]), entry["reason"].replace("|", "/")]) + " |")
    if retained:
        lines += ["", f"## Dead or empty but kept ({len(retained)})", "", "| ID | Source | URL | Why kept |", "|---|---|---|---|"]
        for entry in sorted(retained, key=lambda entry: entry["id"]):
            lines.append("| " + " | ".join([entry["id"], entry["title"].replace("|", "/"), entry["url"], entry["why"].replace("|", "/")]) + " |")
    (directory / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def command_retire(library: Library, args: argparse.Namespace) -> int:
    plan = load_json(args.plan, "plan")
    if not isinstance(plan, list) or not plan:
        raise LibraryError("plan must be a non-empty list of {id, reason, evidence}")
    day = date.today().isoformat()
    documents = dict(library.snapshot.documents)
    entries, skipped = [], []
    for item in plan:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not isinstance(item.get("reason"), str) or not item["reason"].strip():
            raise LibraryError(f"plan entry needs id and reason: {one_line(item, 120)}")
        record = library.records.get(item["id"].upper())
        if record is None or not record.document:
            skipped.append((item["id"], "no canonical record"))
            continue
        cited = citing_documents(documents, record)
        if cited:
            skipped.append((record.id, f"cited in {', '.join(cited[:3])}"))
            continue
        entries.append(archive_entry(library, record, item, day, documents))
        remove_record(documents, record)
    changes = {document: text for document, text in documents.items() if text != library.snapshot.documents.get(document)}
    if entries:
        commit(library, changes, True)
    if entries and not args.dry_run:
        directory = Path(args.archive_dir)
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / "retired-records.jsonl").open("a", encoding="utf-8") as handle:
            for entry in entries:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        commit(library, changes, False)
        write_report(directory)
    print(f"{'DRY RUN, nothing written; would delete' if args.dry_run else 'deleted'} {len(entries)} records; skipped {len(skipped)}")
    for source_id, reason in skipped[:20]:
        print(f"  skipped {source_id}: {reason}")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Retrieve, add and relabel research library sources through 1-3 label entities.")
    root.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    commands = root.add_subparsers(dest="command", required=True)
    labels = commands.add_parser("labels", help="list label vocabulary, optionally inside a 0-3 entity pool")
    labels.add_argument("--entity", action="append", default=[])
    labels.add_argument("--topic")
    labels.add_argument("--kind", choices=KINDS)
    labels.add_argument("--match")
    labels.add_argument("--limit", type=int, default=40)
    labels.add_argument("--include-retired", action="store_true")
    find = commands.add_parser("find", help="filter to the pool matching 1-3 entities, then rank by optional terms")
    find.add_argument("--entity", action="append", default=[])
    find.add_argument("--topic")
    find.add_argument("terms", nargs="*")
    find.add_argument("--limit", type=limit_value, default=8)
    find.add_argument("--checked-before")
    find.add_argument("--include-retired", action="store_true")
    topics = commands.add_parser("topics", help="list product topics from topics.md with live pool sizes; --check fails on broken topics")
    topics.add_argument("--project")
    topics.add_argument("--check", action="store_true")
    audit = commands.add_parser("audit", help="report label quality per project")
    audit.add_argument("--project", action="append")
    commands.add_parser("template", help="print a JSON packet skeleton for add")
    queue = commands.add_parser("queue", help="list web sources due for recheck and write batch files")
    queue.add_argument("--tranche", type=int, choices=(1, 2, 3))
    queue.add_argument("--output-dir")
    queue.add_argument("--batch-size", type=int, default=20)
    recheck = commands.add_parser("recheck", help="apply recheck results: Checked on a successful read, Attempted otherwise, plus History")
    recheck.add_argument("results", nargs="+")
    recheck.add_argument("--date")
    recheck.add_argument("--dry-run", action="store_true")
    retire = commands.add_parser("retire", help="delete records with no remaining use after archiving them in full; cited records are skipped")
    retire.add_argument("plan")
    retire.add_argument("--archive-dir", required=True)
    retire.add_argument("--dry-run", action="store_true")
    show = commands.add_parser("show", help="print register row and canonical section by R-ID or exact source URL")
    show.add_argument("keys", nargs="+")
    add = commands.add_parser("add", help="add records from a JSON packet: register row, section, domain index and project pointers")
    add.add_argument("packet")
    add.add_argument("--new-label", action="store_true")
    add.add_argument("--allow-same-source", action="store_true")
    add.add_argument("--dry-run", action="store_true")
    relabel = commands.add_parser("relabel", help="change tags or projects on one or more records with a dated History entry")
    relabel.add_argument("ids", nargs="*")
    relabel.add_argument("--plan")
    relabel.add_argument("--add-tag", action="append", default=[])
    relabel.add_argument("--remove-tag", action="append", default=[])
    relabel.add_argument("--add-project", action="append", default=[])
    relabel.add_argument("--remove-project", action="append", default=[])
    relabel.add_argument("--reason", required=True)
    relabel.add_argument("--new-label", action="store_true")
    relabel.add_argument("--dry-run", action="store_true")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    handlers = {"labels": command_labels, "find": command_find, "show": command_show, "add": command_add, "relabel": command_relabel, "topics": command_topics, "audit": command_audit, "template": command_template, "queue": command_queue, "recheck": command_recheck, "retire": command_retire}
    try:
        return handlers[args.command](load(args.root), args)
    except LibraryError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
