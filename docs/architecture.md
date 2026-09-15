# JugaadLang Architecture

## Overview

JugaadLang is a Hindi-keyword programming language that transforms its own syntax tree into Python AST (Abstract Syntax Tree), compiles it to bytecode, and executes it on the Python VM. Parsing, transformation, and runtime helpers have costs; this is not a zero-overhead guarantee. The runtime caches generated Python source to reuse it on subsequent executions.

### Pipeline

```
Source (.jug)
    │
    ▼
┌─────────────┐
│   Lexer     │  Tokenizes source into tokens (jugaadlang/lexer/lexer.py)
└──────┬──────┘
       │ tokens
       ▼
┌─────────────┐
│   Parser    │  Recursive-descent parser → JugaadLang AST (jugaadlang/parser/parser.py)
└──────┬──────┘
       │ JL AST
       ▼
┌────────────────────┐
│  Transformer       │  Converts JL AST → Python AST (jugaadlang/transformer/to_python.py)
└──────┬─────────────┘
       │ Python AST
       ▼
┌─────────────┐
│  compile()  │  Python's built-in: Python AST → bytecode
└──────┬──────┘
       │ bytecode
       ▼
┌─────────────┐
│  exec()     │  Python VM executes bytecode
└─────────────┘
```

## Directory Structure

```
jugaadlang/
├── jug_cli/                  # Command-line interface
│   ├── main.py               # Click-based CLI entry point
│   └── __init__.py
│
├── jugaadlang/               # Core language implementation
│   ├── ast_nodes/
│   │   ├── nodes.py          # JugaadLang AST node definitions (dataclasses)
│   │   └── __init__.py
│   ├── errors/
│   │   ├── messages.py       # Funny Hindi error formatting
│   │   └── __init__.py
│   ├── lexer/
│   │   ├── lexer.py          # Source tokenizer with indentation tracking
│   │   ├── tokens.py         # TokenType enum and keyword mapping
│   │   └── __init__.py
│   ├── parser/
│   │   ├── parser.py         # Recursive-descent parser
│   │   └── __init__.py
│   ├── runtime/
│   │   ├── interpreter.py    # Execution harness, built-in functions
│   │   └── __init__.py
│   ├── transformer/
│   │   ├── to_python.py      # JL AST → Python AST visitor
│   │   └── __init__.py
│   ├── stdlib/               # Standard library modules (importable via `lao`)
│   │   ├── ganit.py          # Mathematics
│   │   ├── web.py            # HTTP client + JugaadWeb framework
│   │   ├── faili.py          # File system
│   │   ├── json.py           # JSON parser
│   │   ├── samay.py          # Date/time
│   │   ├── tantra.py         # System/environment
│   │   ├── crypto.py         # Hashing & encoding
│   │   ├── database.py       # JugaadORM (SQLite ORM)
│   │   ├── chai.py           # Tea-themed utility
│   │   ├── jokes.py          # Programmer jokes
│   │   ├── motivation.py     # Motivational quotes
│   │   ├── fortune.py        # Fortune telling
│   │   ├── memes.py          # ASCII art memes
│   │   ├── catfacts.py       # Cat facts
│   │   └── __init__.py
│   ├── REPL/
│   │   ├── repl.py           # Interactive REPL with syntax highlighting
│   │   └── __init__.py
│   ├── package_manager/
│   │   ├── manager.py        # Package installation/search/removal
│   │   └── __init__.py
│   ├── __init__.py           # Version info
│   └── pyproject.toml        # Project metadata & dependencies
│
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_runtime.py
│   ├── test_errors.py
│   └── __init__.py
│
├── docs/
│   ├── spec.md               # Language specification
│   ├── architecture.md       # This file
│   ├── grammar.ebnf          # Formal EBNF grammar
│   ├── keywords.md           # Keyword reference
│   ├── stdlib.md             # Standard library reference
│   ├── cli.md                # CLI command reference
│   └── api.md                # Internal API reference
│
├── examples/                 # Example .jug programs
├── scratch/                  # Scratch/test files
├── website/                  # Landing page HTML/CSS
├── vscode_extension/         # VS Code syntax highlighting extension
└── docker/                   # Docker deployment files
```

## Core Components

### 1. Lexer (`jugaadlang/lexer/`)

