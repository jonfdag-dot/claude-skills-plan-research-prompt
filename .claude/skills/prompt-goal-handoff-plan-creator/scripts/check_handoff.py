import argparse
import json
import re
import sys
from pathlib import Path


GOAL_LIMIT = 4000
PROMPT_WARN = 10000
PLAN_WARN = 25000
BUNDLE_WARN = 60000
MAIN_FILES = ("plan.md", "prompt.md", "goal.md")
PLAN_HEADINGS = ("Lineage", "Status", "Delta", "Approvals", "Decisions", "Discoveries")
STATUSES = {"in_progress", "complete", "superseded"}
BUNDLE_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(-[a-z0-9]+)*$")
REFERENCES_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-references$")
SUBJECT_STEM = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+?)(?:-handoff(?:-[a-z0-9]+)*)?$")
HEADING = re.compile(r"^##\s+(?:\d+[.)]\s+)?(.+?)\s*$", re.M)
FIELD = re.compile(r"^([A-Za-z_][\w-]*):(.*)$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^(```|~~~).*?^\1\s*$", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")
URL = re.compile(r"https?://\S+")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
PATHLIKE = re.compile(r"(?:~|\.{0,2})?(?:/[\w.@+-]+)+/?")
GLUE = [
    re.compile(r"(?i)\b(with|was|and|at|all|exits|existing|not|of|to|the|in|on|for|by|from|has|have|is|are|keeps|than|only|about|into|after|before|over|under|release|done|commit|run|now|total|left)(\d)"),
    re.compile(r"\d%[A-Za-z]"),
    re.compile(r"\b[a-z]{2,},[A-Za-z]{2,}"),
]
HEX = re.compile(r"(?<![0-9A-Za-z-])(?=[0-9a-f]*[a-f])(?=[0-9a-f]*[0-9])[0-9a-f]{7,40}(?![0-9A-Za-z-])")
RATIO = re.compile(r"(?<![\w/])\d+\s*/\s*\d+(?![\w/])")
PROCESS = re.compile(r"(?i)\b(read in order|reading order|read first|first read|step \d|then run|open the file)\b")
SECRETS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\b(?:sk|rk|pk)_(?:live|test)_[A-Za-z0-9]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._-]{20,}"),
    re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_.-]{12,}"),
]


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, code, message):
        self.errors.append({"code": code, "message": message})

    def warn(self, code, message):
        self.warnings.append({"code": code, "message": message})


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    fields = {}
    for line in text[4:end].splitlines():
        match = FIELD.match(line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields, text[end + 4:]


def prose(text):
    _, body = frontmatter(text)
    body = FENCE.sub("", body)
    body = LINK_TARGET.sub("]", body)
    body = INLINE_CODE.sub("", body)
    return URL.sub("", body)


def sections(text):
    found = {}
    matches = list(HEADING.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        found[match.group(1).strip()] = text[match.end():end]
    return found


def reference_files(folder):
    return sorted(path for path in folder.rglob("*") if path.is_file() and path.name != ".DS_Store")


def check_tree(bundle, report):
    match = BUNDLE_NAME.match(bundle.name)
    if not match:
        report.error("tree.name", f"bundle folder must be YYYY-MM-DD-<kebab-subject>: {bundle.name}")
        return None, None
    bundle_date = match.group(1)
    references = None
    for entry in sorted(bundle.iterdir()):
        if entry.name == ".DS_Store":
            report.error("tree.ds_store", f"remove {entry}")
        elif entry.is_file() and entry.name in MAIN_FILES:
            continue
        elif entry.is_dir() and REFERENCES_NAME.match(entry.name):
            if references is not None:
                report.error("tree.references", f"only one references folder is allowed: {entry.name}")
            elif REFERENCES_NAME.match(entry.name).group(1) != bundle_date:
                report.error("tree.references", f"references folder date must equal the bundle date {bundle_date}: {entry.name}")
            references = entry
        else:
            report.error("tree.extra", f"bundle root holds only plan.md, prompt.md, goal.md and {bundle_date}-references/: {entry.name}")
    for name in MAIN_FILES:
        if not (bundle / name).is_file():
            report.error("tree.missing", f"missing {name}")
    return bundle_date, references


def check_references(references, report):
    if references is None:
        return []
    files = reference_files(references)
    if any(path.name == ".DS_Store" for path in references.rglob(".DS_Store")):
        report.error("tree.ds_store", f"remove .DS_Store files under {references}")
    others = [path for path in files if path != references / "README.md"]
    has_readme = (references / "README.md").is_file()
    if not others:
        report.error("references.empty", f"remove the empty references folder {references.name}")
    elif len(others) > 1 and not has_readme:
        report.error("references.readme", f"{references.name} holds {len(others)} files and needs README.md")
    elif len(others) == 1 and has_readme:
        report.error("references.readme", f"{references.name} holds one file; README.md is only allowed when it holds more than one")
    return others


def check_plan(bundle, bundle_date, report):
    path = bundle / "plan.md"
    if not path.is_file():
        return
    text = read(path)
    fields, body = frontmatter(text)
    if fields is None:
        report.error("plan.frontmatter", "plan.md needs frontmatter with status, created and completed")
        return
    if fields.get("status") not in STATUSES:
        report.error("plan.status", f"plan.md status must be one of {sorted(STATUSES)}")
    if "completed" not in fields:
        report.error("plan.completed", "plan.md frontmatter needs a completed field (empty while in progress)")
    if bundle_date and fields.get("created") != bundle_date:
        report.error("plan.created", f"plan.md created must equal the bundle date {bundle_date}")
    found = sections(body)
    for heading in PLAN_HEADINGS:
        if heading not in found:
            report.error("plan.heading", f"plan.md needs a '## {heading}' section")
    status = found.get("Status", "")
    if "Status" in found and not re.search(r"(?m)^\s*(?:[-*]\s*)?\**Next action:?\**:?", status):
        report.error("plan.next_action", "plan.md Status needs a 'Next action:' line")
    if len(text) > PLAN_WARN:
        report.warn("budget.plan", f"plan.md is {len(text)} characters; keep history in superseded predecessors")


def check_prompt(bundle, references, reference_list, report):
    path = bundle / "prompt.md"
    if not path.is_file():
        return
    text = read(path)
    if not text.strip():
        report.error("prompt.empty", "prompt.md is empty")
        return
    if text.startswith("---\n"):
        report.error("prompt.frontmatter", "prompt.md is paste text; remove frontmatter")
    plan_path = str((bundle / "plan.md").resolve())
    if plan_path not in text:
        report.error("prompt.plan", f"prompt.md must name the absolute plan path {plan_path}")
    if "goal.md" not in text:
        report.error("prompt.goal", "prompt.md must point to goal.md")
    words = PATHLIKE.sub(" ", text)
    if not re.search(r"(?i)\binstall", words):
        report.error("prompt.install", "prompt.md must say how to install the plan")
    if not re.search(r"(?i)\bdone\b", words):
        report.error("prompt.done", "prompt.md must say what done means")
    if references is not None:
        if references.name not in text:
            report.error("prompt.references", f"prompt.md must point to {references.name}/")
        readme = references / "README.md"
        readme_text = read(readme) if readme.is_file() else ""
        for item in reference_list:
            relative = item.relative_to(references).as_posix()
            if relative not in text and relative not in readme_text and item.name not in text and item.name not in readme_text:
                report.error("prompt.reference_file", f"reference file is named neither in prompt.md nor in README.md: {relative}")
    if len(text) > PROMPT_WARN:
        report.warn("budget.prompt", f"prompt.md is {len(text)} characters; aim for about 6,000")
    hashes = sorted(set(HEX.findall(prose(text))))
    if hashes:
        report.warn("prompt.volatile", f"prompt.md copies revision-like values {hashes[:5]}; point to plan.md Status instead")


def check_goal(bundle, report):
    path = bundle / "goal.md"
    if not path.is_file():
        return
    text = read(path)
    length = len(text)
    if not text.strip():
        report.error("goal.empty", "goal.md is empty")
        return
    if length > GOAL_LIMIT:
        report.error("goal.length", f"goal.md is {length} characters; the limit is {GOAL_LIMIT}")
    if text.startswith("---\n") or text.lstrip().startswith("```"):
        report.error("goal.wrapper", "goal.md is the paste text itself; remove frontmatter and fences")
    if not re.search(r"(?i)\bdone\b", PATHLIKE.sub(" ", text)):
        report.error("goal.done", "goal.md must state what done means")
    body = prose(text)
    volatile = sorted(set(HEX.findall(body)))
    if volatile:
        report.warn("goal.volatile", f"goal.md holds revision-like values {volatile[:5]}; volatile state belongs in plan.md Status")
    if PROCESS.search(body):
        report.warn("goal.process", "goal.md appears to hold process or reading-order text; keep it to final state and done")


def check_prose(bundle, reference_list, report):
    paths = [bundle / name for name in MAIN_FILES if (bundle / name).is_file()]
    paths.extend(path for path in reference_list if path.suffix == ".md")
    references_readme = [path for path in bundle.glob("*-references/README.md")]
    paths.extend(references_readme)
    for path in paths:
        text = read(path)
        body = prose(text)
        for pattern in GLUE:
            hits = sorted(set(match.group(0) for match in pattern.finditer(body)))
            if hits:
                report.error("prose.glued", f"{path.relative_to(bundle)} glues words and numbers: {hits[:6]}")
        for pattern in SECRETS:
            if pattern.search(text):
                report.error("secret", f"{path.relative_to(bundle)} contains a secret-like value matching {pattern.pattern[:40]}")
        for match in LINK.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = Path(target) if target.startswith("/") else (path.parent / target)
            if not resolved.exists():
                report.error("link", f"{path.relative_to(bundle)} links to a missing path: {target}")
    return paths


def check_duplication(bundle, report):
    seen = {}
    for name in MAIN_FILES:
        path = bundle / name
        if not path.is_file():
            continue
        for line in prose(read(path)).splitlines():
            normalized = re.sub(r"\s+", " ", line).strip().lower()
            if len(normalized) < 80:
                continue
            seen.setdefault(normalized, set()).add(name)
    for line, names in seen.items():
        if len(names) > 1:
            report.warn("duplication", f"same line appears in {sorted(names)}: {line[:90]}...")


def check_budget(bundle, report):
    total = sum(len(read(bundle / name)) for name in MAIN_FILES if (bundle / name).is_file())
    if total > BUNDLE_WARN:
        report.warn("budget.bundle", f"plan, prompt and goal total {total} characters; aim under 40,000 before references")


def check_prior(bundle, prior, report):
    if not prior.is_file():
        report.error("prior.missing", f"prior plan not found: {prior}")
        return
    fields, _ = frontmatter(read(prior))
    if fields is None:
        report.error("prior.frontmatter", f"prior plan has no frontmatter: {prior}")
        return
    if fields.get("status") == "superseded":
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fields.get("superseded_on", "")):
            report.error("prior.superseded_on", "prior plan needs superseded_on: YYYY-MM-DD")
        successor = fields.get("succeeded_by", "")
        project = bundle.parent
        if not successor:
            report.error("prior.succeeded_by", "prior plan needs succeeded_by pointing to the new plan.md")
        elif (project / successor).resolve() != (bundle / "plan.md").resolve():
            report.error("prior.succeeded_by", f"prior succeeded_by resolves to {(project / successor)} instead of {bundle / 'plan.md'}")
    else:
        report.warn("prior.status", f"prior plan status is {fields.get('status')}; use superseded unless this is a partial replacement")
    plan = bundle / "plan.md"
    if plan.is_file():
        lineage = sections(frontmatter(read(plan))[1]).get("Lineage", "")
        if prior.parent.name not in lineage and prior.name not in lineage:
            report.error("prior.lineage", f"plan.md Lineage must name the prior handoff {prior.parent.name}")


def subject_stem(name):
    match = SUBJECT_STEM.match(name)
    return match.group(1) if match else None


def check_siblings(bundle, report):
    stem = subject_stem(bundle.name)
    plan = bundle / "plan.md"
    if not stem or not plan.is_file():
        return
    lineage = sections(frontmatter(read(plan))[1]).get("Lineage", "")
    for sibling in sorted(bundle.parent.iterdir()):
        if sibling == bundle or not sibling.is_dir() or subject_stem(sibling.name) != stem:
            continue
        sibling_plan = sibling / "plan.md"
        if not sibling_plan.is_file():
            continue
        fields, _ = frontmatter(read(sibling_plan))
        if (fields or {}).get("status") != "in_progress":
            continue
        named = [line for line in lineage.splitlines() if sibling.name in line]
        if any(line.lstrip("-* ").startswith("Canonical plan:") or "Partially supersedes" in line for line in named):
            continue
        report.warn("lineage.live_sibling", f"{sibling.name} is another in_progress bundle for this initiative; supersede it or name it in Lineage as the canonical plan or a partial replacement")


def run(bundle, prior):
    report = Report()
    if not bundle.is_dir():
        report.error("tree.missing", f"bundle folder not found: {bundle}")
        return report
    bundle_date, references = check_tree(bundle, report)
    reference_list = check_references(references, report)
    check_plan(bundle, bundle_date, report)
    check_prompt(bundle, references, reference_list, report)
    check_goal(bundle, report)
    check_prose(bundle, reference_list, report)
    check_duplication(bundle, report)
    check_budget(bundle, report)
    check_siblings(bundle, report)
    if prior is not None:
        check_prior(bundle, prior, report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check a session handoff bundle against the prompt-goal-handoff-plan-creator contract.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--prior", type=Path, help="plan.md of the handoff this bundle supersedes")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    options = parser.parse_args(argv)
    bundle = options.bundle.resolve()
    report = run(bundle, options.prior.resolve() if options.prior else None)
    if options.format == "json":
        sys.stdout.write(json.dumps({"bundle": str(bundle), "errors": report.errors, "warnings": report.warnings, "pass": not report.errors}, indent=2) + "\n")
    else:
        for item in report.errors:
            sys.stdout.write(f"ERROR {item['code']}: {item['message']}\n")
        for item in report.warnings:
            sys.stdout.write(f"WARN {item['code']}: {item['message']}\n")
        goal = bundle / "goal.md"
        goal_size = len(read(goal)) if goal.is_file() else 0
        sys.stdout.write(f"{'PASS' if not report.errors else 'FAIL'}: {len(report.errors)} errors, {len(report.warnings)} warnings; goal.md {goal_size}/{GOAL_LIMIT} characters\n")
    return 0 if not report.errors else 1


if __name__ == "__main__":
    sys.exit(main())
