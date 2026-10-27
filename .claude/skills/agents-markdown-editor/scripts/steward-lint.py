import argparse
import ast
import fnmatch
import importlib.util
import json
import os
import re
import shlex
import shutil
import sys
import tomllib
from pathlib import Path

TOOL_VERSION = "2"
VERSION_FLOOR = (2, 1, 273)
CHARS_PER_TOKEN = 3.7
CODEX_DEFAULT_BUDGET = 32768
FILE_LINE_ADVICE = 200
AGGREGATE_LINE_ADVICE = 400
CLAUDE_SKIP_BYTES = 4 * 1024 * 1024
GLOB_PATTERN_BUDGET = 1000
GLOB_BYTE_BUDGET = 4 * 1024 * 1024
EMPHASIS_LINE_BUDGET = 3
MAX_IMPORT_DEPTH = 4
MANAGED_POLICY = Path("/Library/Application Support/ClaudeCode/CLAUDE.md")
PRUNE = frozenset({".git", "node_modules", "dist", "build", ".next", ".venv", "venv", "__pycache__", ".turbo", "coverage", "target", ".cache", "Pods", ".gitnexus", "graphify-out", ".pytest_cache", ".mypy_cache"})
SEVERITY_RANK = {"info": 0, "report": 1, "warn": 2, "block": 3}
GATE_ORDER = ["G1", "G2", "G3", "G4", "G6", "G7", "G8", "G9", "G10", "G12", "G13", "G15", "G16"]
GATE_NAMES = {
    "G1": "size",
    "G2": "pointers",
    "G3": "model phrases",
    "G4": "duplication",
    "G6": "emphasis",
    "G7": "enforcement",
    "G8": "executable",
    "G9": "contract",
    "G10": "twins",
    "G12": "glob budget",
    "G13": "runtime bytes",
    "G15": "required reference",
    "G16": "generated",
}
COPY_PART = re.compile(r"^(complete|\.runs|archives?|eval-runs)$|backup|baseline|archive", re.IGNORECASE)
CONTRACT_DIRS = ("scripts", "tests", "test", "tools", "bin", "ci", ".github", ".husky", "hooks", ".work")
CONTRACT_SUFFIXES = (".py", ".sh", ".js", ".mjs", ".cjs", ".ts", ".rb", ".yml", ".yaml", ".json", ".toml")
CONTRACT_ROOT_FILES = ("Makefile", "GNUmakefile", "makefile", "package.json", "justfile", "Taskfile.yml")
CONTRACT_READER = re.compile(r"([\"'`])((?:/|~/)?(?:[\w .-]+/)*(?:CLAUDE\.md|AGENTS\.md|CLAUDE\.local\.md|AGENTS\.override\.md))\1")
CONTENT_READ = re.compile(r"\b(?:read_text|read_bytes|readFileSync|readFile|readTextFile|readlines|readlinesSync|read_to_string|readFileToString)\s*\(|\bFile\.(?:read|readlines|binread)\s*\(|\bopen\s*\([^\n]*\)\s*\.read\s*\(|\b(?:cat|wc|awk|sed)\b[^\n]*\.(?:md)\b")
PATH_READ = re.compile(r"\b(?:exists|existsSync|is_file|is_symlink|symlink\?|readlink|stat|statSync|lstat|access)\s*\(")
SOURCE_ASSIGNMENT = re.compile(r"^\s*(?:(?:const|let|var)\s+)?([A-Za-z_]\w*)\s*(?::[^=]+)?=(?!=)")
SOURCE_LOOP = re.compile(r"\bfor\s+(?:\(\s*(?:const|let|var)\s+)?([A-Za-z_]\w*)\s+(?:in|of)\b")
GENERATED_START = re.compile(r"<!--\s*([\w.-]+):start\b[^>]*-->")
GENERATED_END = "<!--\\s*{name}:end\\b[^>]*-->"

FENCE = re.compile(r"^(`{3,}|~{3,})(.*)$")
INLINE_CODE = re.compile(r"`[^`\n]*`")
BACKTICK = re.compile(r"`([^`\n]+)`")
MD_LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)\)")
BARE_PATH = re.compile(r"(?<![\w`/~])((?:/Users/|~/)[^\s`,;:)\]'\"]+)")
IMPORT = re.compile(r"(?<![\w@`/.])@((?:~/|\.{1,2}/|/)?[A-Za-z0-9_][A-Za-z0-9_./-]*)")
ALLCAPS_RUN = re.compile(r"\b[A-Z][A-Z0-9 ,'/&-]{24,}\b")
EMPHASIS_TOKEN = re.compile(r"\b(NEVER|MUST|IMPORTANT|CRITICAL|ALWAYS)\b")
BOLD_ONLY = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+)?(\*\*|__)(?=\S)(.+?)(?<=\S)\1[.:]?$")
BOLD_LEAD = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+)?(?:\*\*|__)([^*_]+?)(?:\*\*|__)", re.IGNORECASE)
LEAD_DIRECTIVE = re.compile(r"\b(never|must|always|do not|don't|only|required|mandatory|iron|critical)\b", re.IGNORECASE)
NON_ASSERTIVE = re.compile(r"\b(never|not a|no longer|forbidden|banned|instead of|rather than|e\.g\.|for example|example|placeholder|deprecated|removed|gone|do not create|is gone|gets denied|would be|such as|stops?|prevents?|avoid|must not|do not|don't|nothing|absent|not exist|missing|saved to|written to|created on|on first use|will be created)\b", re.IGNORECASE)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
ENFORCEMENT_CLAIM = re.compile(r"\b(?:(?:is|are|gets?|will be|be|been)\s+(?:automatically\s+|always\s+)?(?:blocked|denied|rejected|enforced|prevented)|enforced\s+by|fails?\s+closed|hard[- ]gate|blocks?\s+(?:every|any|all)|(?:hook|hooks|ci|lint|linter|check|checks|workflow|pre-commit|pre-push)\s+(?:blocks|rejects|fails|enforces?|prevents|denies))\b", re.IGNORECASE)
KIND_WORDS = {
    "hook": re.compile(r"\b(?:hooks?|pre-commit|pre-push|husky|lefthook)\b", re.IGNORECASE),
    "ci": re.compile(r"\b(?:ci|workflows?|github actions|pipeline)\b", re.IGNORECASE),
    "lint": re.compile(r"\b(?:lint|linter|eslint|ruff|semgrep|biome|oxlint)\b", re.IGNORECASE),
    "permission": re.compile(r"\b(?:permissions?|deny rules?)\b", re.IGNORECASE),
}
CONTRACT_EXACT = re.compile(r"\bexactly\s+(\d+)\s+(newline-terminated\s+)?lines\b", re.IGNORECASE)
CONTRACT_WC = re.compile(r"`wc\s+-l\s+([^`]+)`\s+(?:(?:must\s+)?reports?|(?:must\s+)?(?:returns?|outputs?))\s+exactly\s+`?(\d+)`?", re.IGNORECASE)
CONTRACT_CAP = re.compile(r"\b(?:under|at most|no more than|fewer than|below)\s+(\d+)\s+lines\b", re.IGNORECASE)
CONTRACT_TWIN = re.compile(r"\bbyte[- ]identical\b", re.IGNORECASE)
CONTRACT_RESOLVES = re.compile(r"\bevery\s+(?:path|pointer|link)\b[^.]*\bresolves?\b", re.IGNORECASE)
INSTRUCTION_NAME = re.compile(r"\b(CLAUDE\.md|AGENTS\.md|CLAUDE\.local\.md|AGENTS\.override\.md)\b")
REQUIRED_LINE = re.compile(r"\b(?:required|must[- ]read|must (?:understand|load|invoke|use|read)|load (?:the )?(?:skill|agent)|invoke (?:the )?\S+ skill)\b", re.IGNORECASE)
SKILL_REF = re.compile(r"(?<![\w/.:@-])([a-z0-9][a-z0-9-]*):([a-z][a-z0-9-]*[a-z0-9])(?![\w/:-])")
NAMED_SKILL = re.compile(r"`([a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?)`\s+(?:skill|agent|subagent)\b|\b(?:skill|agent|subagent)\s+`([a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?)`", re.IGNORECASE)
REF_NAMESPACE_IGNORE = frozenset({"http", "https", "file", "mailto", "ssh", "git", "data", "localhost", "tcp", "udp", "note", "see", "example", "source", "scope", "verdict", "evidence", "action", "plugin", "personal", "project", "user", "global", "type", "class", "status", "created", "completed", "model", "effort", "npm", "node", "pool"})
VERSION_TRIPLE = re.compile(r"(\d+)\.(\d+)\.(\d+)")

