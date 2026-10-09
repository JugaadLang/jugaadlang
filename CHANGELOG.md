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

## [1.2.6] - 2026-10-06

### Added
- Syntax highlighting in try-online compiler editor
- Live contributors strip in hero with GitHub icons
- Implement marshal-based bytecode serialization for AST cache (fixes #124)
- Add online JugaadLang compiler
- Implement AST caching layer
- Improve help output with examples
- Improve CLI help output with command descriptions and examples (fixes #115)
- Add searchable documentation portal
- Add interactive mascot cursor pair
- Add paath (text/string) module

### Changed
- Update version to 1.2.6 in README, __init__.py, pyproject.toml, package.json, and website files
- Bump @typescript-eslint/parser in /vscode_extension
- Bump @types/node in /vscode_extension
- Bump @typescript-eslint/eslint-plugin
- Remove custom cursor animation
- Bump dawidd6/action-homebrew-bump-formula from 8 to 10
- Bump @typescript-eslint/eslint-plugin
- Bump @types/node in /vscode_extension
- Bump eslint from 10.7.0 to 10.9.0 in /vscode_extension
- Bump aiohttp in the uv group across 1 directory

### Fixed
- Full responsive overflow audit - wrap tables in scroll containers, fix long text wrapping in docs, fix jugonline mobile nav and editor panes
- Update button titles for better accessibility and consistency
- Repair hero CTA button sequence and consistent button styles
- Resolve merge conflicts between AST JSON cache and Marshal bytecode cache
- Streamline issue and PR automation workflows by removing unnecessary inputs and ensuring proper event handling
- Update issue and PR automation workflows to enhance comment messages and input handling
- Update PR automation workflow to include input for pull request number and adjust permissions
- Move permissions to the top level in PR automation workflow
- Change pull_request to pull_request_target for automated PR comments
- Show syntax errors in jug check
- Adjust scroll behavior for reduced motion preference
- Improve mobile search focus and touch targets

### Documentation
- Document CLI architecture, technical specifications, and updated commands table

### Tests
- Add unit tests for whatsapp.bhejo and spam
- Add CLI version flag test

### CI/CD
- Update both scoop bucket manifests on release

### Other
- Fix spelling in code examples and comment out unused button link in index.html
- Add changelog workflow and script for automatic CHANGELOG.md updates
- Refactor code structure for improved readability and maintainability
- Refactor CLI tests to use monkeypatch for directory changes
- Refactor code structure for improved readability and maintainability
- Add new commands to CLI test cases
- Refactor token definitions and improve formatting
- Add kadak chai function to stdlib/chai
- Feature #114 Adding Online Compiler to JugaadLang Website is done
- Improve JugaadLang hero section
- Fix typecheck when mypy is not installed

## [1.1.6] - 2026-08-23

### Added
- Enhance shell command execution and add batch scripts for development tasks
- Implement multi-level AST and code object caching (fixes #61)
- Implement event bus architecture (fixes #60)
- Add spotlight search to docs navbar - closes #47
- Add Open Graph and Twitter metadata
- Implement dark mode across website

### Changed
- Reorganize imports and improve code structure across multiple files
- Bump @typescript-eslint/parser in /vscode_extension
- Bump @typescript-eslint/eslint-plugin
- Bump eslint from 8.57.1 to 10.7.0 in /vscode_extension
- Bump dawidd6/action-homebrew-bump-formula from 7 to 8
- Bump actions/setup-node from 6 to 7
- Bump actions/checkout from 6 to 7
- Bump typescript in /vscode_extension
- Bump @types/vscode in /vscode_extension
- Bump eslint from 10.4.1 to 10.6.0 in /vscode_extension
- Bump @typescript-eslint/eslint-plugin
- Bump actions/checkout from 4 to 6
- Bump softprops/action-gh-release from 2 to 3
- Bump actions/setup-node from 4 to 6
- Bump dawidd6/action-homebrew-bump-formula from 4 to 7
- Bump astral-sh/setup-uv from 5 to 7
- Bump @typescript-eslint/parser in /vscode_extension

### Fixed
- Update pip install command to avoid editable mode and improve encoding handling in CLI refactor: remove unused imports in cache and event bus modules test: clean up test files by removing unnecessary imports
- Point issue template question link to correct repo Fixes #83
- Read jug --version from package metadata
- Patch 4 RCE vectors (chalao, kholo, builtins, shell_chalao)
- Implement jug doctor and correct CLI/docs mismatches Add jug doctor diagnostics, fix README command/extension errors, remove unused publish dependency, and exit non-zero on pip failures. Closes #56
- Make Flask an optional web dependency
- Align typescript-eslint deps for npm ci
- Raise LexerError instead of crashing on malformed \u/\x string escapes

### Documentation
- Add Homebrew tap installation instructions to README and landing page

### Tests
- Update assertion for tuple unpacking in for loop to accommodate Python 3.10+
- Add transformer and stdlib test suites
- Add regression tests and fix Windows SQLite cleanup

### CI/CD
- Fix env variable scope for conditionals
- Fix publish job errors and swap to dawidd6 for homebrew bump

### Other
- Add loops and Variables
- Fix issues
- Initial plan
- Add star request to README
- Validate VS Code extension CI fix
- Add Node types to VS Code extension tsconfig
- Fix VS Code engine version mismatch for extension build
- Potential fix for pull request finding
- Remove

## [1.1.5] - 2026-06-14

### Changed
- Fix homebrew formula bump source and tap name

### Other
- Vscode extension v1.1.5
- Update version v1.1.5

## [1.1.4] - 2026-06-13

### Changed
- Remove slow macos-13 intel runner to speed up releases

### Other
- Update new version
- Update version v1.1.3

## [1.1.3] - 2026-06-13

### Changed
- Remove slow macos-13 intel runner to speed up releases

## [1.1.2] - 2026-06-13

### Added
- Compile and upload vscode extension to releases
- Setup multi-platform CI/CD packaging pipelines

### Fixed
- Remove windows arm64 build as x64 runner cannot install arm64 python natively
- Install libarchive-tools for pacman fpm package
- Update ci matrices and scoop config

### Other
- Fromat code

## [1.1.1] - 2026-06-13

### Changed
- Commit changes

### Fixed
- Resolve ruff lint errors in stdlib and fun_builtins

### Documentation
- Add comprehensive git documentation

### Other
- Vs code extension
- Fix code
- Fix ruff lint errors
- Update REPL and VSCode Extension to support new stdlib modules
- Add whatsapp, student, love, and dev stdlib modules
- Add new Fun Built-ins to website Built-in grid section
- Update website with 40+ Fun Built-ins feature card
- Add 40+ fun, productivity, and desi built-in functions
- Example add

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
