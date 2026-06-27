# Contributing to JugaadLang

Welcome! We are excited that you want to contribute to JugaadLang — a Hindi-keyword programming language for Indian developers. By contributing, you help make coding more accessible to millions of developers.

Please take a moment to review this document before submitting contributions.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Reporting Issues & Feature Requests](#reporting-issues--feature-requests)
3. [Development Setup](#development-setup)
4. [Project Architecture](#project-architecture)
5. [Coding Standards](#coding-standards)
6. [Contribution Workflow](#contribution-workflow)
7. [Adding a New Keyword](#adding-a-new-keyword)
8. [Adding a Standard Library Module](#adding-a-standard-library-module)
9. [Pull Request Guidelines](#pull-request-guidelines)
10. [Release Process](#release-process)
11. [Debugging Tips](#debugging-tips)
12. [Getting Help](#getting-help)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](../CODE_OF_CONDUCT.md). Please report any unacceptable behavior to `jugaadlang@gmail.com`.

---

## Reporting Issues & Feature Requests

We use GitHub Issues to track bugs and feature requests.

### Standard Bugs & Feature Requests

For general bugs or proposing new features:

1. **Search** existing issues to ensure it hasn't already been reported.
2. **Open** a [new GitHub issue](https://github.com/jugaadlang/jugaadlang/issues).
3. **Provide** a clear description, reproduction steps, expected behavior, and system details (OS version, Python version).

### Security Bug Reports

> [!IMPORTANT]
> If you discover a security vulnerability or sensitive bug, **do not** open a public issue. Please refer to our [Security Policy](../SECURITY.md) and email the details confidentially to **jugaadlang@gmail.com**.

---

## Development Setup

### Prerequisites

- **Python 3.10 or later**
- `pip`, `uv`, or your preferred Python package manager
- `git` for version control

### Fork & Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/jugaadlang.git
cd jugaadlang
```

### Install in Editable Mode

```bash
# Install with development and all optional dependencies
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

For a detailed walkthrough, see [docs/architecture.md](architecture.md).

### Pipeline Overview

```
Source (.jug)
  → Lexer (jugaadlang/lexer/)        → Token stream
  → Parser (jugaadlang/parser/)      → JugaadLang AST
  → Transformer (jugaadlang/transformer/) → Python AST
  → compile()                        → Python bytecode
  → exec()                           → Execute in Python VM
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
| `tests/` | Pytest test suite |
| `examples/` | Example `.jug` programs |

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
ruff check --fix .   # auto-fix issues
```

### Running Type Checks

```bash
mypy jugaadlang/ jug_cli/
```

### Running Tests

```bash
pytest
pytest -v                          # verbose
pytest --cov                       # with coverage
pytest tests/test_lexer.py         # single test file
pytest tests/ -k "keyword"         # filter tests by keyword
```

### Test Structure

Tests use `pytest` in the `tests/` directory:

| File | What It Tests |
|---|---|
| `tests/test_lexer.py` | Lexer tokenization |
| `tests/test_parser.py` | Parser AST generation |
| `tests/test_runtime.py` | Full execution pipeline |
| `tests/test_errors.py` | Error formatting |
| `tests/test_english_keywords.py` | English keyword interop |

---

## Contribution Workflow

The recommended workflow for contributing code:

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name:
- `feature/` — new features (e.g., `feature/pattern-matching`)
- `fix/` — bug fixes (e.g., `fix/parser-error`)
- `docs/` — documentation changes (e.g., `docs/update-readme`)
- `refactor/` — code refactoring (e.g., `refactor/lexer-speed`)

### 2. Make Changes

Write clean, documented code following the [coding standards](#coding-standards).

### 3. Verify Locally

Before committing, run:

```bash
# Lint check
ruff check .

# Type check
mypy jugaadlang/ jug_cli/

# Test suite
pytest
```

All checks must pass before submitting a PR.

### 4. Write Tests

- **New features** must include tests
- **Bug fixes** should include a regression test
- Run the full test suite to ensure nothing breaks

### 5. Commit

Use clear, structured commit messages:

```
<type>: <short description>

<optional body>
```

Types: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `style:`, `chore:`, `ci:`

Examples:
```
feat: add kismat() built-in for random number generation
fix: handle 'not in' as compound comparison in parser
docs: add 100% Python feature parity section to README
```

### 6. Submit a Pull Request

Push your branch and open a PR on GitHub. The CI will automatically run:

- **Multi-version tests** (Python 3.10–3.14)
- **Ruff linting**
- **All checks must pass** before merging

---

## Adding a New Keyword

Follow these steps to add a new keyword to JugaadLang:

| Step | File | Action |
|---|---|---|
| 1 | `jugaadlang/lexer/tokens.py` | Add `TokenType` enum member |
| 2 | `jugaadlang/lexer/tokens.py` | Add to `KEYWORDS` dict |
| 3 | `jugaadlang/lexer/lexer.py` | Verify lexer tokenizes it (should work automatically) |
| 4 | `jugaadlang/ast_nodes/nodes.py` | Add AST node class (if new statement/expression type) |
| 5 | `jugaadlang/parser/parser.py` | Add parse method + dispatch in `parse_statement()` or `parse_expression()` |
| 6 | `jugaadlang/transformer/to_python.py` | Add `visit_{NodeType}` method |
| 7 | `jugaadlang/runtime/interpreter.py` | Add to `globals` dict (if a built-in function) |
| 8 | `jugaadlang/repl/repl.py` | Add to `KEYWORDS_LIST` for autocomplete |
| 9 | `jugaadlang/repl/repl.py` | Add to `JugaadPygmentsLexer` for syntax highlighting |
| 10 | `tests/` | Add test cases |
| 11 | `docs/keywords.md`, `docs/Specs.md` | Update documentation |

### Built-in Function Cheatsheet

If adding a Hindi built-in that maps to a Python builtin, ensure you add it in **both** of these places:

1. **Runtime**: `jugaadlang/runtime/interpreter.py` → the `self.globals` dict
2. **Transpiler**: `jugaadlang/transformer/to_python.py` → the `id_map` in `visit_Name()`

Runtime-only functions (like `kismat`, `chai`, `madad`) only need the runtime entry — do NOT add them to the transformer's `id_map`.

---

## Adding a Standard Library Module

1. Create a new `.py` file in `jugaadlang/stdlib/`
2. Import and register it in `jugaadlang/stdlib/__init__.py`
3. Add to the `local_stdlibs` list in `jugaadlang/package_manager/manager.py` for search support
4. Write tests for the module
5. Document in `docs/stdlib.md`

---

## Pull Request Guidelines

1. **Branch from `main`** with a descriptive name
2. **Keep PRs focused** on a single concern — one feature/fix per PR
3. **Include tests** for new features and bug fixes
4. **Ensure CI passes** — all automated checks must be green
5. **Update documentation** if changing behavior or adding features
6. **Write meaningful commit messages** (see format above)
7. **Reference related issues** in the PR description (e.g., `Closes #123`)

---

## Release Process

### Version Bumping

Version is defined in two places. Update both:

- `pyproject.toml` → `[project] version`
- `jugaadlang/__init__.py` → `__version__`

Use the convenience script:

```bash
./update_version.sh 1.1.1
```

### Building Distribution Packages

```bash
python -m build
```

Creates `dist/jugaadlang-{version}.tar.gz` and `dist/jugaadlang-{version}-py3-none-any.whl`.

### Publishing to PyPI

**Automated (recommended):**

1. Tag the release: `git tag v1.1.1 && git push --tags`
2. Create a new GitHub Release on the repository web interface
3. The **JugaadLang Release** workflow (`release.yml`) is triggered automatically:
   - Builds binary wheels and source tarballs
   - Uploads to PyPI using the secured `PYPI_API_TOKEN` secret

**Manual (maintainers only):**

```bash
pip install build twine
python -m build
twine check dist/*
twine upload dist/*
```

---

## Debugging Tips

| Technique | Description |
|---|---|
| `jug check file.jug` | Validate syntax without execution |
| `jug compile file.jug` | See the transpiled Python output |
| `debug(variable)` | Inspect variable values inside JugaadLang code |
| `PYTHONDEVMODE=1` | Enable extra Python runtime checks |
| `pytest -v --tb=long` | Run tests with verbose tracebacks |

---

## Getting Help

- **Issues**: [github.com/JugaadLang/jugaadlang/issues](https://github.com/JugaadLang/jugaadlang/issues)
- **Discussions**: GitHub Discussions page on the repository
- **Email**: `jugaadlang@gmail.com`

---

> 💡 **See also:** [docs/README.md](README.md) for a complete index of all documentation.