MODEL_PHRASES = [
    (re.compile(r"\bhold\b[^.]{0,20}\b(findings|updates|results|progress)\b[^.]{0,40}\b(final|end)\b", re.IGNORECASE), "class-13", "Fable 5.1 guide: review this older narration constraint against current requirements; a justified static edit needs no model run"),
    (re.compile(r"\b(no|avoid|don't use|do not use|never use|minimi[sz]e)\b[^.]{0,30}\b(bullets?|bullet points|bold|markdown|headers|headings|formatting)\b", re.IGNORECASE), "class-13", "Fable 5.1 guide: anti-formatting rule written for older models; replace with when formatting is appropriate"),
    (re.compile(r"\b(show|explain|echo|transcribe|print|write out|narrate)\b[^.]{0,20}\b(your |the )?(internal )?(reasoning|thinking|thought process|chain of thought)\b", re.IGNORECASE), "class-13", "Fable 5 guide: echoing internal reasoning as response text can trigger reasoning_extraction refusals"),
    (re.compile(r"\b(context|token)[- ](budget|countdown|remaining)\b|\b\d{1,3}\s?%\s+of\s+(the\s+)?(context\s+)?window\b|\bremaining context\b", re.IGNORECASE), "class-13", "Fable 5 and 5.1 guides: surfaced context-budget counts are the usual trigger of premature handoff"),
    (re.compile(r"\bbefore (every|any|each|all) (edit|change|task|commit)s?\b[^.]{0,80}\bread\b|\b(always|must) read\b[^.]{0,60}\bbefore\b|\bread all\b[^.]{0,60}\bbefore\b", re.IGNORECASE), "class-13", "GPT-6 Astra guide: mandatory pre-reads become conditional pointers (use X for Y)"),
    (re.compile(r"\b(do not|don't|never) (go beyond|exceed) (the|what)\b|\bonly do (exactly )?what\b", re.IGNORECASE), "class-13", "GPT-6 Astra guide: boundaries written to hold back older models can now hinder results"),
    (re.compile(r"\breport outcomes faithfully\b|\bif tests fail, say so\b", re.IGNORECASE), "class-14", "Claude Code 2.1.273 and later inject this progress-grounding sentence (still present on 2.1.286)"),
    (re.compile(r"\bno message from any agent counts as\b", re.IGNORECASE), "class-14", "Claude Code 2.1.273 and later subagent lifecycle guarantees this (still present on 2.1.286)"),
]
FILE_SUFFIXES = (".md", ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".sh", ".mjs", ".sql", ".yml", ".yaml", ".toml", ".txt", ".html", ".css", ".jsonl", ".rb", ".go", ".rs")
NOT_A_PATH = ("{", "}", "$", "<", ">", "(", ")", "|", "*", "=", "//", "\\")
COMMAND_WORDS = frozenset({"python", "python3", "node", "npm", "pnpm", "npx", "yarn", "bun", "bash", "sh", "zsh", "make", "just", "cargo", "go", "uv", "uvx", "pip", "pip3", "deno", "ruby", "git", "docker", "supabase", "gh", "pytest", "ruff", "tsc", "eslint", "prettier", "pipx", "brew", "rg", "jq"})
SHELL_INFO = frozenset({"sh", "bash", "shell", "zsh", "console", "shell-session", "terminal"})
DESTRUCTIVE = re.compile(r"\b(rm|sudo|curl|wget|deploy|drop|truncate|reset|force|push|publish|kill)\b")
SCRIPT_TOKEN = re.compile(r"^(?:\./|\.\./|scripts/|bin/|tools/|hooks/)[\w./-]+\.(?:sh|py|mjs|rb)$|^[\w./-]+/[\w.-]+\.(?:sh|py)$")
SCRATCH_PREFIXES = ("/tmp/", "/private/tmp/", "/var/folders/", "/dev/")
MAKEFILE_NAMES = ("GNUmakefile", "makefile", "Makefile")
DUPLICATE_LINE_LIST = 8
MAKE_RULE = re.compile(r"^([A-Za-z0-9_./%-][^:=#\t]*?)\s*::?(?![=])")
MAKE_INCLUDE = re.compile(r"^\s*-?s?include\s", re.MULTILINE)
MACHINERY_SHAPE = re.compile(r"(?:^|/)(?:\.claude/hooks|hooks|\.husky|\.github/workflows|\.git/hooks|scripts)(?:/|$)|settings(?:\.local)?\.json$|\.pre-commit-config\.ya?ml$|lefthook\.ya?ml$|eslint\.config\.|\.eslintrc|ruff\.toml$|\.sh$")
HOME_SHORTHAND_TREES = (".claude/skills", ".claude/scripts", ".claude/hooks", ".claude/docs", ".claude/agents", ".claude/rules", ".claude/commands", ".agents/skills")


def severity_max(values):
    best = "pass"
    rank = -1
    for value in values:
        if SEVERITY_RANK[value] > rank and value != "info":
            best = value
            rank = SEVERITY_RANK[value]
    return best


class Store:
    def __init__(self):
        self.cache = {}

    def data(self, path):
        key = str(path)
        if key not in self.cache:
            try:
                self.cache[key] = Path(path).read_bytes()
            except OSError:
                self.cache[key] = None
        return self.cache[key]

    def text(self, path):
        raw = self.data(path)
        return None if raw is None else raw.decode("utf-8", errors="replace")


def iter_lines(text):
    in_fence = False
    marker = ""
    info = ""
    in_frontmatter = False
    lines = text.split("\n")
    if text.endswith("\n"):
        lines = lines[:-1]
    for number, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if number == 1 and stripped == "---":
            in_frontmatter = True
            yield number, raw, "frontmatter", ""
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            yield number, raw, "frontmatter", ""
            continue
        fence = FENCE.match(stripped)
        if fence:
            if not in_fence:
                in_fence = True
                marker = fence.group(1)[0] * 3
                info = fence.group(2).strip().lower()
                yield number, raw, "fence", info
                continue
            if stripped.startswith(marker) and not stripped.strip(marker[0]):
                in_fence = False
                yield number, raw, "fence", info
                continue
        yield number, raw, "code" if in_fence else "text", info


def text_lines(text):
    for number, raw, kind, _info in iter_lines(text):
        if kind == "text" and raw.strip():
            yield number, raw


def prose_atoms(text):
    for number, raw in text_lines(text):
        stripped = raw.strip()
        if stripped.startswith("|---") or stripped == "---":
            continue
        yield number, stripped


def count_newlines(raw):
    return raw.count(b"\n")


def frontmatter_paths(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end].split("\n")
    for index, line in enumerate(block):
        match = re.match(r"^paths:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip()
        items = []
        if value.startswith("["):
            items = [part.strip().strip("\"'") for part in value.strip("[]").split(",") if part.strip()]
        elif value:
            items = [part.strip().strip("\"'") for part in value.split(",") if part.strip()]
        else:
            for follow in block[index + 1:]:
                item = re.match(r"^\s+-\s+(.*)$", follow)
                if not item:
                    if follow.strip() and not follow.startswith((" ", "\t")):
                        break
                    continue
                items.append(item.group(1).strip().strip("\"'"))
        return items
    return None


def walk_files(root, names):
    found = []
    if not root.is_dir():
        return found
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in PRUNE)
        for name in sorted(files):
            if name in names:
                found.append(Path(current) / name)
    return found


def chain_dirs(cwd):
    return list(reversed([cwd] + list(cwd.parents)))


def is_within(path, root):
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False


class LoadedSet:
    def __init__(self, store, repo, cwd, home, managed, claude_settings=(), codex_home=None, codex_config=None, claude_settings_explicit=False):
        self.store = store
        self.repo = repo
        self.cwd = cwd
        self.home = home
        self.managed = managed
        self.claude = []
        self.codex = []
        self.notes = []
        self.seen = set()
        self.codex_home = codex_home or home / ".codex"
        self.codex_config = codex_config or self.codex_home / "config.toml"
        self.claude_settings = list(claude_settings)
        self.claude_settings_explicit = claude_settings_explicit
        self.claude_excludes = []
        self.instruction_option = None

    def selected_claude_settings(self):
        for path in self.claude_settings:
            if not path.is_file():
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                self.notes.append(str(path) + " is unreadable or does not parse; Claude loading settings are unknown")
                continue
            if not isinstance(data, dict):
                self.notes.append(str(path) + " has no settings object; Claude loading settings are unknown")
                continue
            excludes = data.get("claudeMdExcludes", [])
            if isinstance(excludes, list) and all(isinstance(item, str) for item in excludes):
                self.claude_excludes.extend((item, self.repo) for item in excludes)
            else:
                self.notes.append(str(path) + " has an unsupported claudeMdExcludes shape; exclusions are unknown")
            plugins = data.get("pluginConfigs", {})
            builtin = plugins.get("agents-md@builtin", {}) if isinstance(plugins, dict) else {}
            options = builtin.get("options", {}) if isinstance(builtin, dict) else {}
            option = options.get("instructionFiles") if isinstance(options, dict) else None
            if option is not None:
                if not self.claude_settings_explicit and path != self.home / ".claude" / "settings.json":
                    self.notes.append(str(path) + " instructionFiles is ignored in the default project/local layer; its exclusions still apply")
                    continue
                if option in ("claude-md-and-agents-md", "claude-md", "managed-only"):
                    self.instruction_option = option
                else:
                    self.notes.append(str(path) + " has an unsupported instructionFiles option; its effect is unknown")
        if self.claude_settings_explicit:
            self.notes.append("Explicit --claude-settings paths are treated as operator-selected effective layers; original scope/provenance and runtime application are unverified")
        self.notes.append("Static loading prediction from selected files; managed or CLI settings overrides, additional instruction-file options, conditional activation and runtime receipts are unobserved")

    def claude_excluded(self, path):
        def matches(parts: tuple[str, ...], patterns: tuple[str, ...]) -> bool:
            if not patterns:
                return not parts
            if patterns[0] == "**":
                return matches(parts, patterns[1:]) or bool(parts) and matches(parts[1:], patterns)
            return bool(parts) and fnmatch.fnmatchcase(parts[0], patterns[0]) and matches(parts[1:], patterns[1:])

        absolute = os.path.abspath(path)
        real = os.path.realpath(path)
        for pattern, base in self.claude_excludes:
            if any(token in pattern for token in ("{", "}", "!", "(")):
                self.notes.append("Selected claudeMdExcludes contains unsupported extended glob syntax; its effect is unknown")
                continue
            expanded = str(self.home / pattern[2:]) if pattern.startswith("~/") else pattern
            expanded = expanded if os.path.isabs(expanded) else str(base / expanded)
            if any(matches(Path(value).parts, Path(expanded).parts) for value in (absolute, real)):
                self.notes.append(str(path) + " is inventoried but excluded from Claude loading by selected claudeMdExcludes")
                return True
        return False

    def add_claude(self, path, scope, condition, reason, depth=0, parent=None):
        if scope != "managed" and self.claude_excluded(path):
            return None
        real = os.path.realpath(path)
        if real in self.seen:
            return None
        self.seen.add(real)
        raw = self.store.data(path)
        entry = {
            "runtime": "claude-code",
            "path": str(path),
            "real": real,
            "scope": scope,
            "condition": condition,
            "reason": reason,
            "depth": depth,
            "parent": parent,
            "bytes": 0 if raw is None else len(raw),
            "lines": 0 if raw is None else count_newlines(raw),
            "chars": 0 if raw is None else len(raw.decode("utf-8", errors="replace")),
            "symlink": Path(path).is_symlink(),
        }
        self.claude.append(entry)
        return entry

    def rules(self, directory, scope):
        if not directory.is_dir():
            return
        if directory.is_symlink():
            self.notes.append("rules directory " + str(directory) + " is a symlink: paths-scoped members may not load")
        for path in sorted(p for p in directory.rglob("*.md") if p.is_file()):
            text = self.store.text(path) or ""
            globs = frontmatter_paths(text)
            if globs:
                self.add_claude(path, scope, "paths:" + ",".join(globs), "rules file with paths frontmatter")
            else:
                self.add_claude(path, scope, "unconditional", "rules file without paths frontmatter")

    def resolve_claude(self):
        self.selected_claude_settings()
        if self.managed.is_file():
            self.add_claude(self.managed, "managed", "unconditional", "managed policy")
        user = self.home / ".claude" / "CLAUDE.md"
        if user.is_file():
            self.add_claude(user, "user", "unconditional", "user file")
        self.rules(self.home / ".claude" / "rules", "user-rules")
        user_real = os.path.realpath(user)
        chain_has_claude_md = False
        for directory in chain_dirs(self.cwd):
            scope = "project" if is_within(directory, self.repo) else "ancestor"
            for name in ("CLAUDE.md", ".claude/CLAUDE.md"):
                candidate = directory / name
                if candidate.is_file():
                    self.add_claude(candidate, scope, "unconditional", "directory chain")
                    if not self.claude_excluded(candidate) and os.path.realpath(candidate) != user_real:
                        chain_has_claude_md = True
            local = directory / "CLAUDE.local.md"
            if local.is_file():
                self.add_claude(local, "local", "unconditional", "local file")
                if not self.claude_excluded(local):
                    chain_has_claude_md = True
        agents_md_reason = self.agents_md_reason(chain_has_claude_md)
        if agents_md_reason:
            for directory in chain_dirs(self.cwd):
                scope = "project" if is_within(directory, self.repo) else "ancestor"
                for name in ("AGENTS.md", ".claude/AGENTS.md"):
                    candidate = directory / name
                    if candidate.is_file():
                        self.add_claude(candidate, scope, "unconditional", agents_md_reason)
        self.rules(self.repo / ".claude" / "rules", "project-rules")
        for path in walk_files(self.cwd, {"CLAUDE.md", "CLAUDE.local.md"}):
            if path.parent == self.cwd or (path.parent.name == ".claude" and path.parent.parent == self.cwd):
                continue
            if "rules" in path.parts:
                continue
            owner = path.parent.parent if path.parent.name == ".claude" else path.parent
            self.add_claude(path, "nested", "subtree-read:" + str(owner), "nested file below the working directory")
        queue = list(self.claude)
        while queue:
            entry = queue.pop(0)
            text = self.store.text(entry["path"]) or ""
            for number, raw in text_lines(text):
                visible = INLINE_CODE.sub("", raw)
                for match in IMPORT.finditer(visible):
                    token = match.group(1).rstrip(".,;:)")
                    if "/" not in token and "." not in token:
                        continue
                    target = self.resolve_import(token, Path(entry["path"]))
                    if target is None or not target.is_file():
                        if "/" in token or token.endswith(FILE_SUFFIXES):
                            self.notes.append(entry["path"] + ":" + str(number) + " import @" + token + " does not resolve and loads nothing")
                        continue
                    depth = entry["depth"] + 1
                    if depth > MAX_IMPORT_DEPTH:
                        self.notes.append(entry["path"] + ":" + str(number) + " import @" + token + " exceeds depth " + str(MAX_IMPORT_DEPTH) + " and does not load")
                        continue
                    if not is_within(target, self.repo) and not is_within(target, self.home / ".claude"):
                        self.notes.append(entry["path"] + ":" + str(number) + " import @" + token + " is external and needs one-time approval; a declined import stays inert")
                    added = self.add_claude(target, "import", entry["condition"], "import from " + entry["path"] + ":" + str(number), depth, entry["path"])
                    if added:
                        queue.append(added)

    def agents_md_reason(self, chain_has_claude_md):
        option = self.instruction_option
        if option == "claude-md-and-agents-md":
            return "agents-md plugin: instructionFiles claude-md-and-agents-md in selected settings"
        if option in ("claude-md", "managed-only"):
            return None
        if not chain_has_claude_md:
            return "agents-md plugin default: no CLAUDE.md, .claude/CLAUDE.md or CLAUDE.local.md in the working directory or above"
        return None

    def resolve_import(self, token, importer):
        if token.startswith("~/"):
            return self.home / token[2:]
        if token.startswith("/"):
            return Path(token)
        return importer.parent / token

    def resolve_codex(self):
        self.notes.append("Codex prediction uses " + str(self.codex_home) + " and selected config " + str(self.codex_config) + "; CLI/profile/managed and trusted project config overrides, project trust and runtime receipts are unverified")
        for name in ("AGENTS.override.md", "AGENTS.md"):
            candidate = self.codex_home / name
            if candidate.is_file() and (self.store.data(candidate) or b"").strip():
                raw = self.store.data(candidate)
                self.codex.append({"runtime": "codex", "path": str(candidate), "real": os.path.realpath(candidate), "scope": "global", "bytes": len(raw or b""), "budgeted": False})
                break
        root = git_root(self.cwd) or self.repo
        names = ["AGENTS.override.md", "AGENTS.md"]
        if self.codex_config.is_file():
            try:
                config = tomllib.loads(self.codex_config.read_text(encoding="utf-8"))
                fallback = config.get("project_doc_fallback_filenames", [])
                if isinstance(fallback, list) and all(isinstance(name, str) and name and Path(name).name == name for name in fallback):
                    names.extend(name for name in fallback if name not in names)
                else:
                    self.notes.append(str(self.codex_config) + " has unsupported project_doc_fallback_filenames; fallback selection is unknown")
            except (OSError, ValueError):
                self.notes.append(str(self.codex_config) + " is unreadable or does not parse; fallback selection is unknown")
        dirs = [d for d in chain_dirs(self.cwd) if is_within(d, root)]
        for directory in dirs:
            for name in names:
                candidate = directory / name
                if candidate.is_file() and (self.store.data(candidate) or b"").strip():
                    raw = self.store.data(candidate)
                    self.codex.append({"runtime": "codex", "path": str(candidate), "real": os.path.realpath(candidate), "scope": "project", "bytes": len(raw or b""), "budgeted": True})
                    break
        return root


