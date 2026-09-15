"""Check published documentation links, search targets and runnable examples."""

from __future__ import annotations

import json
import re
import runpy
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website" / "docs"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            assert attributes["id"] not in self.ids, f"Duplicate ID: {attributes['id']}"
            self.ids.add(attributes["id"])
        for name in ("href", "src"):
            if name in attributes:
                self.links.append(attributes[name])


def assert_target(page, href, pages):
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return
    target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page.resolve()
    assert target.exists(), f"{page.name}: missing target {href}"
    if parsed.fragment and target.suffix == ".html":
        parsed_page = pages.get(target) or Page(target)
        assert unquote(parsed.fragment) in parsed_page.ids, f"{page.name}: missing anchor {href}"


def test_generated_pages_are_current():
    pytest.importorskip("markdown", reason="Install docs/requirements.txt to check generated pages")
    build = runpy.run_path(str(ROOT / "scripts" / "build_docs.py"))["build"]
    for filename, content in build().items():
        assert (SITE / filename).read_text(encoding="utf-8") == content, filename


def test_documentation_links_and_search_targets():
    pages = {path.resolve(): Page(path) for path in SITE.glob("*.html")}
    assert len(pages) >= 17
    for path, page in pages.items():
        for href in page.links:
            assert_target(path, href, pages)
    script = (SITE / "search-index.js").read_text(encoding="utf-8")
    entries = json.loads(script.removeprefix("window.DOCS_INDEX = ").rstrip(";\n"))
    assert entries
    for entry in entries:
        assert_target(SITE / "index.html", entry["url"], pages)


def examples():
    paths = sorted((ROOT / "docs" / "guides").glob("*.md")) + [ROOT / "docs" / "stdlib.md"]
    pattern = r"```jugaadlang\n(.*?)```(?:(?!```).)*?```text\n(.*?)```"
    for path in paths:
        for index, match in enumerate(re.finditer(pattern, path.read_text(encoding="utf-8"), re.S)):
            yield pytest.param(match[1], match[2], id=f"{path.stem}-{index + 1}")


@pytest.mark.parametrize("source, expected", list(examples()))
def test_documented_examples(source, expected, capsys, monkeypatch, tmp_path):
    from jugaadlang.cache.manager import cache_manager
    from jugaadlang.runtime.interpreter import JugaadInterpreter

    monkeypatch.setattr(cache_manager, "cache_dir", str(tmp_path / "cache"))
    monkeypatch.chdir(tmp_path)
    JugaadInterpreter("documentation.jug").run(source)
    assert capsys.readouterr().out.strip() == expected.strip()
