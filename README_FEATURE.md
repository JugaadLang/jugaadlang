# JugaadLang CLI Help Enhancement & Architecture Guide

## Overview & Background
This feature directly resolves [Issue #115](https://github.com/JugaadLang/jugaadlang/issues/115): **"[Feature]: Improve CLI help output with command descriptions and examples"**.

New users exploring JugaadLang often rely on the CLI help output (`jug --help`) to discover commands and syntax. Previously:
- The root CLI help only printed basic command names without usage patterns.
- Subcommands lacked practical examples.
- The `install` command description was truncated due to Click sentence-splitting on `e.g.`.
- Only `--help` was accepted, rejecting standard `-h`.

This enhancement introduces a custom Click command and group hierarchy (`JugaadGroup` and `JugaadCommand`) that provides structured, beautifully aligned, and terminal-safe **Examples** sections for the root CLI as well as all individual subcommands.

---

## Tech Stack & Architecture

- **Language**: Python 3.10+ (tested across 3.10 – 3.14)
- **CLI Framework**: [Click](https://click.palletsprojects.com/)
- **Terminal Styling & Output**: [Rich](https://rich.readthedocs.io/)
- **Transpilation Pipeline**:
  - `jugaadlang.lexer.lexer.Lexer`: Converts Roman Hindi keywords to language tokens.
  - `jugaadlang.parser.parser.Parser`: Builds an Abstract Syntax Tree (AST).
  - `jugaadlang.transformer.to_python.JugaadToPythonTransformer`: Compiles JugaadLang AST to native Python AST.
  - `jugaadlang.runtime.interpreter.JugaadInterpreter`: Executes Python AST with funny diagnostic error hooks.
- **Testing & Quality Assurance**:
  - `pytest` & `pytest-cov` (81%+ total test coverage)
  - `ruff` linting and style enforcement

---

## Components & Implementation Details

### 1. `JugaadCommand(click.Command)`
Custom Click Command class that stores `examples: list[tuple[str, str]]` and overrides `format_epilog` using Click's native `formatter.section("Examples")` and `formatter.write_dl(...)`. This guarantees identical column padding and word wrapping consistent with Click's native `Commands:` and `Options:` sections.

### 2. `JugaadGroup(click.Group)`
Custom Click Group class that:
- Sets `command_class = JugaadCommand` to automatically endow all `@main.command` subcommands with example support.
- Renders the root `Examples` table on `jug --help` or bare `jug` invocation.

### 3. Root Examples Registered
- `jug run <file.jug>` — Run a JugaadLang program
- `jug compile <file.jug>` — Compile a JugaadLang program to Python
- `jug repl` — Start the interactive REPL
- `jug install <package>` — Install a package
- `jug search <query>` — Search for packages
- `jug doctor` — Diagnose common setup issues
- `jug new <project_name>` — Create a new project boilerplate
- `jug check <file.jug>` — Validate syntax without executing

### 4. Subcommand Examples Registered
- **`jug run`**: `jug run hello.jug`, `jug run app.jug arg1 arg2`
- **`jug compile`**: `jug compile hello.jug`, `jug compile hello.jug -o hello.py`
- **`jug repl`**: `jug repl`
- **`jug install`**: `jug install chai`, `jug install web`
- **`jug remove`**: `jug remove chai`
- **`jug update`**: `jug update chai`
- **`jug search`**: `jug search chai`
- **`jug new`**: `jug new my_project`
- **`jug check`**: `jug check hello.jug`
- **`jug typecheck`**: `jug typecheck hello.jug`
- **`jug doctor`**: `jug doctor`

### 5. Short Flag Support (`-h`)
Configured `CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])` on `@click.group`, allowing developers to query help using both standard flags.

---

## Fixed Bugs & Improvements

1. **Truncation Fix for `install` Command**:
   - *Bug*: Click extracts short help from the first sentence ending with a period. In `Install a package or custom bundle (e.g. 'web').`, Click truncated the summary to `Install a package or custom bundle (e.g.`.
   - *Fix*: Added explicit `short_help="Install a package or custom bundle."`.
2. **Click Epilog Formatting Bug**:
   - *Issue*: Standard Click epilog strings are wrapped into flat paragraphs, destroying tabular alignment.
   - *Fix*: Implemented native definition list rendering via `formatter.write_dl(self.examples)`.

---

## Local Development & Setup Commands

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # On Windows
source .venv/bin/activate # On Linux/macOS

# 2. Install package in editable mode with development dependencies
pip install -e .[dev,all]

# 3. Run linting check
ruff check .

# 4. Run test suite with coverage
pytest --cov=jugaadlang

# 5. Test CLI help
python -m jug_cli.main --help
python -m jug_cli.main run --help
```