def git_root(start):
    for directory in [start] + list(start.parents):
        if (directory / ".git").exists():
            return directory
    return None


def finding(path, line, gate, severity, evidence):
    return {"path": str(path), "line": line, "gate": gate, "severity": severity, "evidence": " ".join(str(evidence).replace("|", "/").split())}


def gate_result(gate, scope, findings, stats=None, verdict=None):
    ordered = sorted(findings, key=lambda f: (-SEVERITY_RANK[f["severity"]], f["path"], f["line"], f["evidence"]))
    return {
        "gate": gate,
        "name": GATE_NAMES[gate],
        "scope": scope,
        "verdict": verdict or severity_max(f["severity"] for f in ordered),
        "findings": ordered,
        "stats": stats or {},
    }


def copy_reason(path: Path, repo: Path) -> str | None:
    try:
        parts = Path(path).resolve().relative_to(Path(repo).resolve()).parts[:-1]
    except ValueError:
        return None
    archived = next((part for part in parts if COPY_PART.search(part)), None)
    if archived:
        return "historical/copy directory " + archived
    if ".session" in parts and "artifacts" in parts and "fixtures" in parts:
        return ".session artifact explicitly stored under fixtures"
    if "before" in parts and any(re.match(r"^\d{4}-\d{2}-\d{2}(?:-|$)", part) for part in parts) and any(part in (".claude", ".codex") for part in parts):
        return "dated before snapshot preserving a runtime-tree path"
    return None


def is_copy(path, repo):
    return copy_reason(path, repo) is not None


def live_entries(entries, repo):
    return [entry for entry in entries if not is_copy(entry["path"], repo)]


def instruction_files(loaded):
    seen = {}
    for entry in live_entries(loaded.claude + loaded.codex, loaded.repo):
        display = entry["real"] if Path(entry["path"]).is_symlink() else entry["path"]
        seen.setdefault(entry["real"], display)
    return [Path(path) for _real, path in sorted(seen.items(), key=lambda item: item[1])]


def gate_size(loaded):
    findings = []
    unconditional_lines = 0
    conditional_lines = 0
    unconditional_chars = 0
    conditional_chars = 0
    for entry in loaded.claude:
        if entry["condition"] == "unconditional":
            unconditional_lines += entry["lines"]
            unconditional_chars += entry["chars"]
        else:
            conditional_lines += entry["lines"]
            conditional_chars += entry["chars"]
        tokens = round(entry["chars"] / CHARS_PER_TOKEN)
        if entry["bytes"] > CLAUDE_SKIP_BYTES:
            findings.append(finding(entry["path"], 1, "G1", "warn", str(entry["bytes"]) + " bytes exceeds the 4 MiB limit; Claude Code skips this file"))
        if entry["lines"] > FILE_LINE_ADVICE:
            findings.append(finding(entry["path"], 1, "G1", "report", str(entry["lines"]) + " lines, ~" + str(tokens) + " est. tokens; above the 200-line advisory target, propose extraction (never an @path split, which loads at launch)"))
    if unconditional_lines > AGGREGATE_LINE_ADVICE:
        first = next((e["path"] for e in loaded.claude if e["condition"] == "unconditional"), loaded.claude[0]["path"] if loaded.claude else "")
        findings.append(finding(first, 1, "G1", "report", "unconditional aggregate " + str(unconditional_lines) + " lines, ~" + str(round(unconditional_chars / CHARS_PER_TOKEN)) + " est. tokens across the concatenated set; above the 400-line aggregate advisory"))
    copies = sorted({entry["path"] for entry in loaded.claude + loaded.codex if is_copy(entry["path"], loaded.repo)})
    if copies:
        findings.append(finding(copies[0], 1, "G1", "warn", str(len(copies)) + " historical instruction artifacts remain discoverable and may load if their subtree is read; other gates skip current-policy assertions for these classified copies: " + ", ".join(path + " (" + copy_reason(path, loaded.repo) + ")" for path in copies[:10]) + (" and more" if len(copies) > 10 else "")))
    stats = {
        "files": len(loaded.claude),
        "unconditional_lines": unconditional_lines,
        "conditional_lines": conditional_lines,
        "unconditional_est_tokens": round(unconditional_chars / CHARS_PER_TOKEN),
        "conditional_est_tokens": round(conditional_chars / CHARS_PER_TOKEN),
        "token_note": "estimates at 3.7 characters per token; /context is authoritative",
    }
    return gate_result("G1", "claude-code loaded set (" + str(len(loaded.claude)) + " files); advisories at 200 lines per file and 400 unconditional aggregate", findings, stats)


def looks_like_path(text):
    text = text.strip()
    if not text or text.startswith(("http://", "https://", "#", "@")):
        return False
    if any(token in text for token in NOT_A_PATH):
        return False
    if " " in text:
        return False
    if text.startswith(("~", "/Users/", "./", "../")):
        return True
    if text.endswith("/") and "/" in text.rstrip("/"):
        return True
    return text.endswith(FILE_SUFFIXES)


class BasenameIndex:
    def __init__(self, roots):
        self.roots = [Path(r) for r in roots]
        self.index = None

    def build(self):
        self.index = {}
        for root in self.roots:
            if not root.is_dir():
                continue
            for current, dirs, files in os.walk(root):
                dirs[:] = sorted(d for d in dirs if d not in PRUNE)
                for name in files + dirs:
                    self.index.setdefault(name, []).append(str(Path(current) / name))

    def lookup(self, candidate):
        if self.index is None:
            self.build()
        tail = candidate.strip("./").rstrip("/")
        if not tail:
            return None
        name = Path(tail).name
        for found in sorted(self.index.get(name, [])):
            if found.endswith("/" + tail) or Path(found).name == tail:
                return found
        return None


