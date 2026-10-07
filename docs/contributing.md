# Contributing to JugaadLang

> **First time?** Read `CONTRIBUTING.md` at the project root for the quick-start guide.

This document provides deeper technical guidance for contributors.

---

## Development Setup

### Prerequisites

- Python 3.10 or later
- pip, uv, or your preferred Python package manager

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/jugaadlang.git
cd jugaadlang

# Editable install with all extras
pip install -e .[dev,all]

# Or with uv
uv sync --dev
```

### Verify Setup

```bash
jug --version
jug run examples/01_namaste_duniya.jug
jug repl
```

---

## Project Architecture

See `docs/architecture.md` for detailed architecture documentation.

### Quick Overview

```
Source (.jug)
  → Lexer (tokens)
  → Parser (JL AST)
  → Transformer (Python AST)
  → compile() (bytecode)
  → exec() (execute)
```

### Key Modules

| Module | Purpose |
|---|---|
| `jugaadlang/lexer/` | Tokenizer with indentation tracking |
| `jugaadlang/ast_nodes/` | AST node definitions (dataclasses) |
| `jugaadlang/parser/` | Recursive-descent parser |
| `jugaadlang/transformer/` | JL AST → Python AST converter |
| `jugaadlang/runtime/` | Execution engine + built-in functions |
| `jugaadlang/errors/` | Funny Hindi error formatter |
| `jugaadlang/stdlib/` | Standard library modules |
| `jugaadlang/package_manager/` | Package manager (pip wrapper) |
| `jugaadlang/repl/` | Interactive REPL |
| `jug_cli/` | Command-line interface |

---

## Coding Standards

### Code Style

- **Line length**: 100 characters
- **Formatter**: `ruff` (replaces black/isort/flake8)
- **Type hints**: Required for all function signatures (`from __future__ import annotations`)
- **Docstrings**: Required for public modules, classes, and functions

### Running the Formatter

```bash
ruff check .
ruff check --fix .
```

### Running Type Checks

```bash
mypy jugaadlang/ jug_cli/
```

### Running Tests

```bash
pytest
pytest -v              # verbose
pytest --cov           # with coverage
pytest tests/test_lexer.py  # single test file
```

### Test Structure

Tests are in the `tests/` directory using `pytest`:

| File | Tests |
|---|---|
| `tests/test_lexer.py` | Lexer tokenization |
| `tests/test_parser.py` | Parser AST generation |
| `tests/test_runtime.py` | Full execution pipeline |
| `tests/test_errors.py` | Error formatting |

---

## Adding a New Keyword

1. **Token type**: Add to `TokenType` enum in `jugaadlang/lexer/tokens.py`
2. **Keyword mapping**: Add to `KEYWORDS` dict in `jugaadlang/lexer/tokens.py`
3. **Lexer**: Ensure the lexer tokenizes the keyword (should work automatically via `_scan_identifier`)
4. **AST node**: If a new statement/expression type, add node class in `jugaadlang/ast_nodes/nodes.py`
5. **Parser**: Add parse method in `jugaadlang/parser/parser.py` and dispatch in `parse_statement()` or `parse_expression()`
6. **Transformer**: Add `visit_{NodeType}` method in `jugaadlang/transformer/to_python.py`
7. **Built-in mapping**: If a built-in function, add to `globals` dict in `jugaadlang/runtime/interpreter.py`
8. **REPL**: Add to `KEYWORDS_LIST` in `jugaadlang/repl/repl.py` for auto-completion
9. **Pygments lexer**: Add to `JugaadPygmentsLexer` in `jugaadlang/repl/repl.py` for syntax highlighting
10. **Tests**: Add test cases in the appropriate test file
11. **Docs**: Update `docs/keywords.md` and `docs/spec.md`

---

## Adding a Standard Library Module

1. Create a new `.py` file in `jugaadlang/stdlib/`
2. Import and register it in `jugaadlang/stdlib/__init__.py`
3. Add to the `local_stdlibs` list in `jugaadlang/package_manager/manager.py` for search support
4. Add tests for the module
5. Document in `docs/stdlib.md`

---

## Release Process

### Version Bumping

Version is defined in two places:
- `pyproject.toml` → `[project] version`
- `jugaadlang/__init__.py` → `__version__`

Update both using:

```bash
./update_version.sh 1.1.1
```

### Building

```bash
python -m build
```

Creates `dist/jugaadlang-{version}.tar.gz` and `dist/jugaadlang-{version}-py3-none-any.whl`.

### Publishing to PyPI

```bash
twine check dist/*
twine upload dist/*
```

### Creating a GitHub Release

1. Tag the release: `git tag v1.1.1`
2. Push tags: `git push --tags`
3. Create a release on GitHub → triggers automated `release.yml` workflow

---

## Pull Request Guidelines

1. **Branch from `main`** with a descriptive name (e.g., `feature/pattern-matching`, `fix/parser-error`)
2. **Keep PRs focused** on a single concern
3. **Include tests** for new features and bug fixes
4. **Ensure CI passes** (runs tests on Python 3.10–3.14 + ruff linting)
5. **Update documentation** if changing behavior or adding features
6. **Write meaningful commit messages**

### Commit Message Format

```
<type>: <short description>

<optional body>
```

Types: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `style:`, `chore:`, `ci:`

Example:
```
feat: add kismat() built-in for random number generation
```

---

## Debugging Tips

- Use `jug check file.jug` to validate syntax without execution
- Use `jug compile file.jug` to see the transpiled Python output
- Use `debug(variable)` inside JugaadLang code to inspect values
- Set `PYTHONDEVMODE=1` for extra Python runtime checks

---

## Working on the documentation website

The documentation portal is a static site at `website/docs/`. Its HTML and search index are generated from the Markdown files in `docs/` and `docs/guides/`. Navigation and page order are defined in `scripts/build_docs.py`; the shared layout lives in `docs/site/template.html`. Styles and browser behavior live in `website/docs/docs.css`, `theme.js`, and `docs.js`.

Install the build dependency and regenerate after editing Markdown or the template:

```bash
python -m pip install -e ".[dev]" -r docs/requirements.txt
python scripts/build_docs.py
python scripts/build_docs.py --check
python -m pytest tests/test_documentation.py
python -m http.server 8000 --directory website
```

Open `http://localhost:8000/docs/`. Commit the generated HTML and search index along with source changes, so existing static hosting can serve the portal without a build step. CI checks that generated files match their sources. Do not edit generated HTML directly.

Guide code blocks marked `jugaadlang` followed by an expected `text` output block are executed in the documentation tests. Keep these examples deterministic and independent of network access. Check navigation, search, copy buttons, keyboard access, light/dark themes, and narrow screens when changing the portal UI.

Related: [architecture](architecture.html), [internal API](api.html), and [coding guidelines](practices.html).

## Getting Help

- **Issues**: https://github.com/JugaadLang/jugaadlang/issues
- **Discussions**: GitHub Discussions page
- **Email**: jugaadlang@atomicmail.io
