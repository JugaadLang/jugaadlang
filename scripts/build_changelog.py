#!/usr/bin/env python3
"""Generate and verify CHANGELOG.md from git tags and commit history.

Existing hand-written version sections are preserved verbatim; sections
missing from CHANGELOG.md are generated from git history. The
[Unreleased] section's body is preserved.

Usage:
    python scripts/build_changelog.py           # regenerate CHANGELOG.md
    python scripts/build_changelog.py --check   # exit 1 if stale
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"

HEADER = "# Changelog\n\nAll notable changes to **JugaadLang** will be documented in this file.\n"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def list_tags() -> list[str]:
    out = git("tag", "--sort=-v:refname")
    tags = [t for t in out.splitlines() if t]
    # Exclude pre-release/beta tags from the main changelog.
    return [t for t in tags if "-beta" not in t and "-alpha" not in t and "-rc" not in t]


def tag_date(tag: str) -> str:
    return git("log", "-1", "--format=%cs", tag)


CATEGORY_MAP = {
    "feat": "Added",
    "feature": "Added",
    "add": "Added",
    "fix": "Fixed",
    "bugfix": "Fixed",
    "security": "Security",
    "perf": "Performance",
    "refactor": "Changed",
    "change": "Changed",
    "style": "Changed",
    "chore": "Changed",
    "docs": "Documentation",
    "test": "Tests",
    "ci": "CI/CD",
    "build": "CI/CD",
    "remove": "Removed",
    "revert": "Removed",
}

CATEGORY_ORDER = ["Added", "Changed", "Fixed", "Security", "Performance", "Removed", "Documentation", "Tests", "CI/CD", "Other"]


def categorize(subject: str) -> tuple[str, str]:
    m = re.match(r"^(\w+)(?:\([^)]*\))?[!:]\s*(.*)$", subject)
    if m:
        prefix, rest = m.group(1).lower(), m.group(2).strip()
        category = CATEGORY_MAP.get(prefix)
        if category:
            return category, rest[0].upper() + rest[1:] if rest else subject
    return "Other", subject[0].upper() + subject[1:] if subject else subject


def format_commits(commits: list[str]) -> str:
    groups: dict[str, list[str]] = {}
    for subject in commits:
        category, text = categorize(subject)
        groups.setdefault(category, []).append(text)
    blocks = []
    for category in CATEGORY_ORDER:
        if category in groups:
            items = "\n".join(f"- {t}" for t in groups[category])
            blocks.append(f"### {category}\n{items}")
    return "\n\n".join(blocks) + "\n"


def commits_between(prev: str | None, tag: str) -> list[str]:
    rev_range = f"{prev}..{tag}" if prev else tag
    out = git(
        "log", rev_range, "--no-merges", "--format=%s",
    )
    skip = re.compile(r"^(chore: bump version|Merge |dependabot|style)", re.IGNORECASE)
    return [line for line in out.splitlines() if line and not skip.search(line)]


def split_sections(text: str) -> tuple[str, dict[str, str]]:
    """Return (header_and_unreleased_prefix, {version: body})."""
    parts = re.split(r"(?m)^## ", text)
    prefix = parts[0]
    sections: dict[str, str] = {}
    unreleased_prefix = prefix
    for part in parts[1:]:
        first_line, _, body = part.partition("\n")
        m = re.match(r"\[?([^\]\s]+)\]?(?: - (\S+))?", first_line.strip())
        key = m.group(1) if m else first_line.strip()
        if key.lower() == "unreleased":
            unreleased_prefix = prefix + "## [Unreleased]\n" + body
        else:
            sections[key] = "## " + part.rstrip("\n") + "\n"
    return unreleased_prefix, sections


def build() -> str:
    existing = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
    _, curated = split_sections(existing)

    m = re.search(r"(?ms)^## \[Unreleased\].*?(?=^## |\Z)", existing)
    unreleased_block = m.group(0).rstrip("\n") + "\n\n" if m else "## [Unreleased]\n\n"

    out_text = HEADER + "\n" + unreleased_block

    tags = list_tags()

    # newest first
    for i, tag in enumerate(tags):
        version = tag.lstrip("v")
        if version in curated:
            out_text += curated[version].rstrip("\n") + "\n\n"
            continue
        prev = tags[i + 1] if i + 1 < len(tags) else None
        commits = commits_between(prev, tag)
        section = f"## [{version}] - {tag_date(tag)}\n\n"
        if commits:
            section += format_commits(commits)
        else:
            section += "### Changed\n- Maintenance release.\n"
        out_text += section + "\n"

    return out_text.rstrip("\n") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if CHANGELOG.md is stale")
    args = parser.parse_args()

    new = build()
    if args.check:
        old = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
        if old != new:
            print("CHANGELOG.md is stale. Run python scripts/build_changelog.py")
            return 1
        print("CHANGELOG.md is up to date.")
        return 0

    CHANGELOG.write_text(new, encoding="utf-8")
    print(f"Wrote {CHANGELOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