def shorthand_index(args):
    roots = [args.pointer_root or args.repo] + [args.home / tree for tree in HOME_SHORTHAND_TREES]
    return BasenameIndex(roots)


def clean_pointer(candidate):
    candidate = candidate.strip().rstrip(".,;:")
    candidate = candidate.split("#", 1)[0]
    candidate = re.sub(r":\d+(?:-\d+)?$", "", candidate)
    return candidate


def pointer_bases(path, args):
    bases = []
    file_dir = Path(path).parent
    if args.pointer_root and is_within(file_dir, args.repo):
        bases.append(args.pointer_root / Path(os.path.relpath(file_dir, args.repo)))
    bases.append(file_dir)
    bases.append(args.pointer_root or args.repo)
    bases.append(args.cwd)
    if user_scope(path, args):
        bases.append(args.home)
    return bases


def user_scope(path, args):
    return is_within(path, args.home / ".claude") or is_within(path, args.home / ".codex")


def pointer_exists(candidate, path, args):
    if candidate.startswith("~"):
        return (args.home / candidate[1:].lstrip("/")).exists()
    if candidate.startswith("/"):
        return Path(candidate).exists()
    return any((base / candidate).exists() for base in pointer_bases(path, args))


def gate_pointers(loaded, store, args):
    findings = []
    index = shorthand_index(args)
    checked = 0
    globs = 0
    for path in instruction_files(loaded):
        text = store.text(path) or ""
        for number, raw, kind, _info in iter_lines(text):
            if kind != "text" or not raw.strip():
                continue
            assertive = NON_ASSERTIVE.search(raw) is None
            candidates = [m for m in BACKTICK.findall(raw) if looks_like_path(m)]
            candidates += [m for m in MD_LINK.findall(raw) if not m.startswith(("http://", "https://", "#", "mailto:")) and looks_like_path(m)]
            candidates += [m for m in BARE_PATH.findall(raw) if looks_like_path(m)]
            for candidate in dict.fromkeys(clean_pointer(c) for c in candidates):
                if not candidate:
                    continue
                if any(ch in candidate for ch in "*?["):
                    globs += 1
                    continue
                if candidate.startswith(SCRATCH_PREFIXES):
                    continue
                checked += 1
                if pointer_exists(candidate, path, args):
                    continue
                if not assertive:
                    findings.append(finding(path, number, "G2", "info", "absent `" + candidate + "` in prohibitive, example or creation context"))
                    continue
                elsewhere = None if candidate.startswith(("/", "~")) else index.lookup(candidate)
                if elsewhere:
                    findings.append(finding(path, number, "G2", "report", "shorthand pointer `" + candidate + "` resolves elsewhere as " + elsewhere))
                elif "/" not in candidate.rstrip("/"):
                    findings.append(finding(path, number, "G2", "report", "bare filename `" + candidate + "` not found in scope; name its directory or confirm it is meant generically"))
                elif user_scope(path, args) and not candidate.startswith(("/", "~")):
                    findings.append(finding(path, number, "G2", "report", "relative path `" + candidate + "` in a user-scope file resolves against whichever repository is active; absent in " + str(args.repo)))
                else:
                    findings.append(finding(path, number, "G2", "block", "dead pointer `" + candidate + "`: nothing by that name exists in scope"))
    scope = "backticks, Markdown links and absolute paths in every live loaded instruction file, scratch paths under /tmp skipped; resolved against the file directory, " + str(args.pointer_root or args.repo) + " and the working directory; shorthand searched under " + ", ".join(str(r) for r in index.roots) + "; block only for a directory-qualified path in assertive context"
    return gate_result("G2", scope, findings, {"checked": checked, "globs_skipped": globs})


def gate_model_phrases(loaded, store):
    findings = []
    for path in instruction_files(loaded):
        text = store.text(path) or ""
        for number, stripped in prose_atoms(text):
            if HEADING.match(stripped):
                continue
            body = re.sub(r"[*_`>]", "", stripped)
            for pattern, cut_class, note in MODEL_PHRASES:
                match = pattern.search(body)
                if match:
                    findings.append(finding(path, number, "G3", "report", cut_class + " '" + match.group(0)[:60] + "': " + note))
    return gate_result("G3", "prose lines outside code in every live loaded instruction file; phrase families from the Fable 5 and 5.1 and GPT-6 Astra guides plus text Claude Code already injects (floor 2.1.273, last checked on 2.1.286); a lead for propose, never an edit by itself", findings)


