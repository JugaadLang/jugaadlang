# Changelog

All notable changes to **JugaadLang** will be documented in this file.

## [Unreleased]

### Added
- **Test Coverage**: `tests/test_transformer.py` — 120 parametrized tests covering all keyword mappings, built-in name mappings, operators, comprehensions, pattern matching, async/await, classes, and all statement types.
- **Test Coverage**: `tests/test_stdlib.py` — 47 tests covering all 18 standard library modules (ganit, samay, crypto, faili, json, tantra, chai, dev, fortune, motivation, love, student, jokes, memes, database, web, crypto_module, catfacts, whatsapp).
- **CI/CD**: OS matrix expanded to `[ubuntu-latest, windows-latest, macos-latest]` in `.github/workflows/ci.yml`.
- **Coverage Enforcement**: `[tool.coverage.report] fail_under = 60` added to `pyproject.toml`.

### Audit
- **Full Repository Audit**: `JUGAADLANG_AUDIT_REPORT.md` — 78 findings across 8 domains (architecture, security, performance, testing, documentation, contribution opportunities).

### Security
- **Restrict `__builtins__`**: Replaced unrestricted `__builtins__` in the interpreter globals with an explicit allowlist (`_SAFE_BUILTINS`). Dangerous functions (`exec`, `eval`, `compile`, `open`, `__import__`) are no longer accessible from JugaadLang code. Closes issue #53 (vector 3).
- **Remove `chalao` (exec)**: Removed `"chalao": exec` from the interpreter globals and the `"chalao": "exec"` mapping from the transformer name map. JugaadLang users can no longer execute arbitrary Python code via `chalao()`. Closes issue #53 (vector 1).
- **Remove `kholo` (open)**: Removed `"kholo": open` from the interpreter globals and the `"kholo": "open"` mapping from the transformer name map. JugaadLang users can no longer open arbitrary files via `kholo()`. Closes issue #53 (vector 2).
- **Hardened `tantra.shell_chalao`**: Changed from `subprocess.run(command, shell=True)` to `shlex.split(command)` with `shell=False`, preventing shell injection attacks. Closes issue #53 (vector 4).
## [1.1.0] - 2026-06-12

### Added
- **Native Built-in Functions**:
  - `kismat(start, end)`: Random number generation.
  - `sikka()`: Coin flip returning "Head" or "Tail".
  - `saaf()`: Cross-platform terminal clear.
  - `ruk(seconds)`: Pause execution.
  - `bahar()`: Exit the program safely.
  - `namaste()`: Displays a beautiful JugaadLang ASCII welcome banner.
  - `debug(variable)`: Specialized built-in function to print types and representation.
  - `version()`: Prints the active JugaadLang version.
  - `madad()`: A massive custom Help Menu covering Data Types, System I/O, Math, and Desi Funny functions (replaces standard Python help).
- **GitHub Infrastructure**:
  - `dependabot.yml` for automated updates across pip, npm, Docker, and Actions.
  - Custom automated desi welcome messages for issues and PRs.
  - PR Autolabeler based on file routing.
  - YAML Issue Forms for structured bug reports and feature requests.

### Fixed
- **VS Code Extension**: Resolved a strict peer dependency conflict between `@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin` in `package.json` locking versions to `^8.61.0`.
- **Version Skew**: Fixed an issue where the hardcoded `__version__` string inside `jugaadlang/__init__.py` would fall out of sync with `pyproject.toml`.
- **Release Automation**: Updated `update_version.sh` to correctly bump `jugaadlang/__init__.py` during future release cuts.

## [1.0.3] - 2026-06-11
### Fixed
- General bug fixes and patches to stabilize the `1.0` release series.

## [1.0.2] - 2026-06-10
### Fixed
- Minor patches and hotfixes following the `1.0.1` pre-release.

## [1.0.1] - 2026-06-10
### Added
- Pre-release build introducing minor enhancements to core components.

## [1.0.0] - 2026-06-09

### Added
- **Core Syntax & Compiler**:
  - Implemented 1:1 direct compilation from JugaadLang AST to native Python AST.
  - Added **Structural Pattern Matching** (`agar_match` / `kaand`) syntax translating to Python 3.10+ pattern matching block structures.
  - Implemented full block parser, async/await constructs, slicing, lambda expressions (`chota_funkshan`), and list/dict/set comprehensions.
  - Added Hindi keyword `jaise` (along with `as`) to define aliases in imports, exceptions (`gadbad ... jaise e`), and pattern matches.
  - Added Hindi keyword mappings for all remaining Python keywords: `pakka` (for `assert`), `hatao` (for `del`), `gair_local` (for `nonlocal`), and `ke_saath` (for `with`).
  
- **Standard Mapped Built-ins**:
  - Registered 35+ Roman-Hindi wrappers for standard Python built-ins (e.g., `prakar` for `type`, `lambaee` for `len`, `suchi` for `list`, `kosh` for `dict`, `maan` for `abs`, `subclass_hai` for `issubclass`).
  - Added 8 new interactive funny built-in functions:
    - `nazar()`: Blocks compiler bad vibes and bugs.
    - `ashirwad()`:Elder blessings for guaranteed successful runtime runs.
    - `dhanya_waad()`: Polite desi gratitude output.
    - `bhagwan_bhala_kare()`: Divine intervention prayer request for compilers.
    - `paisa_wasool()`: Value verification for free open-source software.
    - `bas_kar_bhai()`: Prompt to shutdown laptop and sleep.
    - `chilla_mat()`: Reminder to calm down and relax while debugging.
    - `kundli()`: Code horoscopic analysis highlighting loop blocking transits.

- **Standard Library Features**:
  - **JugaadORM (`database`)**: SQLite-backed ORM supporting database table migrations, MRO-aware class resolving, and transaction rollbacks.
  - **JugaadWeb (`web`)**: Micro REST framework routing via `@web.agar_route` decorator, Flask query/body parsing, and auto JSON serialization.
  - Core modules: `ganit` (maths), `faili` (files), `json`, `samay` (datetime), `tantra` (system), and `crypto`.

- **CLI & Packaging**:
  - Added static typechecker command `jug typecheck` running `mypy` behind the scenes.
  - Implemented package manager locking generating `jug.lock`.
  - Added script arguments pass-through to environment under `sys.argv`/`tantra.argv`.
  - Added root `run.sh` script to streamline testing, packing, and local editable installs.

- **VS Code Extension**:
  - Compiled and packaged extension files into a standalone `.vsix` installer.
  - Included TextMate grammar for highlighting, TS extension for hover docstrings, and a custom circular JL App Logo.

- **Landing Website**:
  - Implemented interactive code tabs highlighting loops, OOP, pattern matching, and JugaadWeb servers.
  - Added copyable terminals with clipboards.
  - Fixed stats grid layouts and preserved space-indentation styling.

### Fixed
- **CI/CD Pipeline**: Corrected setup-python GitHub Action path to `actions/setup-python@v5` and added Python 3.14 coverage.
- **Indentation collapse**: Patched website CSS by applying `white-space: pre` to avoid browser space-collapsing, restoring Python-like indentation formatting.
