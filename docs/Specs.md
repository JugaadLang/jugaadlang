# JugaadLang Language Specification

JugaadLang is a modern programming language with Roman Hindi keywords, transpiled to Python. It mirrors Python's semantic model and block layout while introducing Hindi equivalents for all core keywords, built-in helper functions, funny diagnostics, and micro-frameworks.

---

## 1. Syntax & Layout

JugaadLang is an indentation-based language. Code blocks are defined by a colon (`:`) followed by a newline and indent.

### 1.1 Indentation

Indentation levels are computed in spaces or tabs (tabs expanded to 8 spaces). Inconsistent indentation (e.g., mixing spaces and tabs or incorrect dedents) triggers a compiler error.

- Standard convention: 4 spaces per indentation level
- Empty lines and comment-only lines don't affect indentation level
- Leading indentation is computed at the start of each logical line

### 1.2 Comments

JugaadLang supports three comment formats:

| Format | Style | Example |
|---|---|---|
| `# comment` | Python-style | `# yeh ek comment hai` |
| `// comment` | C/JS-style | `// yeh bhi comment hai` |
| `/* comment */` | Block comment | `/* multi-line \n comment */` |

### 1.3 Line Termination

Statements are terminated by:
- A newline (most common)
- A semicolon (`;`) for inline separation

### 1.4 String Literals

| Type | Syntax | Example |
|---|---|---|
| Single-quoted | `'...'` | `'Namaste'` |
| Double-quoted | `"..."` | `"Duniya"` |
| Triple single | `'''...'''` | `'''multi\nline'''` |
| Triple double | `"""..."""` | `"""also multi"""` |
| f-strings | `f"..."` | `f"Mera naam {naam} hai"` |

Escape sequences: `\n`, `\t`, `\r`, `\\`, `\'`, `\"`, `\0`, `\a`, `\b`, `\f`, `\v`, `\uXXXX` (Unicode), `\xXX` (hex byte).

### 1.5 Number Literals

| Type | Format | Example |
|---|---|---|
| Decimal integer | `digits` | `42`, `1_000_000` |
| Hexadecimal | `0x...` | `0xFF`, `0xDEAD_BEEF` |
| Octal | `0o...` | `0o755` |
| Binary | `0b...` | `0b1010` |
| Float | `digits.digits` | `3.14`, `1e-3`, `1.5e10` |

### 1.6 Identifiers

Identifiers start with a letter, underscore, or any Unicode character with `isalpha() == True`, followed by alphanumeric or underscore characters. Full Unicode/emoji support.

Valid: `naam`, `_count`, `x1`, `🦄`
Invalid: `1var`, `my-var`, `@name`

---

## 2. Keywords

### 2.1 Complete Keyword Mapping

| JugaadLang | Python | Category |
|---|---|---|
| `bolo` | `print` | I/O |
| `poochho` | `input` | I/O |
| `agar` | `if` | Conditional |
| `shayad` | `elif` | Conditional |
| `warna` | `else` | Conditional |
| `ghumo` | `for` | Loop |
| `jabtak` | `while` | Loop |
| `banao` | `def` | Function |
| `wapas` | `return` | Function |
| `ustad` | `class` | Class |
| `khud` | `self` | Class |
| `lao` | `import` | Import |
| `se` | `from` | Import |
| `jaise` | `as` | Import/alias |
| `rukja` | `break` | Loop control |
| `chalte_raho` | `continue` | Loop control |
| `theek_hai` | `pass` | Placeholder |
| `koshish` | `try` | Exception |
| `gadbad` | `except` | Exception |
| `aakhir_me` | `finally` | Exception |
| `udao` | `raise` | Exception |
| `sahi` | `True` | Boolean |
| `galat` | `False` | Boolean |
| `kuch_nahi` | `None` | Null |
| `aur` | `and` | Logical |
| `ya` | `or` | Logical |
| `nahi` | `not` | Logical |
| `mein` | `in` | Membership |
| `mein_nahi` | `not in` | Membership |
| `hai` | `is` | Identity |
| `nahi_hai` | `is not` | Identity |
| `tez` | `async` | Async |
| `intezaar` | `await` | Async |
| `baanto` | `yield` | Generator |
| `chota_funkshan` | `lambda` | Lambda |
| `sabka` | `global` | Scope |
| `gair_local` | `nonlocal` | Scope |
| `pakka` | `assert` | Assertion |
| `hatao` | `del` | Deletion |
| `ke_saath` | `with` | Context mgr |
| `agar_match` | `match` | Pattern match |
| `kaand` | `case` | Pattern match |
| `bulawo` | (call sugar) | Function call |