def shingles(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return frozenset(tuple(words[i:i + 4]) for i in range(max(0, len(words) - 3)))


def scope_side(entry):
    return "user" if entry["scope"] in ("managed", "user", "user-rules", "global") else "project"


def gate_duplication(loaded, store):
    findings = []
    pairs = 0
    launch_claude = [e for e in live_entries(loaded.claude, loaded.repo) if e["condition"] == "unconditional"]
    for runtime, entries in (("claude-code", launch_claude), ("codex", live_entries(loaded.codex, loaded.repo))):
        atoms = []
        seen = set()
        side = {}
        for entry in entries:
            if entry["real"] in seen:
                continue
            seen.add(entry["real"])
            side[str(entry["path"])] = scope_side(entry)
            text = store.text(entry["path"]) or ""
            for number, stripped in prose_atoms(text):
                if HEADING.match(stripped) or len(stripped.split()) < 10:
                    continue
                grams = shingles(stripped)
                if grams:
                    atoms.append((entry["path"], entry["real"], number, stripped, grams))
        groups = {}
        for i in range(len(atoms)):
            for j in range(i + 1, len(atoms)):
                a = atoms[i]
                b = atoms[j]
                union = len(a[4] | b[4])
                if not union:
                    continue
                jaccard = len(a[4] & b[4]) / union
                if jaccard < 0.5:
                    continue
                pairs += 1
                if a[1] != b[1] and jaccard >= 0.9:
                    groups.setdefault((str(a[0]), str(b[0])), []).append((a, b, jaccard))
                    continue
                findings.append(finding(a[0], a[2], "G4", "report", runtime + " duplicate of " + str(b[0]) + ":" + str(b[2]) + " at 4-gram Jaccard " + format(jaccard, ".2f") + ": " + a[3][:90]))
        anchors = {}
        for key in sorted(groups):
            matches = groups[key]
            first_a, first_b, first_jaccard = matches[0]
            lines = ", ".join(str(a[2]) + "=" + str(b[2]) for a, b, _ in matches[:DUPLICATE_LINE_LIST])
            more = "" if len(matches) <= DUPLICATE_LINE_LIST else " and " + str(len(matches) - DUPLICATE_LINE_LIST) + " more"
            cross = side.get(str(first_a[0])) != side.get(str(first_b[0]))
            severity = "warn" if cross else "block"
            detail = str(first_b[0]) + " (" + str(len(matches)) + " atom" + ("s" if len(matches) != 1 else "") + ", this:other lines " + lines + more + ", first at " + format(first_jaccard, ".2f") + ")"
            anchor = anchors.setdefault((str(first_a[0]), first_a[2]), {"severity": "warn", "partners": [], "text": first_a[3][:90], "cross": False})
            anchor["partners"].append(detail)
            anchor["cross"] = anchor["cross"] or cross
            if severity == "block":
                anchor["severity"] = "block"
        for (path, line), anchor in sorted(anchors.items()):
            note = "; user-scope and project copies: a user-scope rule may require the duplicate, so check before proposing a delete" if anchor["cross"] else ""
            findings.append(finding(path, line, "G4", anchor["severity"], runtime + " duplicate at 4-gram Jaccard 0.90 or more of " + "; ".join(anchor["partners"]) + note + ": " + anchor["text"]))
    return gate_result("G4", "4-gram Jaccard over prose atoms of 10+ words across files loaded at launch per runtime, historical artifacts with copy/fixture/snapshot evidence skipped; block when two project-side files share an atom at 0.90, warn when the pair crosses user and project scope", findings, {"pairs": pairs})


def gate_emphasis(loaded, store):
    findings = []
    for path in instruction_files(loaded):
        text = store.text(path) or ""
        lines = []
        tokens = {"caps word": 0, "bold directive lead": 0, "bold-only line": 0, "ALL-CAPS run": 0}
        for number, raw in text_lines(text):
            if HEADING.match(raw):
                continue
            visible = INLINE_CODE.sub("", raw).strip()
            hit = False
            found = EMPHASIS_TOKEN.findall(visible)
            if found:
                tokens["caps word"] += len(found)
                hit = True
            lead = BOLD_LEAD.match(visible)
            if BOLD_ONLY.match(visible):
                tokens["bold-only line"] += 1
                hit = True
            elif lead and LEAD_DIRECTIVE.search(lead.group(1)):
                tokens["bold directive lead"] += 1
                hit = True
            if ALLCAPS_RUN.search(visible):
                tokens["ALL-CAPS run"] += 1
                hit = True
            if hit:
                lines.append(number)
        if len(lines) > EMPHASIS_LINE_BUDGET:
            detail = ", ".join(key + " x" + str(value) for key, value in tokens.items() if value)
            findings.append(finding(path, lines[0], "G6", "report", str(len(lines)) + " emphasised lines (lines " + ",".join(str(n) for n in lines[:30]) + "); " + detail + "; remove emphasis only on lines the operator names"))
        elif lines:
            findings.append(finding(path, lines[0], "G6", "info", str(len(lines)) + " emphasised lines"))
    return gate_result("G6", "uppercase NEVER, MUST, IMPORTANT, CRITICAL and ALWAYS, bold-only lines, bold leads carrying a directive word in any case, and ALL-CAPS runs of 25+ characters outside code; reported above 3 lines per file, never a block", findings)


def machinery(scope_root, store):
    root = Path(scope_root)
    found = {"hook": [], "ci": [], "lint": [], "permission": []}
    settings = [root / ".claude" / "settings.json", root / ".claude" / "settings.local.json"]
    for path in settings:
        text = store.text(path) if path.is_file() else None
        if text and '"hooks"' in text:
            found["hook"].append(str(path))
        if text and '"permissions"' in text:
            found["permission"].append(str(path))
    for directory, kind, pattern in ((root / ".claude" / "hooks", "hook", "*"), (root / ".husky", "hook", "*"), (root / ".github" / "workflows", "ci", "*.y*ml"), (root / ".circleci", "ci", "*.y*ml"), (root / ".semgrep", "lint", "*")):
        if directory.is_dir():
            for path in sorted(directory.glob(pattern)):
                if path.is_file() and not path.name.startswith("_"):
                    found[kind].append(str(path))
    hooks_dir = root / ".git" / "hooks"
    if hooks_dir.is_dir():
        for path in sorted(hooks_dir.iterdir()):
            if path.is_file() and not path.name.endswith(".sample"):
                found["hook"].append(str(path))
    for name, kind in ((".pre-commit-config.yaml", "hook"), ("lefthook.yml", "hook"), ("lefthook.yaml", "hook"), (".gitlab-ci.yml", "ci"), ("azure-pipelines.yml", "ci"), ("Jenkinsfile", "ci"), ("ruff.toml", "lint"), (".ruff.toml", "lint"), ("biome.json", "lint"), (".oxlintrc.json", "lint"), (".semgrep.yml", "lint"), (".golangci.yml", "lint")):
        if (root / name).is_file():
            found[kind].append(str(root / name))
    for path in sorted(root.glob("eslint.config.*")) + sorted(root.glob(".eslintrc*")):
        if path.is_file():
            found["lint"].append(str(path))
    package = root / "package.json"
    if package.is_file():
        text = store.text(package) or ""
        if '"husky"' in text or '"simple-git-hooks"' in text or '"lint-staged"' in text:
            found["hook"].append(str(package))
        try:
            scripts = json.loads(text).get("scripts", {})
        except (ValueError, AttributeError):
            scripts = {}
        if isinstance(scripts, dict) and any("lint" in key for key in scripts):
            found["lint"].append(str(package))
    pyproject = root / "pyproject.toml"
    if pyproject.is_file() and "[tool.ruff" in (store.text(pyproject) or ""):
        found["lint"].append(str(pyproject))
    return {key: sorted(set(value)) for key, value in found.items()}


def scope_root_for(path, args):
    if is_within(path, args.home / ".claude") or is_within(path, args.home / ".codex"):
        return args.home
    return args.repo


def span_paths(raw):
    found = []
    for span in BACKTICK.findall(raw):
        for part in span.split():
            if looks_like_path(part):
                found.append(clean_pointer(part))
    return [p for p in dict.fromkeys(found) if p]


def gate_enforcement(loaded, store, args):
    findings = []
    inventories = {}
    claims = 0
    index = shorthand_index(args)
    for path in instruction_files(loaded):
        root = scope_root_for(path, args)
        if str(root) not in inventories:
            inventories[str(root)] = machinery(root, store)
        inventory = inventories[str(root)]
        text = store.text(path) or ""
        for number, raw in text_lines(text):
            if HEADING.match(raw) or not ENFORCEMENT_CLAIM.search(raw):
                continue
            claims += 1
            kinds = sorted(kind for kind, pattern in KIND_WORDS.items() if pattern.search(raw))
            named = [n for n in span_paths(raw) if MACHINERY_SHAPE.search(n.rstrip("/"))]
            present = [n for n in named if pointer_exists(n, path, args) or index.lookup(n)]
            missing = [n for n in named if n not in present and "/" in n.rstrip("/")]
            executable = [n for n in present if not re.search(r"\.(?:json|ya?ml|toml)$", n)]
            unbacked = [k for k in kinds if not inventory[k]]
            if missing:
                findings.append(finding(path, number, "G7", "block", "enforcement claim names machinery that does not exist: " + ", ".join("`" + m + "`" for m in missing)))
            elif executable:
                findings.append(finding(path, number, "G7", "report", "enforcement claim names existing machinery " + ", ".join("`" + m + "`" for m in executable) + "; confirm it enforces this exact rule"))
            elif present and not (kinds and len(unbacked) == len(kinds)):
                findings.append(finding(path, number, "G7", "report", "enforcement claim names existing machinery " + ", ".join("`" + m + "`" for m in present) + "; confirm it enforces this exact rule"))
            elif kinds and len(unbacked) == len(kinds):
                findings.append(finding(path, number, "G7", "block", "enforcement claim of kind " + "/".join(kinds) + " but no " + "/".join(kinds) + " machinery exists under " + str(root)))
            else:
                bound = ", ".join(k + "=" + str(len(inventory[k])) for k in kinds) if kinds else "no machinery kind named"
                findings.append(finding(path, number, "G7", "report", "enforcement claim, binding unverified (" + bound + "); confirm the named mechanism enforces this rule"))
    scope = "; ".join(root + ": " + ", ".join(kind + "=" + str(len(items)) for kind, items in sorted(inv.items())) for root, inv in sorted(inventories.items()))
    return gate_result("G7", "machinery probed per scope root (" + (scope or "no files") + "); hooks in .claude/settings.json, .claude/hooks, .husky, .git/hooks, pre-commit and lefthook; CI workflows; lint configs; permission rules; only machinery-shaped named paths can block", findings, {"claims": claims})


def command_segments(command):
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return None
    segments = []
    current = []
    for token in tokens:
        if token in ("&&", "||", ";", "|", "&", ";;"):
            if current:
                segments.append(current)
            current = []
            continue
        current.append(token)
    if current:
        segments.append(current)
    return segments


def python_payload_modules(payload):
    try:
        tree = ast.parse(payload)
    except SyntaxError:
        return None
    modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.append(node.module.split(".")[0])
    return sorted(set(modules))


def command_target(token: str, directory: Path, args) -> Path:
    if token.startswith("~/"):
        return args.home / token[2:]
    target = Path(token)
    return target if target.is_absolute() else directory / target


def classify_segment(tokens, path, args, index, directory=None):
    directory = Path(directory or args.pointer_root or args.cwd)
    while tokens and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0]):
        tokens = tokens[1:]
    if not tokens:
        return "unverified", "empty command"
    head = tokens[0]
    if head == "cd":
        return "skip", "directory change"
    if re.fullmatch(r"/[A-Za-z][\w-]*", head):
        return "skip", "runtime slash command, not a filesystem executable"
    if head.startswith(SCRATCH_PREFIXES):
        return "skip", "scratch path"
    if "/" in head:
        if command_target(head, directory, args).is_file():
            return "resolves", "script `" + head + "` exists; not run"
        elsewhere = index.lookup(head)
        if elsewhere:
            return "shorthand", "script `" + head + "` resolves only elsewhere as " + elsewhere
        return "missing", "script `" + head + "` does not exist"
    if head in ("python", "python3"):
        if "-c" in tokens:
            index = tokens.index("-c")
            payload = tokens[index + 1] if index + 1 < len(tokens) else ""
            modules = python_payload_modules(payload)
            if modules is None:
                return "unverified", "python -c payload does not parse"
            absent = [m for m in modules if m not in sys.stdlib_module_names and importlib.util.find_spec(m) is None]
            if absent:
                return "missing", "python module " + ", ".join("`" + m + "`" for m in absent) + " is not locatable by " + sys.executable + " (checked with importlib.util.find_spec, nothing imported)"
            return "resolves", "python -c imports locatable; not run"
    if head in ("python", "python3", "node", "ruby", "bash", "sh", "zsh"):
        payload_flags = {"-c", "-e", "--eval", "-p", "--print", "-m", "-r", "--require", "--loader", "--import"}
        if not any(token in payload_flags or any(token.startswith(flag + "=") for flag in payload_flags) for token in tokens[1:]):
            scripts = [token for token in tokens[1:] if not token.startswith("-")]
            suffixes = {"python": (".py",), "python3": (".py",), "node": (".js", ".mjs", ".cjs", ".ts"), "ruby": (".rb",), "bash": (".sh",), "sh": (".sh",), "zsh": (".sh",)}
            if scripts and scripts[0].endswith(suffixes[head]) and not scripts[0].startswith(SCRATCH_PREFIXES):
                target = command_target(scripts[0], directory, args)
                if target.is_file():
                    return "resolves", "script `" + scripts[0] + "` exists in " + str(directory) + "; not run"
                return "missing", "script `" + scripts[0] + "` does not exist in " + str(directory)
    if head in ("npm", "pnpm", "yarn", "bun"):
        arguments = []
        position = 1
        while position < len(tokens):
            token = tokens[position]
            if token in ("--prefix", "--dir", "--cwd", "-C") and position + 1 < len(tokens):
                directory = command_target(tokens[position + 1], directory, args)
                position += 2
                continue
            if token.startswith(("--prefix=", "--dir=", "--cwd=")):
                directory = command_target(token.split("=", 1)[1], directory, args)
            elif not token.startswith("-"):
                arguments.append(token)
            position += 1
        script = arguments[1] if len(arguments) >= 2 and arguments[0] in ("run", "run-script") else arguments[0] if arguments and arguments[0] in ("test", "start", "stop", "restart") else None
        if script is None:
            return "unverified", "package-manager command is not a named run or lifecycle script; not run"
        package = directory / "package.json"
        if package.is_file():
            try:
                scripts = json.loads(package.read_text(encoding="utf-8")).get("scripts", {})
            except (ValueError, OSError, AttributeError):
                return "unverified", "cannot parse scripts in " + str(package)
            if not isinstance(scripts, dict):
                return "unverified", "unsupported scripts object in " + str(package)
            if script not in scripts:
                return "missing", head + " script `" + script + "` is absent from " + str(package)
            return "resolves", head + " script `" + script + "` exists in " + str(package) + "; not run"
        return "unverified", "no package.json in command working directory " + str(directory)
    if head in ("make", "gmake"):
        return classify_make(tokens[1:], path, args)
    if shutil.which(head) is None:
        return "missing", "binary `" + head + "` is not on PATH"
    return "resolves", "binary `" + head + "` is on PATH; not run"


def make_arguments(arguments):
    directory = None
    makefile = None
    targets = []
    pending = None
    for token in arguments:
        if pending:
            if pending == "directory":
                directory = token
            else:
                makefile = token
            pending = None
        elif token in ("-C", "--directory"):
            pending = "directory"
        elif token in ("-f", "--file", "--makefile"):
            pending = "file"
        elif token.startswith("--directory="):
            directory = token.split("=", 1)[1]
        elif token.startswith(("--file=", "--makefile=")):
            makefile = token.split("=", 1)[1]
        elif not token.startswith("-") and "=" not in token:
            targets.append(token)
    return directory, makefile, targets


def makefile_targets(text):
    names = set()
    for line in text.splitlines():
        match = MAKE_RULE.match(line)
        if match:
            names.update(match.group(1).split())
    return names


def classify_make(arguments, path, args):
    directory, makefile, targets = make_arguments(arguments)
    bases = [path.parent, Path(args.repo)] if directory is None else [(path.parent / directory), (Path(args.repo) / directory)]
    names = [makefile] if makefile else MAKEFILE_NAMES
    if makefile:
        found = next((base / makefile for base in bases if (base / makefile).is_file()), None)
    else:
        found = next((base / name for base in bases if base.is_dir() for name in names if name in set(os.listdir(base))), None)
    if found is None:
        return "unverified", "no " + "/".join(names) + " in " + ", ".join(sorted({str(b) for b in bases})) + "; make target " + (", ".join("`" + t + "`" for t in targets) or "default") + " unconfirmed"
    try:
        text = found.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "unverified", "cannot read " + str(found)
    defined = makefile_targets(text)
    absent = [t for t in targets if t not in defined]
    if not absent:
        return "resolves", "make target " + (", ".join("`" + t + "`" for t in targets) or "default") + " defined in " + str(found) + "; not run"
    if MAKE_INCLUDE.search(text):
        return "unverified", "make target " + ", ".join("`" + t + "`" for t in absent) + " not in " + str(found) + ", which includes other makefiles"
    return "missing", "make target " + ", ".join("`" + t + "`" for t in absent) + " is not defined in " + str(found)


