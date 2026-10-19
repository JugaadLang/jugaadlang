# JugaadLang Language Specification

JugaadLang is a modern programming language with Roman Hindi keywords, transpiled to Python. It mirrors Python's semantic model and block layout while introducing Hindi equivalents for all core keywords, built-in helper functions, funny diagnostics, and micro-frameworks.

---

## 1. Syntax & Layout

JugaadLang is an indentation-based language. Code blocks are defined by a colon (`:`) followed by a newline and indent.

### 1.1 Indentation
Indentation levels are computed in spaces or tabs (expanded to 8 spaces). Inconsistent indentation (e.g. Mixing spaces and tabs or incorrect dedents) triggers a compiler error.

### 1.2 Comments
JugaadLang supports three comment formats:
* `# comment` — single-line comment (Python style)
* `// comment` — single-line comment (C/JS style), only when `//` is the first token on a line (leading whitespace and a preceding `;` are allowed)
* `/* comment */` — multi-line/block comment (C/JS style)

Because `//` is also the floor-division operator, the two uses are split by position: a line that starts with `//` (after indentation) is a comment, while `//` anywhere inside an expression is floor division. For example, `x = 7 // 2` divides, and `x //= 2` is floor-division assignment. Trailing `//` comments after code are not supported; use `#` for those.

---

## 2. Keywords

The compiler tokenizes the following keywords:

| Keyword | Python Equivalent | Purpose |
| :--- | :--- | :--- |
| `bolo` | `print` | Output statement |
| `poochho` | `input` | Input statement / expression |
| `agar` | `if` | Conditional branch |
| `shayad` | `elif` | Secondary conditional branch |
| `warna` | `else` | Fallback conditional branch |
| `ghumo` | `for` | Definite loop |
| `jabtak` | `while` | Indefinite loop |
| `banao` | `def` | Function definition |
| `wapas` | `return` | Function return |
| `ustad` | `class` | Class definition |
| `khud` | `self` | Instance self-reference |
| `lao` | `import` | Module import |
| `se` | `from` | Sub-module import |
| `sust` | `lazy` (3.15+) | Deferred import |
| `rukja` | `break` | Loop termination |
| `chalte_raho`| `continue` | Loop skip iteration |
| `koshish` | `try` | Exception try block |
| `gadbad` | `except` | Exception catch block |
| `aakhir_me` | `finally` | Exception cleanup block |
| `udao` | `raise` | Exception raise |
| `sahi` | `True` | Boolean true constant |
| `galat` | `False` | Boolean false constant |
| `kuch_nahi` | `None` | Null constant |
| `aur` | `and` | Logical AND operator |
| `ya` | `or` | Logical OR operator |
| `nahi` | `not` | Logical NOT operator |
| `tez` | `async` | Asynchronous modifier |
| `intezaar` | `await` | Asynchronous wait |
| `baanto` | `yield` | Generator yield |
| `theek_hai` | `pass` | Null statement |
| `sabka` | `global` | Global scope variable |
| `chota_funkshan` | `lambda` | Anonymous inline function |
| `mein` | `in` | Membership operator |
| `hai` | `is` | Identity operator |

---

## 3. Data Types

JugaadLang maps natively to Python's dynamic type system:
* `int`: Arbitrary-precision integer (e.g. `10`, `0xFA`, `0b101`)
* `float`: Double-precision floating-point (e.g. `10.5`, `1e-3`)
* `str`: Unicode string literals (e.g. `"Namaste"`, `'Duniya'`, `f"Hi {naam}"`)
* `Template`: Template literal `t"Hi {naam}"` (PEP 750, Python 3.14+; degrades to `str` on older interpreters)
* `bool`: Boolean values (`sahi`, `galat`)
* `null`: Null value (`kuch_nahi`)
* `list`: Resizable array (e.g. `[1, 2, 3]`)
* `tuple`: Immutable array (e.g. `(1, 2, 3)`)
* `dict`: Hash table / map (e.g. `{"naam": "Sumu", "umar": 20}`)
* `set`: Unique set of elements (e.g. `{1, 2, 3}`)

---

## 4. Functions & Classes

### 4.1 Functions (`banao`)
Functions are declared with `banao`. They support default arguments, type annotations, and positional/keyword arguments.
```jugaadlang
banao jod(a: int, b: int = 10) -> int:
    wapas a + b
```

### 4.2 Classes (`ustad`)
Classes are defined with `ustad`. The initialization method must be named `shuru` (which maps to `__init__`). All instance method arguments must specify `khud` (which maps to `self`) as the first argument.
```jugaadlang
ustad Aadmi:
    banao shuru(khud, naam):
        khud.naam = naam
```

---

## 5. built-in Functions

The interpreter automatically injects these interactive functions into the global namespace:
* `chai()`: prints ASCII cup of tea.
* `himmat()`: Prints motivational booster.
* `ghaas_chhoo()`: Prints touch grass advice.
* `bachao()`: Prints emergency help search.
* `fortune()`: Tells a programmer's fortune.
* `jugaad()`: Prints funny debugging tips.
* `roop(t"...")`: Renders a template (`t"..."`) back to text.

---

## 6. Python 3.14 & 3.15 Syntax

JugaadLang tracks CPython's "What's New" releases. Each feature below is transpiled to the native construct when the running interpreter understands it, and to an equivalent older construct otherwise — one source file works on every supported Python (3.10+).

### 6.1 Template strings (`t"..."`, PEP 750)

`t"..."` produces a `string.templatelib.Template` on Python 3.14+ whose `strings` and `interpolations` expose the literal pieces separately. `roop(template)` renders it the way an f-string would.

```jugaadlang
naam = "Asha"
bolo(roop(t"Namaste {naam}, {naam!r:>6}!"))
```

Conversions (`!r`, `!s`, `!a`) and format specs (`{:>6}`, `{:03d}`) work in both `f"..."` and `t"..."`, including nested specs such as `f"{n:0{w}d}"`. Literal braces use `{{` and `}}`. Raw strings (`r"..."`) are not supported yet.

### 6.2 Bracket-less `except` (PEP 758)

```jugaadlang
koshish:
    1 / 0
gadbad ZeroDivisionError, ValueError:
    bolo("pakda gaya")
```

Multiple types with `as` still require brackets: `gadbad (ValueError, TypeError) as e:`.

### 6.3 Unpacking in comprehensions (PEP 798) and literals (PEP 448)

```jugaadlang
jodon = [[1, 2], [3]]
bolo([*l ghumo l mein jodon])
daftar = [{"a": 1}, {"b": 2}]
bolo({**d ghumo d mein daftar})
bolo([*jodon[0], 9])
```

`*` works in list and set comprehensions and generator expressions, `**` in dict comprehensions, and both in list/set/dict/tuple literals. On Python 3.15+ they are emitted natively; older versions rewrite them as an extra loop, so results and evaluation order are identical.

### 6.4 Lazy imports (`sust`, PEP 810)

```jugaadlang
sust lao json
sust se pathlib lao Path
```

`sust` is contextual — it only introduces a `lao` or `se ... lao` statement, so it remains usable as a variable name. On Python 3.15+ the import is bound lazily; on older versions it imports eagerly.

### 6.5 New builtins (PEP 814, PEP 661)

| JugaadLang | Python | Minimum version |
| :--- | :--- | :--- |
| `jamhi_kosh(...)` | `frozendict(...)` | 3.15 |
| `pahredaar` | `sentinel` | 3.15 |

Using either alias below Python 3.15 raises a clear JugaadLang error naming the required version instead of an obscure `NameError`.
