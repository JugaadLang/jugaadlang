# JugaadLang Internal API Reference

## Package: `jugaadlang`

### `jugaadlang/__init__.py`

```python
from jugaadlang import __version__
__author__ = "JugaadLang Community"
__license__ = "MIT"
```

---

## Module: `jugaadlang.lexer`

### `jugaadlang.lexer.tokens`

**`class TokenType(Enum)`**

All token types used by the lexer. Categories:
- **Literals**: `INT`, `FLOAT`, `STRING`, `FSTRING`
- **Keywords**: `BOLO`, `POOCHHO`, `AGAR`, `SHAYAD`, `WARNA`, `GHUMO`, `JABTAK`, `BANAO`, `WAPAS`, `USTAD`, `KHUD`, `LAO`, `SE`, `RUKJA`, `CHALTE_RAHO`, `KOSHISH`, `GADBAD`, `AAKHIR_ME`, `UDAO`, `SAHI`, `GALAT`, `KUCH_NAHI`, `AUR`, `YA`, `NAHI`, `TEZ`, `INTEZAAR`, `BAANTO`, `THEEK_HAI`, `SABKA`, `CHOTA_FUNKSHAN`, `MEIN`, `MEIN_NAHI`, `HAI`, `NAHI_HAI`, `BULAWO`, `DEL`, `NONLOCAL`, `WITH`, `AS`, `ASSERT`, `AGAR_MATCH`, `KAAND`
- **Operators**: `PLUS`, `MINUS`, `STAR`, `SLASH`, `DOUBLESLASH`, `PERCENT`, `DOUBLESTAR`, `EQ`, `NEQ`, `LT`, `GT`, `LTE`, `GTE`, `ASSIGN`, `PLUS_ASSIGN`, `MINUS_ASSIGN`, `STAR_ASSIGN`, `SLASH_ASSIGN`, `PERCENT_ASSIGN`, `DOUBLESTAR_ASSIGN`, `DOUBLESLASH_ASSIGN`, `ARROW`, `WALRUS`, `AT`, `AT_ASSIGN`, `TILDE`, `AMP`, `PIPE`, `CARET`, `LSHIFT`, `RSHIFT`, `AMP_ASSIGN`, `PIPE_ASSIGN`, `CARET_ASSIGN`, `LSHIFT_ASSIGN`, `RSHIFT_ASSIGN`
- **Delimiters**: `LPAREN`, `RPAREN`, `LBRACKET`, `RBRACKET`, `LBRACE`, `RBRACE`, `COMMA`, `DOT`, `COLON`, `SEMICOLON`, `ELLIPSIS`
- **Layout**: `NEWLINE`, `INDENT`, `DEDENT`
- **Special**: `COMMENT`, `EOF`

**`KEYWORDS: dict[str, TokenType]`**

Maps keyword strings to their `TokenType`. Includes bilingual support:
- `"hatao"` → `TokenType.DEL` (alternative for `del`)
- `"gair_local"` → `TokenType.NONLOCAL` (alternative for `nonlocal`)
- `"ke_saath"` → `TokenType.WITH` (alternative for `with`)
- `"jaise"` → `TokenType.AS` (alternative for `as`)
- `"pakka"` → `TokenType.ASSERT` (alternative for `assert`)

**`@dataclass class Token`**

| Field | Type | Description |
|---|---|---|
| `type` | `TokenType` | The token type |
| `value` | `str` | The token's string value |
| `line` | `int` | Source line number |
| `col` | `int` | Source column number |

Methods: `is_keyword() -> bool`

### `jugaadlang.lexer.lexer`

**`class Lexer`**

| Method | Returns | Description |
|---|---|---|
| `Lexer(source, filename)` | — | Initialize with source string and optional filename |
| `.tokenize()` | `list[Token]` | Tokenize the entire source |

Internal: Uses INDENT/DEDENT stack for indentation-based block detection. Supports `#`, `//`, `/* */` comments, all string types (single, double, triple, f-strings), and all number formats.

---

## Module: `jugaadlang.ast_nodes`

### `jugaadlang.ast_nodes.nodes`

All AST nodes are `@dataclass` inheriting from `ASTNode` (base), `Stmt`, or `Expr`.

**Statements:**
`Module`, `FunctionDef`, `ClassDef`, `Return`, `Delete`, `Assign`, `AugAssign`, `AnnAssign`, `For`, `While`, `If`, `With`, `Raise`, `Try`, `Assert`, `Import`, `ImportFrom`, `Global`, `Nonlocal`, `ExprStmt`, `Pass`, `Break`, `Continue`, `PoochhoStmt`, `Match`

**Expressions:**
`BoolOp`, `BinOp`, `UnaryOp`, `Lambda`, `IfExp`, `Dict`, `Set`, `ListComp`, `SetComp`, `DictComp`, `GeneratorExp`, `Await`, `Yield`, `YieldFrom`, `Compare`, `Call`, `FormattedValue`, `JoinedStr`, `Constant`, `Attribute`, `Subscript`, `Starred`, `Name`, `List`, `Tuple`, `Slice`

**Helper Nodes:**
`arg`, `arguments`, `keyword`, `alias`, `withitem`, `ExceptHandler`, `comprehension`

**Pattern Matching Nodes:**
`Match`, `match_case`, `MatchValue`, `MatchSingleton`, `MatchAs`, `MatchOr`, `MatchSequence`, `MatchMapping`, `MatchClass`