def extract_commands(text):
    commands = []
    pending = None
    directory = None
    fence_directory = None
    example_context = False
    for number, raw, kind, info in iter_lines(text):
        stripped = raw.strip()
        if kind == "fence":
            fence_directory = directory
            continue
        if kind == "code" and info.split(" ")[0] in SHELL_INFO:
            if pending is not None:
                pending = (pending[0], pending[1] + " " + stripped.rstrip("\\").strip())
                if not stripped.endswith("\\"):
                    commands.append((pending[0], pending[1], example_context, fence_directory))
                    pending = None
                continue
            if not stripped or stripped.startswith(("#", "-", "|", ")", "}", "EOF")):
                continue
            command = stripped[2:] if stripped.startswith("$ ") else stripped
            if command.endswith("\\"):
                pending = (number, command.rstrip("\\").strip())
                continue
            commands.append((number, command, example_context, fence_directory))
            segments = command_segments(command)
            if segments:
                for segment in segments:
                    if segment[0] == "cd" and len(segment) == 2:
                        fence_directory = str(Path(fence_directory or ".") / segment[1])
            continue
        if kind != "text" or not stripped:
            continue
        if HEADING.match(raw):
            directory = None
            example_context = bool(re.search(r"\b(?:examples?|illustrative|sample|placeholder)\b", raw, re.IGNORECASE))
        package_context = re.search(r"\(\s*`([\w.-]+(?:/[\w.-]+)*/)`\s*\)", raw)
        if package_context:
            directory = package_context.group(1)
        if stripped.endswith(":") and re.search(r"\b(?:examples?|illustrative|sample|placeholder)\b", raw, re.IGNORECASE):
            example_context = True
        elif stripped.endswith(":") and not HEADING.match(raw):
            example_context = False
        if stripped.endswith(":") and re.search(r"\bscripts?\s+(?:should|must)\s+support\s+both\b", raw, re.IGNORECASE):
            example_context = True
        descriptive_example = re.search(r"\b(?:allows?|illustrates?|demonstrates?)\b[^.]*\bscripts?\b", raw, re.IGNORECASE)
        assertive = NON_ASSERTIVE.search(raw) is None and not example_context and descriptive_example is None
        for span in BACKTICK.findall(raw):
            span = span.strip()
            if re.search(r"[^ ]\|[^ ]", span) or "…" in span or "..." in span:
                continue
            first = span.split(" ")[0]
            if first in COMMAND_WORDS and " " in span:
                commands.append((number, span, not assertive, directory))
            elif SCRIPT_TOKEN.match(first):
                commands.append((number, span, not assertive, directory))
    return commands


def gate_executable(loaded, store, args):
    findings = []
    counts = {"resolves": 0, "missing": 0, "unverified": 0, "shorthand": 0}
    index = shorthand_index(args)
    for path in instruction_files(loaded):
        text = store.text(path) or ""
        for number, command, exemplary, context_directory in extract_commands(text):
            directory = Path(args.pointer_root or args.cwd)
            if context_directory:
                directory = command_target(context_directory, directory, args)
            segments = command_segments(command)
            if segments is None:
                counts["unverified"] += 1
                findings.append(finding(path, number, "G8", "report", "`" + command[:80] + "` unverified: could not tokenize"))
                continue
            for tokens in segments:
                if tokens[0] == "cd" and len(tokens) == 2:
                    directory = command_target(tokens[1], directory, args)
                status, detail = classify_segment(tokens, path, args, index, directory)
                if status == "skip":
                    continue
                counts[status] = counts.get(status, 0) + 1
                segment = " ".join(tokens)
                caution = "; destructive or networked, never run by this skill" if DESTRUCTIVE.search(segment) else ""
                if status == "missing":
                    binary = detail.startswith("binary")
                    severity = "report" if exemplary or binary else "block"
                    note = "; the binary may be project-local or installed in another shell" if binary else ""
                    findings.append(finding(path, number, "G8", severity, detail + note + caution))
                elif status in ("unverified", "shorthand"):
                    findings.append(finding(path, number, "G8", "report", "`" + segment[:80] + "` " + status + ": " + detail + caution))
                else:
                    findings.append(finding(path, number, "G8", "info", detail + caution))
    scope = "shell-fenced blocks and command-shaped inline code (pattern notation and runtime slash commands skipped); resolve cd, named package sections and package-manager directory flags before checking scripts, including interpreter target arguments; literal examples report rather than block; binaries on PATH, make targets and python -c imports; dynamic shell directories remain unverified; no command is ever executed"
    return gate_result("G8", scope, findings, counts)


def gate_contract(loaded, store, args, dead_pointer_files):
    findings = []
    for path in instruction_files(loaded):
        raw = store.data(path) or b""
        text = raw.decode("utf-8", errors="replace")
        own_name = path.name
        for number, line in text_lines(text):
            names = sorted(set(INSTRUCTION_NAME.findall(line)))
            mentions_self = own_name in names or re.search(r"\bthis file\b", line, re.IGNORECASE)
            named_paths = sorted(path.parent / n for n in names if (path.parent / n).exists())
            if re.search(r"\beach\b", line, re.IGNORECASE):
                targets = sorted(set(named_paths) | {path})
            elif named_paths:
                targets = named_paths
            else:
                targets = [path] if mentions_self else []
            exact = CONTRACT_EXACT.search(line)
            wc = CONTRACT_WC.search(line)
            if wc:
                target = command_target(wc.group(1).strip(), Path(args.pointer_root or args.repo), args)
                if target.is_file():
                    measured = count_newlines(store.data(target) or b"")
                    wanted = int(wc.group(2))
                    if measured != wanted:
                        findings.append(finding(path, number, "G9", "block", "requires wc -l " + str(target) + " to report exactly " + str(wanted) + "; measured " + str(measured) + "; changing this criterion requires an authorized policy decision"))
            if exact and targets:
                wanted = int(exact.group(1))
                terminated = bool(exact.group(2))
                for target in targets:
                    data = store.data(target) or b""
                    newlines = data.count(b"\n")
                    last = data[-1:] if data else b""
                    records = newlines + (1 if data and last != b"\n" else 0)
                    problems = []
                    if newlines != wanted:
                        problems.append("wc -l " + str(newlines) + " (awk " + str(records) + ")")
                    if terminated and last != b"\n":
                        problems.append("final byte " + repr(last.decode("utf-8", errors="replace")) + " is not a newline")
                    if problems:
                        findings.append(finding(path, number, "G9", "block", "claims " + target.name + " is exactly " + str(wanted) + (" newline-terminated" if terminated else "") + " lines; measured " + "; ".join(problems)))
            cap = CONTRACT_CAP.search(line)
            if cap and mentions_self:
                limit = int(cap.group(1))
                newlines = (store.data(path) or b"").count(b"\n")
                if newlines >= limit:
                    findings.append(finding(path, number, "G9", "block", "claims under " + str(limit) + " lines; measured " + str(newlines)))
            if CONTRACT_TWIN.search(line):
                for name in names:
                    other = path.parent / name
                    if other == path or not other.exists():
                        continue
                    mine = store.data(path) or b""
                    theirs = store.data(other) or b""
                    if mine != theirs:
                        mine_lines = mine.split(b"\n")
                        their_lines = theirs.split(b"\n")
                        first = next((i + 1 for i in range(max(len(mine_lines), len(their_lines))) if (mine_lines[i] if i < len(mine_lines) else None) != (their_lines[i] if i < len(their_lines) else None)), 0)
                        findings.append(finding(path, number, "G9", "block", "claims byte-identical with " + name + "; files differ, first difference at line " + str(first)))
            if CONTRACT_RESOLVES.search(line) and str(path) in dead_pointer_files:
                findings.append(finding(path, number, "G9", "block", "claims every path resolves; G2 found " + str(dead_pointer_files[str(path)]) + " dead pointer(s) in this file"))
    readers = contract_readers(loaded, store, args)
    for target, uses in sorted(readers.items()):
        findings.append(finding(target, 1, "G9", "warn", "consumed by " + ", ".join(uses[:6]) + (" and more" if len(uses) > 6 else "") + "; inspect the consumed property and proposed edit; an authorized edit clears this reason when the contract is verified unaffected or satisfied"))
    root = args.pointer_root or args.repo
    return gate_result("G9", "self-referential claims (exact or capped line counts, wc -l criteria, newline termination, byte-identical twins, every path resolving) in each live loaded instruction file; resolved instruction targets with static content/path consumption evidence in " + ", ".join(CONTRACT_DIRS) + " and root build files in " + str(root) + "; filename mentions alone do not establish consumers, and dynamic flows remain unverified", findings, {"contract_readers": sum(len(v) for v in readers.values())})


def contract_readers(loaded, store, args):
    root = Path(args.pointer_root or args.repo)
    candidates = []
    for name in CONTRACT_ROOT_FILES:
        if (root / name).is_file():
            candidates.append(root / name)
    for directory in CONTRACT_DIRS:
        base = root / directory
        if not base.is_dir():
            continue
        for current, dirs, files in os.walk(base):
            dirs[:] = sorted(d for d in dirs if d not in PRUNE)
            for name in sorted(files):
                if name.endswith(CONTRACT_SUFFIXES):
                    candidates.append(Path(current) / name)
    project = {}
    for entry in live_entries(loaded.claude + loaded.codex, loaded.repo):
        if entry["scope"] in ("managed", "user", "user-rules", "global"):
            continue
        project.setdefault(os.path.realpath(entry["path"]), entry["path"])
    readers = {}
    for candidate in candidates:
        text = store.text(candidate) or ""
        if len(text) > 2 * 1024 * 1024:
            continue
        lines = text.split("\n")
        for number, line in enumerate(lines, start=1):
            for match in CONTRACT_READER.finditer(line):
                named = match.group(2)
                referenced = command_target(named, root, args)
                target = project.get(os.path.realpath(referenced))
                if not target:
                    continue
                consumed = consumer_trace(lines, number - 1)
                if consumed:
                    read_line, property_name = consumed
                    use = os.path.relpath(candidate, root) + ":" + str(number) + " -> " + str(read_line + 1) + " (" + property_name + "; target " + str(referenced) + ")"
                    readers.setdefault(target, []).append(use)
    return {key: list(dict.fromkeys(value)) for key, value in readers.items()}


