"""Build the static documentation portal. Run with --check in CI."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "website" / "docs"
REPO = "https://github.com/JugaadLang/jugaadlang"
PAGES = [
    ("Start here", "index", "Getting started", "guides/getting-started.md"),
    ("Start here", "installation", "Installation", "guides/installation.md"),
    ("Start here", "tutorials", "Tutorials & learning paths", "guides/tutorials.md"),
    ("Language", "syntax", "Syntax reference", "spec.md"),
    ("Language", "variables", "Variables & data types", "guides/variables.md"),
    ("Language", "operators", "Operators & expressions", "guides/operators.md"),
    ("Language", "control-flow", "Control flow", "guides/control-flow.md"),
    ("Language", "functions", "Functions & modules", "guides/functions.md"),
    ("Language", "keywords", "Keyword reference", "keywords.md"),
    ("Build & debug", "stdlib", "Standard library", "stdlib.md"),
    ("Build & debug", "cli", "Command-line tools", "cli.md"),
    ("Build & debug", "debugging", "Errors & debugging", "guides/debugging.md"),
    ("Build & debug", "practices", "Coding guidelines", "guides/practices.md"),
    ("Build & debug", "faq", "FAQ", "guides/faq.md"),
    ("Contribute", "contributing", "Contributor guide", "contributing.md"),
    ("Contribute", "architecture", "Architecture", "architecture.md"),
    ("Contribute", "api", "Internal API", "api.md"),
]


def navigation(active: str) -> str:
    """Render ordinary links so navigation works without JavaScript."""
    parts = []
    previous = None
    for group, slug, title, _ in PAGES:
        if group != previous:
            if previous:
                parts.append("</ul>")
            parts.append(f"<h2>{html.escape(group)}</h2><ul>")
            previous = group
        current = ' aria-current="page"' if slug == active else ""
        parts.append(f'<li><a href="{slug}.html"{current}>{html.escape(title)}</a></li>')
    return "".join(parts) + "</ul>"


def build() -> dict[str, str]:
    """Return deterministic HTML pages and a section-level search index."""
    from html.parser import HTMLParser

    class SearchSections(HTMLParser):
        def __init__(self, title: str, url: str):
            super().__init__()
            self.title, self.url = title, url
            self.sections: list[dict[str, str]] = []
            self.heading = title
            self.anchor = ""
            self.words: list[str] = []
            self.in_heading = False
            self.heading_words: list[str] = []

        def flush(self):
            text = " ".join(" ".join(self.words).split())
            if text:
                self.sections.append(
                    {
                        "title": self.title,
                        "heading": self.heading,
                        "url": self.url + self.anchor,
                        "text": text,
                    }
                )
            self.words = []

        def handle_starttag(self, tag, attrs):
            if tag in ("h1", "h2", "h3"):
                self.flush()
                self.anchor = "#" + dict(attrs).get("id", "")
                self.in_heading = True
                self.heading_words = []

        def handle_endtag(self, tag):
            if tag in ("h1", "h2", "h3"):
                self.in_heading = False
                self.heading = "".join(self.heading_words)

        def handle_data(self, data):
            self.words.append(data)
            if self.in_heading:
                self.heading_words.append(data)

    outputs = {}
    search = []
    template = (ROOT / "docs" / "site" / "template.html").read_text(encoding="utf-8")
    for index, (group, slug, title, source) in enumerate(PAGES):
        text = (ROOT / "docs" / source).read_text(encoding="utf-8")
        converter = markdown.Markdown(
            extensions=["fenced_code", "tables", "toc"],
            extension_configs={"toc": {"toc_depth": "2-3"}},
        )
        body = converter.convert(text)
        # Wrap wide tables in a horizontal scroll container for small screens.
        body = re.sub(
            r"(<table>.*?</table>)",
            r'<div class="table-scroll">\1</div>',
            body,
            flags=re.DOTALL,
        )
        parser = SearchSections(title, f"{slug}.html")
        parser.feed(body)
        parser.flush()
        search.extend(parser.sections)
        pager = []
        for offset, label in [(-1, "Previous"), (1, "Next")]:
            position = index + offset
            if 0 <= position < len(PAGES):
                _, target, caption, _ = PAGES[position]
                pager.append(
                    f'<a href="{target}.html"><span>{label}</span>{html.escape(caption)}</a>'
                )
        replacements = {
            "TITLE": html.escape(title),
            "GROUP": html.escape(group),
            "BODY": body,
            "NAV": navigation(slug),
            "TOC": converter.toc,
            "EDIT": f"{REPO}/edit/main/docs/{source}",
            "PAGER": "".join(pager),
        }
        page = template
        for key, value in replacements.items():
            page = page.replace("{{" + key + "}}", value)
        outputs[f"{slug}.html"] = page
    # External JS data works both on static hosts and with local file previews.
    outputs["search-index.js"] = (
        "window.DOCS_INDEX = "
        + json.dumps(search, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
        + ";\n"
    )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()
    outputs = build()
    stale = []
    DEST.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        path = DEST / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        print("Documentation is stale. Run python scripts/build_docs.py: " + ", ".join(stale))
        return 1
    print(f"{'Checked' if args.check else 'Built'} {len(PAGES)} documentation pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
