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
- **Literals**: `INT`, `FLOAT`, `STRING`, `FSTRING`, `TSTRING`
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

Internal: Uses INDENT/DEDENT stack for indentation-based block detection. Supports `#`, line-start `//`, `/* */` comments, all string types (single, double, triple, f-strings, t-strings), and all number formats. `//` inside an expression is the floor-division operator. A raw `r"..."` prefix raises a clear lexer error. Prefixes are letters that end at a quote, so identifiers such as `test`, `tf`, and `f` are unaffected.

---

## Module: `jugaadlang.ast_nodes`

### `jugaadlang.ast_nodes.nodes`

All AST nodes are `@dataclass` inheriting from `ASTNode` (base), `Stmt`, or `Expr`.

**Statements:**
`Module`, `FunctionDef`, `ClassDef`, `Return`, `Delete`, `Assign`, `AugAssign`, `AnnAssign`, `For`, `While`, `If`, `With`, `Raise`, `Try`, `Assert`, `Import`, `ImportFrom`, `Global`, `Nonlocal`, `ExprStmt`, `Pass`, `Break`, `Continue`, `PoochhoStmt`, `Match`

**Expressions:**
`BoolOp`, `BinOp`, `UnaryOp`, `Lambda`, `IfExp`, `Dict`, `Set`, `ListComp`, `SetComp`, `DictComp`, `GeneratorExp`, `Await`, `Yield`, `YieldFrom`, `Compare`, `Call`, `FormattedValue`, `JoinedStr`, `TemplateStr`, `Interpolation`, `Constant`, `Attribute`, `Subscript`, `Starred`, `Name`, `List`, `Tuple`, `Slice`

`TemplateStr`/`Interpolation` model PEP 750 t-strings (`Interpolation` carries `value`, `str`, `conversion`, `format_spec`). `DictComp` carries `unpack: bool` for `{**d ghumo ...}`; `Import`/`ImportFrom` carry `is_lazy: bool` for `sust lao ...`.

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
- `.parse_import()` / `.parse_import_from()` — `lao`/`se ... lao` (also `sust`-prefixed lazy imports)
- `.parse_fstring()` / `.parse_tstring()` — `f"..."` and `t"..."` interpolation, including `!r`/`!s`/`!a` conversions and format specs

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

Version-gated emission (`PY314` / `PY315` constants) — newer syntax is written only when the running interpreter supports it, otherwise an equivalent older construct is emitted:

| JugaadLang feature | Python 3.14+ / 3.15+ | Older Python |
|---|---|---|
| `t"..."` (PEP 750) | `ast.TemplateStr` / `ast.Interpolation` | `ast.JoinedStr` / `ast.FormattedValue` |
| `sust lao x` (PEP 810) | `ast.Import(is_lazy=1)` | plain `ast.Import` |
| `[*x ghumo ...]` (PEP 798) | `ast.Starred` in comprehension | extra lowering loop |
| `jamhi_kosh` / `pahredaar` | `frozendict` / `sentinel` | `JugaadError` naming Python 3.15 |

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
| **Templates** | `roop(template)` → render `t"..."` to `str` |
| **Built-in Mappings** | `maan` → `abs`, `sab` → `all`, `lambaee` → `len`, etc. |

Optional builtins from newer CPython releases (`frozendict`, `sentinel`, `__lazy_import__`) are added to the allowlist only when the running interpreter provides them.

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