def consumer_trace(lines: list[str], origin: int) -> tuple[int, str] | None:
    line = lines[origin]
    direct_content = CONTENT_READ.search(line) or re.search(r"\]\s*\.content\b", line)
    direct_path = PATH_READ.search(line)
    if direct_content or direct_path:
        return origin, consumed_property(line, bool(direct_content))
    symbols = set()
    for index in range(origin, max(-1, origin - 32), -1):
        statement = lines[index]
        assignment = SOURCE_ASSIGNMENT.match(statement)
        loop = SOURCE_LOOP.search(statement)
        if assignment or loop:
            if index == origin or statement.rstrip().endswith(("[", "(", "{", ",")) or index < origin and not any(re.match(r"^\s*(?:\]|\)|\});?)\s*;?\s*$", value) for value in lines[index:origin]):
                symbols.add((assignment or loop).group(1))
            break
    if not symbols:
        return None
    for index in range(origin, len(lines)):
        statement = lines[index]
        if not any(re.search(r"\b" + re.escape(symbol) + r"\b", statement) for symbol in symbols):
            continue
        content = CONTENT_READ.search(statement)
        path_read = PATH_READ.search(statement)
        if content or path_read:
            return index, consumed_property(statement, bool(content))
        assignment = SOURCE_ASSIGNMENT.match(statement)
        loop = SOURCE_LOOP.search(statement)
        if assignment:
            symbols.add(assignment.group(1))
        if loop:
            symbols.add(loop.group(1))
        ruby_loop = re.search(r"\.each\s+do\s*\|([A-Za-z_]\w*)\|", statement)
        if ruby_loop:
            symbols.add(ruby_loop.group(1))
    return None


def consumed_property(line: str, content: bool) -> str:
    if not content:
        return "path existence or symlink relationship"
    if re.search(r"\breadlines\b|\bsplitlines\b|\bwc\s+-l\b|\.split\([\"']\\n", line):
        return "line records or matched line/vocabulary"
    if re.search(r"\.content\b|\.includes\(|\.match\(|\.find\(", line):
        return "matched prose or vocabulary"
    return "file content bytes/text; downstream constraints require inspection"


def import_stub_target(path, store):
    text = store.text(path) or ""
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.strip().startswith("#")]
    if not lines or len(lines) > 5:
        return None
    if all(l.startswith("@") for l in lines):
        return (path.parent / lines[0][1:]).resolve()
    return None


def imports_twin(path, twin_name, store):
    text = store.text(path) or ""
    return any(line.strip() == "@" + twin_name for line in text.split("\n"))


def gate_symlink(loaded, store, args):
    findings = []
    acknowledged = set()
    for raw in args.ack_canonical:
        acknowledged.add(os.path.realpath(raw))
        acknowledged.add(os.path.abspath(raw))
    directories = sorted({d for d in chain_dirs(args.cwd) if is_within(d, args.repo)} | {Path(p).parent for p in walk_files(args.repo, {"CLAUDE.md", "AGENTS.md"}) if not is_copy(p, args.repo)})
    for directory in directories:
        claude = directory / "CLAUDE.md"
        agents = directory / "AGENTS.md"
        for member in (claude, agents):
            if member.is_symlink():
                target = os.path.realpath(member)
                ack = target in acknowledged or os.path.abspath(member) in acknowledged
                findings.append(finding(member, 1, "G10", "report" if ack else "block", member.name + " is a symlink to " + os.readlink(member) + "; both names read the canonical file " + target + ("; acknowledged" if ack else "; writes blocked until --ack-canonical names the canonical file")))
        if not claude.is_file() or claude.is_symlink():
            continue
        stub = import_stub_target(claude, store)
        if stub is not None:
            ack = str(stub) in acknowledged or os.path.abspath(claude) in acknowledged
            findings.append(finding(claude, 1, "G10", "report" if ack else "block", "CLAUDE.md is an import stub for " + str(stub) + "; edits belong in " + stub.name + ("; acknowledged" if ack else "; writes blocked until --ack-canonical names the canonical file")))
            continue
        if agents.is_file() and not agents.is_symlink():
            if imports_twin(claude, "AGENTS.md", store):
                findings.append(finding(claude, 1, "G10", "report", "CLAUDE.md imports AGENTS.md and adds Claude-only lines; shared edits belong in AGENTS.md"))
            elif (store.data(claude) or b"") == (store.data(agents) or b""):
                findings.append(finding(claude, 1, "G10", "report", "CLAUDE.md and AGENTS.md are identical copies; an edit to one needs the matching edit to the other"))
            else:
                findings.append(finding(claude, 1, "G10", "report", "CLAUDE.md and AGENTS.md are divergent copies; propose a twin edit only where both files hold the same text"))
    return gate_result("G10", "CLAUDE.md and AGENTS.md in the same directory, along the working-directory chain inside " + str(args.repo) + " and every live subdirectory holding one", findings)


def concat_stats(left, right):
    return (left[0] * right[0], left[1] * right[0] + right[1] * left[0])


def parse_brace_sequence(text, index, stops):
    stats = (1, 0)
    while index < len(text) and text[index] not in stops:
        if text[index] == "{":
            group, after = parse_brace_group(text, index + 1)
            if group is None:
                stats = concat_stats(stats, (1, 1))
                index += 1
                continue
            stats = concat_stats(stats, group)
            index = after
            continue
        stats = concat_stats(stats, (1, 1))
        index += 1
    return stats, index


def parse_brace_group(text, index):
    count = 0
    length = 0
    while True:
        stats, index = parse_brace_sequence(text, index, ",}")
        count += stats[0]
        length += stats[1]
        if index >= len(text):
            return None, index
        if text[index] == "}":
            return (count, length), index + 1
        index += 1


def brace_expand_stats(pattern):
    stats, _ = parse_brace_sequence(pattern, 0, "")
    return stats


def bracket_malformed(pattern):
    depth = 0
    for char in pattern:
        if char == "[":
            depth += 1
        elif char == "]" and depth:
            depth -= 1
    return depth > 0


def gate_globs(loaded, store):
    findings = []
    rules = 0
    for entry in loaded.claude:
        if not entry["condition"].startswith("paths:"):
            continue
        rules += 1
        text = store.text(entry["path"]) or ""
        patterns = frontmatter_paths(text) or []
        total_count = 0
        total_bytes = 0
        for pattern in patterns:
            try:
                count, length = brace_expand_stats(pattern)
            except RecursionError:
                count, length = GLOB_PATTERN_BUDGET + 1, 0
            total_count += count
            total_bytes += length
            if bracket_malformed(pattern):
                findings.append(finding(entry["path"], 1, "G12", "block", "paths pattern `" + pattern + "` has an unclosed [ and matches no files while the rule looks live"))
        if total_count > GLOB_PATTERN_BUDGET or total_bytes > GLOB_BYTE_BUDGET:
            findings.append(finding(entry["path"], 1, "G12", "block", "paths list expands to " + str(total_count) + " patterns and " + str(total_bytes) + " bytes, over the 1,000-pattern or 4 MiB budget; over-budget patterns are used unexpanded and match nothing"))
        elif patterns:
            findings.append(finding(entry["path"], 1, "G12", "info", "paths list expands to " + str(total_count) + " patterns"))
    return gate_result("G12", "paths frontmatter on " + str(rules) + " loaded rules files; brace expansion counted per list against 1,000 patterns and 4 MiB; unclosed brackets", findings)


def codex_budget(config_path, store):
    if not config_path.is_file():
        return CODEX_DEFAULT_BUDGET, "default 32768 (no config at " + str(config_path) + ")"
    try:
        data = tomllib.loads(store.text(config_path) or "")
    except tomllib.TOMLDecodeError:
        return CODEX_DEFAULT_BUDGET, "default 32768 (config at " + str(config_path) + " does not parse)"
    value = data.get("project_doc_max_bytes")
    if isinstance(value, int) and not isinstance(value, bool) and value > 0:
        return value, "project_doc_max_bytes = " + str(value) + " from " + str(config_path)
    return CODEX_DEFAULT_BUDGET, "default 32768 (project_doc_max_bytes absent in " + str(config_path) + ")"


def gate_runtime_bytes(loaded, store, args, codex_root):
    findings = []
    budget, source = codex_budget(args.codex_config, store)
    remaining = budget
    stopped = False
    kept_total = 0
    for entry in loaded.codex:
        if not entry["budgeted"]:
            findings.append(finding(entry["path"], 1, "G13", "info", "global file " + str(entry["bytes"]) + " bytes, loaded as user instructions outside the project budget"))
            continue
        if stopped:
            findings.append(finding(entry["path"], 1, "G13", "block", "Codex drops this file: the project budget of " + str(budget) + " bytes was exhausted by earlier files"))
            continue
        if entry["bytes"] > remaining:
            findings.append(finding(entry["path"], 1, "G13", "block", "Codex truncates this " + str(entry["bytes"]) + "-byte file to " + str(remaining) + " bytes (budget " + str(budget) + " from " + source + ") and drops every deeper AGENTS.md"))
            kept_total += remaining
            remaining = 0
            stopped = True
            continue
        remaining -= entry["bytes"]
        kept_total += entry["bytes"]
        findings.append(finding(entry["path"], 1, "G13", "info", "loads in full, " + str(entry["bytes"]) + " bytes; " + str(remaining) + " bytes of budget left"))
    scope = "Codex project chain from " + str(codex_root) + " to " + str(args.cwd) + " (first nonempty AGENTS.override.md, AGENTS.md or selected project_doc_fallback_filenames per directory); budget " + source + "; only instruction discovery fields are reported, and unobserved config overrides/trust remain unknown"
    return gate_result("G13", scope, findings, {"budget": budget, "kept_bytes": kept_total})


def skill_dirs(root):
    if not root.is_dir():
        return []
    return sorted(child for child in root.iterdir() if child.is_dir() and (child / "SKILL.md").is_file())


def gate_generated(loaded, store):
    findings = []
    regions = 0
    for path in instruction_files(loaded):
        text = store.text(path) or ""
        lines = [(number, INLINE_CODE.sub("", line).strip()) for number, line in text_lines(text)]
        for index, (number, line) in enumerate(lines):
            start = GENERATED_START.match(line)
            if not start:
                continue
            name = start.group(1)
            end_pattern = re.compile(GENERATED_END.format(name=re.escape(name)))
            end = next((lines[j][0] for j in range(index + 1, len(lines)) if end_pattern.match(lines[j][1])), None)
            if end is None:
                findings.append(finding(path, number, "G16", "warn", "generated region `" + name + "` opens at line " + str(number) + " with no matching end marker; treat the rest of the file as generated until the operator says otherwise"))
                continue
            regions += 1
            findings.append(finding(path, number, "G16", "report", "lines " + str(number) + "-" + str(end) + " are generated region `" + name + "`; the generator rewrites them, so every item inside is blocked: generated"))
    return gate_result("G16", "paired standalone <!-- name:start --> and <!-- name:end --> markers in each live loaded instruction file; inline-code and fenced marker examples are literals", findings, {"regions": regions})


