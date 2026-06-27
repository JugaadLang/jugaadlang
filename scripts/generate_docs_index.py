#!/usr/bin/env python3
"""
Generate docs/README.md — Auto-generates the documentation index
by scanning the docs/ directory for files and extracting metadata.

Usage:
    python scripts/generate_docs_index.py

The script reads the first H1 (# Title) from each .md file in docs/
and combines it with a built-in topic/description mapping to produce
a well-formatted index at docs/README.md.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT_FILE = DOCS_DIR / "README.md"

# ── File metadata: topic category, description, and best-for tag ──────────────
# Keys are filenames (without path). Add new files here when creating docs.

FILE_META: dict[str, dict[str, str]] = {
    "Specs.md": {
        "topic": "Getting Started",
        "description": "Complete language specification — syntax, keywords, data types, control flow, functions, classes, pattern matching, async, comprehensions, and more.",
        "best_for": "Learning the language",
        "icon": "📗",
    },
    "keywords.md": {
        "topic": "Getting Started",
        "description": "Dual Hindi/English keyword mappings with Python equivalents. All control flow, operators, built-in function mappings, and fun functions.",
        "best_for": "Quick lookup",
        "icon": "📖",
    },
    "errors.md": {
        "topic": "Getting Started",
        "description": "All 24 humorous Hindi error types with titles, translations, when-they-occur explanations, and the error display format.",
        "best_for": "Understanding errors",
        "icon": "🎭",
    },
    "architecture.md": {
        "topic": "Architecture & Development",
        "description": "Full transpilation pipeline (Lexer → Parser → Transformer → compile → exec), directory structure, and detailed descriptions of all core components.",
        "best_for": "Understanding internals",
        "icon": "🏛️",
    },
    "contributing.md": {
        "topic": "Architecture & Development",
        "description": "Development setup, coding standards, adding keywords/modules, release process, and PR guidelines.",
        "best_for": "Contributing code",
        "icon": "🤝",
    },
    "cli.md": {
        "topic": "Reference",
        "description": "All `jug` CLI commands: `run`, `repl`, `install`, `remove`, `update`, `search`, `new`, `compile`, `check`, `typecheck`, with examples.",
        "best_for": "Using the CLI",
        "icon": "💻",
    },
    "stdlib.md": {
        "topic": "Reference",
        "description": "Standard library reference — `ganit` (math), `faili` (files), `json`, `samay` (time), `tantra` (system), `crypto`, `database` (ORM), `web` (HTTP/framework), and fun libraries.",
        "best_for": "Using stdlib",
        "icon": "📦",
    },
    "api.md": {
        "topic": "Reference",
        "description": "All public classes, methods, and data structures in `jugaadlang.lexer`, `.parser`, `.ast_nodes`, `.transformer`, `.runtime`, `.errors`, `.repl`, and `.package_manager`.",
        "best_for": "Writing extensions",
        "icon": "🔧",
    },
    "grammar.ebnf": {
        "topic": "Reference",
        "description": "Formal EBNF grammar — the complete context-free grammar for JugaadLang.",
        "best_for": "Language tooling",
        "icon": "📐",
    },
}

# ── Quick navigation ────────────────────────────────────────────────────────
# Auto-generated from best_for tags in FILE_META

def build_quick_nav(files_in_order: list[tuple[str, str, str, str, str]]) -> list[tuple[str, list[str]]]:
    """Build quick navigation from best_for tags."""
    nav = []
    for fname, title, topic, desc, best_for in files_in_order:
        if best_for and best_for != "—":
            nav.append((best_for, [fname]))
    return nav

# Category ordering (topic groups appear in this order)
TOPIC_ORDER = ["Getting Started", "Architecture & Development", "Reference"]


def extract_title(filepath: Path) -> str | None:
    """Extract the first H1 heading (# Title) from a markdown file."""
    try:
        text = filepath.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return None


def classify(filepath: Path) -> str:
    """Classify files that aren't in the metadata map."""
    name = filepath.name.lower()
    if name == "readme.md":
        return "Index"
    return "Misc" if filepath.suffix not in (".md", ".ebnf") else "Other"


def generate() -> str:
    """Generate the full docs/README.md content."""
    lines: list[str] = []
    write = lines.append

    # ── Header ─────────────────────────────────────────────────────
    write("# JugaadLang Documentation 📚")
    write("")
    write(
        "Welcome to the official JugaadLang documentation. "
        "This index is **auto-generated** — run "
        "`python scripts/generate_docs_index.py` to regenerate it."
    )
    write("")
    write("---")
    write("")

    # Scan actual files in docs/
    actual_files: set[str] = set()
    for entry in sorted(DOCS_DIR.iterdir()):
        if entry.is_file() and entry.name != "README.md":
            actual_files.add(entry.name)

    # ── Collect files by topic ────────────────────────────────────
    topic_groups: dict[str, list[tuple[str, str, str, str]]] = {}
    # (filename, title, description, icon)

    for fname in actual_files:
        if fname == "README.md":
            continue
        filepath = DOCS_DIR / fname
        meta = FILE_META.get(fname)

        if meta:
            topic = meta["topic"]
            desc = meta["description"]
            icon = meta.get("icon", "📄")
        else:
            title = extract_title(filepath)
            if title:
                desc = title
            elif fname.endswith(".ebnf"):
                desc = f"EBNF grammar — {fname}"
            else:
                desc = f"Documentation file — {fname}"
            topic = classify(filepath)
            icon = "📄"

        title = extract_title(filepath) or fname
        topic_groups.setdefault(topic, []).append((fname, title, desc, icon))

    # ── Topic sections ────────────────────────────────────────────
    # Use defined order for known topics, append others alphabetically
    seen_topics = set()
    for topic in TOPIC_ORDER:
        files = topic_groups.pop(topic, [])
        if not files:
            continue
        seen_topics.add(topic)
        write(f"## {topic}")
        write("")
        write("| File | Description |")
        write("|---|---|")
        for fname, title, desc, icon in files:
            write(f"| [**{fname}**]({fname}) | {icon} {desc} |")
        write("")

    # Remaining topics (not in TOPIC_ORDER)
    for topic in sorted(topic_groups):
        files = topic_groups[topic]
        if topic in seen_topics:
            continue
        write(f"## {topic}")
        write("")
        write("| File | Description |")
        write("|---|---|")
        for fname, title, desc, icon in files:
            write(f"| [**{fname}**]({fname}) | {icon} {desc} |")
        write("")

    # ── File overview table ───────────────────────────────────────
    all_files: list[tuple[str, str, str, str, str]] = []
    for fname in actual_files:
        if fname == "README.md":
            continue
        meta = FILE_META.get(fname)
        filepath = DOCS_DIR / fname
        title = extract_title(filepath) or fname
        if meta:
            all_files.append((fname, title, meta["topic"], meta["description"], meta["best_for"]))
        else:
            all_files.append((fname, title, classify(filepath), title, "—"))

    write("## 📋 File Overview")
    write("")
    write("| # | File | Topics | Best For |")
    write("|---|---|---|---|")
    for i, (fname, title, topic, desc, best_for) in enumerate(sorted(all_files), 1):
        write(f"| {i} | [`{fname}`]({fname}) | {desc} | {best_for} |")
    write("")

    # ── Quick navigation ──────────────────────────────────────────
    quick_nav = build_quick_nav(all_files)
    if quick_nav:
        write("## 🔍 Quick Navigation")
        write("")
        write("**I want to...**")
        write("")
        for goal, refs in quick_nav:
            ref_list = " + ".join(f"[`{r}`]({r})" for r in refs)
            write(f"- **{goal}**: Read {ref_list}")
        write("")
        write("---")
    write("")
    write(
        "> 💡 **Tip:** The main project [`README.md`](../README.md) at the project root "
        "includes quick-start guides, installation instructions, and a high-level overview."
    )
    write("")
    write("---")
    write("")
    write(
        "*This index was auto-generated by "
        "[`scripts/generate_docs_index.py`](../scripts/generate_docs_index.py).*"
    )

    return "\n".join(lines)


def main() -> None:
    content = generate()
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"✅ Generated {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    print(f"   Found {len(list(DOCS_DIR.iterdir())) - 1} documentation files")


if __name__ == "__main__":
    main()