The lexer tokenizes raw source code into a stream of `Token` objects. Key features:

- **Indentation tracking**: Implements Python-style INDENT/DEDENT tokens using a stack-based approach
- **Multi-line comments**: Supports `#`, `//`, and `/* */` comment styles
- **String literals**: Single, double, triple-quoted, and f-strings
- **Number literals**: Decimal, hex (`0x`), octal (`0o`), binary (`0b`), floats with exponents
- **Unicode identifiers**: Full Unicode + emoji support in identifiers

### 2. Parser (`jugaadlang/parser/`)

A recursive-descent parser with precedence climbing for expressions. Produces a JugaadLang-specific AST (defined in `jugaadlang/ast_nodes/nodes.py`).

- Supports all Python control flow: `if`/`elif`/`else`, `for`, `while`, `try`/`except`/`finally`
- Full pattern matching (`agar_match`/`kaand`) translating to Python 3.10+ `match`/`case`
- Comprehensions (list, dict, set, generator)
- Async/await, generator yield
- Decorators, type annotations
- Walrus operator (`:=`)

### 3. Transformer (`jugaadlang/transformer/to_python.py`)

The transformer walks the JugaadLang AST and emits corresponding Python AST nodes. This is where keywords are mapped:

- `bolo` → `print`
- `agar` → `if`
- `shuru` (method name) → `__init__`
- `khud` → `self`
- All Hindi built-in names → Python built-in names

### 4. Interpreter (`jugaadlang/runtime/interpreter.py`)

The interpreter orchestrates the full pipeline:

1. Lex → Parse → Transform → Compile → Execute
2. Maintains a persistent global namespace (shared across REPL sessions)
3. Injects built-in functions (`chai`, `fortune`, `jugaad`, etc.) and built-in name mappings (`maan`→`abs`, `lambaee`→`len`, etc.)
4. Error handling with funny Hindi diagnostic messages

### 5. Error System (`jugaadlang/errors/messages.py`)

Errors are caught at the runtime level and re-formatted with humorous Hindi messages:

| Error Type | Title |
|---|---|
| `SyntaxError` | `🤦 Bhai kya likh diya?` |
| `NameError` | `🕵️ Variable '...' dhundte dhundte thak gaya.` |
| `ZeroDivisionError` | `💀 Zero se divide?` |
| `TypeError` | `🤔 Type mismatch ho gaya.` |
| `IndexError` | `📭 List mein itna nahi hai!` |
| `KeyError` | `🔑 Key gayab hai!` |
| `AttributeError` | `🚫 Attribute mila hi nahi.` |

### 6. CLI (`jug_cli/main.py`)

Built with [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/).

Commands: `run`, `repl`, `install`, `remove`, `update`, `search`, `new`, `compile`, `check`, `typecheck`, `doctor`.

### 7. REPL (`jugaadlang/repl/repl.py`)

Interactive shell using `prompt_toolkit` with:
- Syntax highlighting (via custom Pygments lexer)
- Auto-completion for all keywords and built-ins
- Auto-suggest from history
- Multi-line block input (double-Enter to execute)

### 8. Package Manager (`jugaadlang/package_manager/manager.py`)

Wraps pip with JugaadLang-specific bundle aliases:

| Alias | Packages |
|---|---|
| `web` | flask, requests, httpx, aiohttp |
| `dev` | pytest, pytest-cov, black, mypy, ruff |
| `ml` | numpy, pandas, scikit-learn, matplotlib |
| `*` | Any PyPI package passthrough |

## Translation Examples

| JugaadLang | Python (after transpilation) |
|---|---|
| `bolo("Namaste")` | `print("Namaste")` |
| `agar x > 5:` | `if x > 5:` |
| `ghumo i mein range(10):` | `for i in range(10):` |
| `banao jod(a, b): wapas a + b` | `def jod(a, b): return a + b` |
| `ustad Animal:` | `class Animal:` |
| `banao shuru(khud, naam):` | `def __init__(self, naam):` |
| `koshish: ... gadbad: ...` | `try: ... except: ...` |
| `tez banao fetch():` | `async def fetch():` |
| `intezaar result` | `await result` |
| `poochho naam` | `naam = input()` |
| `lao ganit` | `import ganit` |
| `se math lao sqrt` | `from math import sqrt` |