### 2.2 Additional Keywords (English fallbacks)

The following English keywords are also recognized as alternatives:
- `del` (same as `hatao`)
- `nonlocal` (same as `gair_local`)
- `with` (same as `ke_saath`)
- `as` (same as `jaise`)
- `assert` (same as `pakka`)

---

## 3. Data Types

JugaadLang maps natively to Python's dynamic type system:

| Type | Description | Examples |
|---|---|---|
| `int` | Arbitrary-precision integer | `42`, `-1`, `0xFF`, `0b1010` |
| `float` | Double-precision floating-point | `3.14`, `1e-3`, `-0.5` |
| `str` | Unicode string | `"Namaste"`, `'Duniya'`, `f"Hi {naam}"` |
| `bool` | Boolean | `sahi`, `galat` |
| `NoneType` | Null | `kuch_nahi` |
| `list` | Resizable array | `[1, 2, 3]` |
| `tuple` | Immutable array | `(1, 2, 3)` |
| `dict` | Hash table / map | `{"naam": "Sumu"}` |
| `set` | Unique elements | `{1, 2, 3}` |
| `function` | First-class function | `banao f(): ...` |
| `class` | User-defined type | `ustad Aadmi:` |

---

## 4. Variables & Assignment

```jugaadlang
# Simple assignment
x = 10
naam = "Sumangal"

# Augmented assignment
x += 5
x -= 3
x *= 2
x /= 4
x //= 2
x %= 3
x **= 2

# Type-annotated assignment
x: int = 10
naam: str = "Sumu"

# Multiple assignment
a, b = 1, 2

# Walrus operator (assignment expression)
agar (n := lambaee(list)) > 0:
    bolo(n)
```

---

## 5. Control Flow

### 5.1 Conditionals

```jugaadlang
agar x > 0:
    bolo("Positive")
shayad x == 0:
    bolo("Zero")
warna:
    bolo("Negative")
```

### 5.2 Ternary Expression

```jugaadlang
status = "bada" agar x > 10 warna "chota"
```

### 5.3 For Loops

```jugaadlang
# Basic
ghumo i mein range(5):
    bolo(i)

# With tuple unpacking
ghumo naam, umar mein zip(names, ages):
    bolo(naam + " hai " + str(umar) + " saal ka")

# Async for
tez ghumo x mein async_generator():
    process(x)

# For-else
ghumo i mein range(5):
    agar i == 3:
        rukja
warna:
    bolo("Loop completed without break")
```

### 5.4 While Loops

```jugaadlang
jabtak count > 0:
    bolo(count)
    count -= 1
    agar count == 3:
        rukja

# While-else
jabtak x > 0:
    x -= 1
warna:
    bolo("Loop ended naturally")
```

### 5.5 Break and Continue

```jugaadlang
ghumo i mein range(10):
    agar i % 2 == 0:
        chalte_raho  # skip even numbers
    agar i > 7:
        rukja  # stop at 8
    bolo(i)
```

### 5.6 Pass

```jugaadlang
banao yet_to_be_implemented():
    theek_hai  # placeholder
```

---

## 6. Functions

### 6.1 Function Definition

```jugaadlang
banao add(a, b):
    wapas a + b

banao greet(naam, greeting="Namaste"):
    bolo(greeting + " " + naam)

banao calculate(a: int, b: int = 10) -> int:
    wapas (a * b) // 2
```

### 6.2 Lambda (Anonymous Functions)

```jugaadlang
square = chota_funkshan x: x * x
add = chota_funkshan a, b: a + b
```

### 6.3 Generator Functions

```jugaadlang
banao count_up_to(n):
    count = 1
    jabtak count <= n:
        baanto count
        count += 1
```

### 6.4 Call Sugar

```jugaadlang
bulawo my_function(arg1, arg2)  # same as my_function(arg1, arg2)
```

---

## 7. Classes & OOP

### 7.1 Class Definition