Each node includes `line: int` and `col: int` fields for error reporting.

---

## Module: `jugaadlang.parser`

### `jugaadlang.parser.parser`

**`class Parser`**

| Method | Returns | Description |
|---|---|---|
| `Parser(tokens, filename, source)` | — | Initialize with token list |
| `.parse()` | `Module` | Parse the entire token stream into an AST |

Internal recursive-descent parser with these parse methods:
- `.parse_statement()` — Top-level statement dispatcher
- `.parse_expression()` — Expression entry (precedence climbing)
- `.parse_block()` — Indented block or inline statement
- `.parse_function_def(is_async)` — `banao`/`tez banao`
- `.parse_class_def()` — `ustad`
- `.parse_if()` / `.parse_elif()` — `agar`/`shayad`/`warna`
- `.parse_for(is_async)` — `ghumo`/`tez ghumo`
- `.parse_while()` — `jabtak`
- `.parse_match()` — `agar_match`/`kaand`
- `.parse_try()` — `koshish`/`gadbad`/`aakhir_me`
- `.parse_lambda()` — `chota_funkshan`
- `.parse_import()` / `.parse_import_from()` — `lao`/`se ... lao`

---

## Module: `jugaadlang.transformer`

### `jugaadlang.transformer.to_python`

**`class JugaadToPythonTransformer`**

| Method | Returns | Description |
|---|---|---|
| `JugaadToPythonTransformer(filename)` | — | Initialize transformer |
| `.transform(node: Module)` | `ast.Module` | Transform entire JL AST to Python AST |
| `.visit(node, ctx)` | `ast.AST` | Dispatch visitor by node type |

Each `visit_{NodeType}` method handles a specific JL AST node and returns the corresponding Python AST node.

Key translations:
- `shuru` → `__init__`
- `khud` → `self`
- `bolo` → `print`
- `poochho` → `input`
- All Hindi built-in names → Python built-in names (mapped in `visit_Name`)

---

## Module: `jugaadlang.runtime`

### `jugaadlang.runtime.interpreter`

**`class JugaadInterpreter`**

| Method | Returns | Description |
|---|---|---|
| `JugaadInterpreter(filename)` | — | Init with persistent global namespace |
| `.run(source)` | `None` | Execute JugaadLang source (exec mode) |
| `.run_expression(source)` | `Any` | Evaluate expression (eval mode) or execute statements |

The interpreter maintains a `globals` dict that persists across calls (important for REPL).

**Built-in Functions** (injected at interpreter init):

| Group | Functions |
|---|---|
| **Standard I/O** | `bolo` → `print`, `poochho` → `input` |
| **Random** | `kismat(start, end)`, `sikka()` |
| **System** | `saaf()`, `ruk(seconds)`, `bahar()` |
| **Fun** | `namaste()`, `chai()`, `himmat()`, `ghaas_chhoo()`, `bachao()`, `fortune()`, `jugaad()`, `nazar()`, `ashirwad()`, `dhanya_waad()`, `bhagwan_bhala_kare()`, `paisa_wasool()`, `bas_kar_bhai()`, `chilla_mat()`, `kundli()` |
| **Dev** | `debug(var)`, `version()`, `madad()` |
| **Built-in Mappings** | `maan` → `abs`, `sab` → `all`, `lambaee` → `len`, etc. |

---

## Module: `jugaadlang.errors`

### `jugaadlang.errors.messages`

**`class JugaadError(Exception)`** — Base class for compiler/runtime errors.
**`class JugaadSyntaxError(JugaadError)`** — Syntax errors.
**`class JugaadRuntimeError(JugaadError)`** — Runtime errors.
**`class JugaadNameError(JugaadRuntimeError)`** — Name errors.
**`class JugaadTypeError(JugaadRuntimeError)`** — Type errors.
**`class JugaadZeroDivisionError(JugaadRuntimeError)`** — Division by zero.

**Functions:**

| Function | Description |
|---|---|
| `format_error(exc, source, filename)` | Format any exception with funny Hindi message |
| `format_syntax_error(msg, line, col, source_line, filename)` | Format syntax errors with caret highlighting |

**`FUNNY_ERRORS` dict** — Maps Python exception type names to humorous Hindi titles and descriptions.

---

## Module: `jugaadlang.repl`

### `jugaadlang.repl.repl`

**`class JugaadREPL`**

| Method | Description |
|---|---|
| `JugaadREPL()` | Init with persistent interpreter and history |
| `.start()` | Launch interactive REPL loop |

Uses `prompt_toolkit.PromptSession` with:
- `PygmentsLexer(JugaadPygmentsLexer)` — Syntax highlighting
- `WordCompleter(KEYWORDS_LIST)` — Auto-completion
- `FileHistory` — Persistent history
- `AutoSuggestFromHistory()` — Suggestion

---

## Module: `jugaadlang.package_manager`

### `jugaadlang.package_manager.manager`

**`class JugaadPackageManager`**

All methods are static:

| Method | Description |
|---|---|
| `JugaadPackageManager.install(package)` | Install package/bundle via pip |
| `JugaadPackageManager.remove(package)` | Uninstall package |
| `JugaadPackageManager.update(package)` | Upgrade package |
| `JugaadPackageManager.search(query)` | Search PyPI and stdlib |

**`PACKAGE_MAP`** — Bundle definitions mapping short aliases to pip packages.