def installed_skills(args):
    names = set()
    roots = [args.home / ".claude" / "skills", args.repo / ".claude" / "skills", args.home / ".agents" / "skills", args.repo / ".agents" / "skills"]
    for root in roots:
        for directory in skill_dirs(root):
            names.add(directory.name)
    plugins = args.home / ".claude" / "plugins"
    for path in walk_files(plugins, {"SKILL.md"}):
        if path.parent.parent.name == "skills":
            names.add(path.parent.name)
    agents = {"general-purpose", "Explore", "Plan"}
    for root in (args.home / ".claude" / "agents", args.repo / ".claude" / "agents"):
        if root.is_dir():
            agents.update(p.stem for p in root.glob("*.md"))
    return names, agents, roots + [plugins]


def gate_required(loaded, store, args):
    findings = []
    names, agents, roots = installed_skills(args)
    index = shorthand_index(args)
    checked = 0
    for path in instruction_files(loaded):
        text = store.text(path) or ""
        for number, raw in text_lines(text):
            if not REQUIRED_LINE.search(raw):
                continue
            refs = []
            if re.search(r"skill|background", raw, re.IGNORECASE):
                for namespace, name in SKILL_REF.findall(INLINE_CODE.sub(lambda m: m.group(0).strip("`"), raw)):
                    if namespace.lower() in REF_NAMESPACE_IGNORE or namespace.isdigit():
                        continue
                    refs.append((namespace + ":" + name, name, "skill"))
            for first, second in NAMED_SKILL.findall(raw):
                token = first or second
                refs.append((token, token.split(":")[-1], "skill-or-agent"))
            for token, name, kind in dict.fromkeys(refs):
                checked += 1
                if name in names or (kind == "skill-or-agent" and name in agents):
                    continue
                findings.append(finding(path, number, "G15", "block", "required reference `" + token + "` resolves to no installed skill or agent"))
            if re.search(r"\bmust[- ]read\b|\bread\b[^.]*\bfirst\b|\brequired reading\b", raw, re.IGNORECASE):
                for candidate in [clean_pointer(m) for m in BACKTICK.findall(raw) if looks_like_path(m)]:
                    if not candidate or candidate.startswith(SCRATCH_PREFIXES):
                        continue
                    checked += 1
                    if pointer_exists(candidate, path, args):
                        continue
                    elsewhere = None if candidate.startswith(("/", "~")) else index.lookup(candidate)
                    if elsewhere:
                        findings.append(finding(path, number, "G15", "report", "required reading `" + candidate + "` resolves only as shorthand for " + elsewhere))
                    elif "/" in candidate.rstrip("/") and not user_scope(path, args):
                        findings.append(finding(path, number, "G15", "block", "required reading `" + candidate + "` does not exist"))
                    else:
                        findings.append(finding(path, number, "G15", "report", "required reading `" + candidate + "` not found in scope"))
    scope = "lines marked required or must-read in loaded instruction files; skills searched in " + ", ".join(str(r) for r in roots) + "; agents in .claude/agents at user and project scope plus built-ins"
    return gate_result("G15", scope, findings, {"references_checked": checked, "installed_skill_names": len(names)})


def parse_version(text):
    if not text:
        return None
    match = VERSION_TRIPLE.search(text)
    return tuple(int(part) for part in match.groups()) if match else None


def run(args):
    store = Store()
    loaded = LoadedSet(store, args.repo, args.cwd, args.home, args.managed, args.claude_settings, args.codex_home, args.codex_config, args.claude_settings_explicit)
    loaded.resolve_claude()
    codex_root = loaded.resolve_codex()
    gates = {}
    gates["G1"] = gate_size(loaded)
    gates["G2"] = gate_pointers(loaded, store, args)
    dead = {}
    for item in gates["G2"]["findings"]:
        if item["severity"] == "block":
            dead[item["path"]] = dead.get(item["path"], 0) + 1
    gates["G3"] = gate_model_phrases(loaded, store)
    gates["G4"] = gate_duplication(loaded, store)
    gates["G6"] = gate_emphasis(loaded, store)
    gates["G7"] = gate_enforcement(loaded, store, args)
    gates["G8"] = gate_executable(loaded, store, args)
    gates["G9"] = gate_contract(loaded, store, args, dead)
    gates["G10"] = gate_symlink(loaded, store, args)
    gates["G12"] = gate_globs(loaded, store)
    gates["G13"] = gate_runtime_bytes(loaded, store, args, codex_root)
    gates["G15"] = gate_required(loaded, store, args)
    gates["G16"] = gate_generated(loaded, store)
    version = parse_version(args.claude_version)
    if version is None:
        floor = "unverified (pass --claude-version with the output of claude --version)"
    elif version >= VERSION_FLOOR:
        floor = "met (floor 2.1.273)"
    else:
        floor = "below floor 2.1.273: loaded-set mechanics and subagent reports may differ; record this beside every result"
    summary = {key: 0 for key in ("block", "warn", "report", "indeterminate")}
    for gate in gates.values():
        if gate["verdict"] in summary:
            summary[gate["verdict"]] += 1
    return {
        "tool": "steward-lint " + TOOL_VERSION,
        "repo": str(args.repo),
        "cwd": str(args.cwd),
        "home": str(args.home),
        "claude_version": args.claude_version or "unrecorded",
        "version_floor": floor,
        "loaded": {"claude-code": loaded.claude, "codex": loaded.codex, "notes": sorted(set(loaded.notes))},
        "gates": [gates[key] for key in GATE_ORDER],
        "summary": summary,
        "exit": 1 if summary["block"] else 0,
    }


def render(report, show_all):
    out = []
    out.append(report["tool"])
    for key in ("repo", "cwd", "home", "claude_version", "version_floor"):
        out.append(key + ": " + str(report[key]))
    out.append("loaded set, claude-code (" + str(len(report["loaded"]["claude-code"])) + " files, concatenated in this order):")
    for entry in report["loaded"]["claude-code"]:
        tag = "unconditional" if entry["condition"] == "unconditional" else "conditional"
        out.append("  " + tag + " | " + entry["scope"] + " | " + entry["path"] + (" -> " + entry["real"] if entry["symlink"] else "") + " | lines=" + str(entry["lines"]) + " bytes=" + str(entry["bytes"]) + " est_tokens=" + str(round(entry["chars"] / CHARS_PER_TOKEN)) + " | " + entry["condition"] + " | " + entry["reason"])
    out.append("loaded set, codex (" + str(len(report["loaded"]["codex"])) + " files):")
    for entry in report["loaded"]["codex"]:
        out.append("  " + entry["scope"] + " | " + entry["path"] + " | bytes=" + str(entry["bytes"]) + " | budgeted=" + ("yes" if entry["budgeted"] else "no"))
    for note in report["loaded"]["notes"]:
        out.append("  note: " + note)
    for gate in report["gates"]:
        counts = {}
        for item in gate["findings"]:
            counts[item["severity"]] = counts.get(item["severity"], 0) + 1
        tally = " ".join(key + "=" + str(counts[key]) for key in ("block", "warn", "report", "info") if counts.get(key))
        stats = " ".join(key + "=" + str(value) for key, value in gate["stats"].items())
        out.append(gate["gate"] + " " + gate["name"] + " | verdict: " + gate["verdict"] + " | " + (tally or "no findings") + (" | " + stats if stats else ""))
        out.append("  scope: " + gate["scope"])
        shown = gate["findings"] if show_all else [f for f in gate["findings"] if f["severity"] in ("block", "warn")]
        for item in shown:
            out.append("  " + item["path"] + ":" + str(item["line"]) + " | " + item["gate"] + " | " + item["severity"] + " | " + item["evidence"])
        hidden = len(gate["findings"]) - len(shown)
        if hidden:
            out.append("  " + str(hidden) + " report or info findings not listed; rerun with --all or --json to list them")
    out.append("summary: " + " ".join(key + "=" + str(value) for key, value in report["summary"].items()))
    out.append("exit: " + str(report["exit"]))
    return "\n".join(out) + "\n"


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="steward-lint", description="Offline static gates over the instruction set each runtime loads. No model, no network, never executes a command it finds.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--cwd")
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--managed", default=str(MANAGED_POLICY))
    parser.add_argument("--codex-config")
    parser.add_argument("--codex-home", help="Codex config root; defaults to CODEX_HOME or --home/.codex")
    parser.add_argument("--claude-settings", action="append", help="Selected Claude settings layers in precedence order; repeat to merge exclusions and loading options")
    parser.add_argument("--pointer-root")
    parser.add_argument("--claude-version")
    parser.add_argument("--ack-canonical", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args(argv)
    args.repo = Path(args.repo).expanduser().resolve()
    args.cwd = Path(args.cwd).expanduser().resolve() if args.cwd else args.repo
    args.home = Path(args.home).expanduser().resolve()
    args.managed = Path(args.managed)
    args.codex_home = Path(args.codex_home or os.environ.get("CODEX_HOME") or args.home / ".codex").expanduser().resolve()
    args.codex_config = Path(args.codex_config).expanduser().resolve() if args.codex_config else args.codex_home / "config.toml"
    args.claude_settings_explicit = bool(args.claude_settings)
    args.claude_settings = [Path(path).expanduser().resolve() for path in args.claude_settings] if args.claude_settings else [args.home / ".claude" / "settings.json", args.repo / ".claude" / "settings.json", args.repo / ".claude" / "settings.local.json"]
    args.pointer_root = Path(args.pointer_root).expanduser().resolve() if args.pointer_root else None
    args.ack_canonical_raw = list(args.ack_canonical)
    args.ack_canonical = [str(Path(p).expanduser()) for p in args.ack_canonical]
    return args


def main(argv):
    try:
        args = parse_args(argv)
    except SystemExit as exit_signal:
        return 2 if exit_signal.code else 0
    if not args.repo.is_dir() or not args.cwd.is_dir():
        sys.stderr.write("steward-lint: repository or working directory is not a readable directory\n")
        return 2
    if not is_within(args.cwd, args.repo):
        sys.stderr.write("steward-lint: --cwd must be inside --repo\n")
        return 2
    report = run(args)
    if args.json:
        sys.stdout.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    else:
        sys.stdout.write(render(report, args.all))
    return report["exit"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