```jugaadlang
ustad Animal:
    banao shuru(khud, naam):
        khud.naam = naam

    banao speak(khud):
        bolo(khud.naam + " makes a sound")

    banao __str__(khud):
        wapas "Animal: " + khud.naam
```

### 7.2 Inheritance

```jugaadlang
ustad Dog(Animal):
    banao speak(khud):
        bolo(khud.naam + " says Woof!")
```

### 7.3 Decorators

```jugaadlang
@classmethod
banao create_default(khud):
    wapas khud("Unknown")

@staticmethod
banao info():
    wapas "This is the Animal class"
```

---

## 8. Exception Handling

### 8.1 Try-Except-Finally

```jugaadlang
koshish:
    result = risky_operation()
    bolo(result)
gadbad ValueError jaise e:
    bolo("Value error aaya: " + str(e))
gadbad TypeError:
    bolo("Type mismatch!")
gadbad:
    bolo("Kuch aur gadbad hui")
warna:
    bolo("Koi error nahi aaya!")
aakhir_me:
    bolo("Ye to chalega hi")
```

### 8.2 Raise

```jugaadlang
udao ValueError("Kuch gadbad hai")
udao Exception("Original cause") se ValueError("Wrapper")
```

---

## 9. Imports

```jugaadlang
# Simple import
lao math

# With alias
lao numpy jaise np

# From-import
se math lao sqrt, sin

# From-import with alias
se math lao sqrt jaise square_root

# From-import all
se math lao *
```

---

## 10. Pattern Matching (Python 3.10+)

```jugaadlang
agar_match value:
    kaand 0:
        bolo("Zero")
    kaand 1 | 2 | 3:
        bolo("Small number")
    kaand int():
        bolo("Some other integer")
    kaand [x, y]:
        bolo("A list of " + str(x) + " and " + str(y))
    kaand {"naam": naam}:
        bolo("Name found: " + naam)
    kaand _:
        bolo("Kuch aur")
```

---

## 11. Async/Await

```jugaadlang
lao asyncio

tez banao fetch_data():
    bolo("Fetching...")
    intezaar asyncio.sleep(1)
    wapas "Data mil gaya!"

tez banao main():
    result = intezaar fetch_data()
    bolo(result)

asyncio.run(main())
```

---

## 12. Context Managers

```jugaadlang
# Using 'with' (or 'ke_saath')
ke_saath open("file.txt", "w") as f:
    f.likho("JugaadLang content")

# Using 'with'
with open("file.txt") as f:
    content = f.padho()

# Async context manager
tez banao main():
    tez ke_saath AsyncConnection(host) jaise conn:
        data = intezaar conn.fetch()
```

`tez ke_saath` only works inside a `tez banao` function, the same way as in Python.

---

## 13. Comprehensions

```jugaadlang
# List comprehension
squares = [x * x ghumo x mein range(10)]
even_squares = [x * x ghumo x mein range(10) agar x % 2 == 0]

# Dictionary comprehension
square_map = {x: x * x ghumo x mein range(5)}

# Set comprehension
unique_squares = {x * x ghumo x mein [1, 2, 2, 3, 3, 3]}

# Generator expression
sum_of_squares = yog(x * x ghumo x mein range(100))
```

---

## 14. I/O

```jugaadlang
# Output
bolo("Hello World")
bolo(42)
bolo(f"Value: {x}")

# Input
poochho naam  # shorthand: name = input()
user_input = poochho("Apna naam likho: ")  # function form: input("prompt")
```

---

## 15. Built-in Functions

### 15.1 Standard Built-in Mappings

35+ Hindi wrappers map to Python's built-in functions. See `docs/keywords.md` for complete list.

### 15.2 JugaadLang-Specific Built-ins

Custom funny/utility functions injected at runtime (see `docs/keywords.md` or the `madad()` help menu).

---

## 16. Error System

Errors are displayed with humorous Hindi messages instead of standard Python tracebacks. See `docs/api.md` → `jugaadlang/errors/messages.py` for details.

---

## 17. Grammar (EBNF)

The complete formal grammar is defined in `docs/grammar.ebnf`.

Key aspects:
- Indentation-based blocks (handled by lexer via INDENT/DEDENT tokens)
- Expressions use precedence climbing (Pratt parsing)
- Full pattern matching grammar for Python 3.10+ compatibility
