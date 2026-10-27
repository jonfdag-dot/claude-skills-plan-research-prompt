#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import sys
import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

FRONTMATTER_KEY = re.compile(r'^([A-Za-z0-9_-]+):(?:[ \t]+(.*))?$')
BLOCK_SCALAR_INDICATORS = ('>', '>-', '>+', '|', '|-', '|+')


def unquote_scalar(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        inner = value[1:-1]
        if value[0] == "'":
            return inner.replace("''", "'")
        return inner.replace('\\"', '"').replace('\\\\', '\\')
    return value


def read_block_scalar(indicator, lines):
    stripped = [line.strip() for line in lines]
    while stripped and not stripped[-1]:
        stripped.pop()
    if indicator.startswith('|'):
        return '\n'.join(stripped)
    return ' '.join(part for part in stripped if part)


def read_nested_value(lines):
    items = [line.strip() for line in lines if line.strip()]
    if all(item == '-' or item.startswith('- ') for item in items):
        return [unquote_scalar(item[1:].strip()) for item in items]
    mapping = {}
    for item in items:
        key, _, value = item.partition(':')
        mapping[key.strip()] = unquote_scalar(value.strip())
    return mapping


def parse_frontmatter_without_yaml(frontmatter_text):
    frontmatter = {}
    lines = frontmatter_text.split('\n')
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith('#'):
            index += 1
            continue
        match = FRONTMATTER_KEY.match(line)
        if not match:
            return None, f"Invalid YAML in frontmatter: cannot parse line {index + 1}: {line.strip()}"
        key = match.group(1)
        raw = (match.group(2) or '').strip()
        index += 1
        block = []
        while index < len(lines) and (not lines[index].strip() or lines[index][:1] in (' ', '\t')):
            block.append(lines[index])
            index += 1
        if raw in BLOCK_SCALAR_INDICATORS:
            frontmatter[key] = read_block_scalar(raw, block)
        elif not raw:
            frontmatter[key] = read_nested_value(block) if any(part.strip() for part in block) else None
        else:
            continuation = ' '.join(part.strip() for part in block if part.strip())
            frontmatter[key] = unquote_scalar(raw + ' ' + continuation if continuation else raw)
    return frontmatter, None


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    if yaml is None:
        frontmatter, error = parse_frontmatter_without_yaml(frontmatter_text)
        if error:
            return False, error
    else:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return False, "Frontmatter must be a YAML dictionary"
        except yaml.YAMLError as e:
            return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
