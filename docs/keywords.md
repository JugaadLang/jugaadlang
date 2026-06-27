# JugaadLang Keywords Reference

JugaadLang supports **dual keyword systems**: the original Hindi (Roman Hindi) keywords AND standard Python English keywords. You can use either interchangeably in the same file.

## Keyword Mapping

### Control Flow

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `if` | `agar` | `if` | `if x > 5: print("bada hai")` |
| `elif` | `shayad` | `elif` | `elif x == 5: print("barabar")` |
| `else` | `warna` | `else` | `else: print("chota hai")` |
| `for` | `ghumo` | `for` | `for i in range(5):` |
| `while` | `jabtak` | `while` | `while x > 0:` |
| `break` | `rukja` | `break` | `break` |
| `continue` | `chalte_raho` | `continue` | `continue` |
| `pass` | `theek_hai` | `pass` | `pass` |

### Functions & Classes

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `def` | `banao` | `def` | `def add(a, b): return a + b` |
| `return` | `wapas` | `return` | `return result` |
| `class` | `ustad` | `class` | `class Car:` |
| `self` | `khud` | `self` | `self.name = name` |
| *(n/a)* | `shuru` | `__init__` | Constructor method name |
| `lambda` | `chota_funkshan` | `lambda` | `lambda x: x + 1` |
| `yield` | `baanto` | `yield` | `yield value` |

### Exception Handling

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `try` | `koshish` | `try` | `try:` |
| `except` | `gadbad` | `except` | `except ValueError:` |
| `finally` | `aakhir_me` | `finally` | `finally:` |
| `raise` | `udao` | `raise` | `raise ValueError("kuch gadbad hai")` |

### Imports

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `import` | `lao` | `import` | `import math` |
| `from` | `se` | `from` | `from math import sqrt` |
| `as` | `jaise` | `as` | `import numpy as np` |

### Boolean & Operators

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `True` | `sahi` | `True` | `if True:` |
| `False` | `galat` | `False` | `while False:` |
| `None` | `kuch_nahi` | `None` | `x = None` |
| `and` | `aur` | `and` | `if x > 0 and x < 10:` |
| `or` | `ya` | `or` | `if x == 0 or x == 1:` |
| `not` | `nahi` | `not` | `if not x:` |
| `in` | `mein` | `in` | `for x in list:` |
| `not in` | `mein_nahi` | `not in` | `if 5 not in list:` |
| `is` | `hai` | `is` | `if x is None:` |
| `is not` | `nahi_hai` | `is not` | `if x is not y:` |

### Async

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `async` | `tez` | `async` | `async def fetch():` |
| `await` | `intezaar` | `await` | `await fetch()` |

### Declarations

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `global` | `sabka` | `global` | `global x` |
| `nonlocal` | `gair_local` | `nonlocal` | `nonlocal x` |
| `assert` | `pakka` | `assert` | `assert x > 0, "positive hona chahiye"` |
| `del` | `hatao` | `del` | `del x` |
| `with` | `ke_saath` | `with` | `with open("file") as f:` |

### Pattern Matching (Python 3.10+)

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `match` | `agar_match` | `match` | `match value:` |
| `case` | `kaand` | `case` | `case True:` |

### I/O Keywords

| English | Hindi | Python Equivalent | Example |
|---|---|---|---|
| `print` | `bolo` | `print` | `print("Hello")` or `bolo("Hello")` |
| `input` | `poochho` | `input` | `name = input("Name: ")` or `poochho naam` |
| `call` | `bulawo` | (call sugar) | `call func()` |

## Built-in Functions (Hindi → Python Mapping)

These JugaadLang built-in function names map directly to Python's built-in functions:

| JugaadLang | Python | Meaning |
|---|---|---|
| `maan(x)` | `abs(x)` | Value |
| `sab(x)` | `all(x)` | All |
| `koi_bhi(x)` | `any(x)` | Any |
| `binary(x)` | `bin(x)` | Binary |
| `satyata(x)` | `bool(x)` | Truth value |
| `bulaane_yogya(x)` | `callable(x)` | Callable |
| `akshar(x)` | `chr(x)` | Character |
| `avdhi(s, e)` | `range(s, e)` | Range of numbers |
| `dashamlav(x)` | `float(x)` | Decimal/float number |
| `gun_hatao(o, a)` | `delattr(o, a)` | Remove attribute |
| `gol(x, n)` | `round(x, n)` | Round number |
| `jama_huya(x)` | `frozenset(x)` | Immutable set |
| `jod(s1, s2)` | `zip(s1, s2)` | Zip sequences |
| `kosh()` | `dict()` | Dictionary |
| `kram(c)` | `ord(c)` | Unicode code point |
| `bhag_shesh(a, b)` | `divmod(a, b)` | Quotient-remainder |
| `ginti(x)` | `enumerate(x)` | Counting |
| `chalao(x)` | `exec(x)` | Execute |
| `chhano(f, x)` | `filter(f, x)` | Filter |
| `gun_lao(o, a)` | `getattr(o, a)` | Get attribute |
| `gun_hai(o, a)` | `hasattr(o, a)` | Has attribute |
| `madad()` | `help()` | Help |
| `pehchan(x)` | `id(x)` | Identity |
| `purnank(x)` | `int(x)` | Integer |
| `prakar_hai(x, t)` | `isinstance(x, t)` | Is of type |
| `subclass_hai(c, b)` | `issubclass(c, b)` | Is subclass |
| `lambaee(x)` | `len(x)` | Length |
| `manchitra(f, s)` | `map(f, s)` | Map function to sequence |
| `pratinidh(x)` | `repr(x)` | Representation |
| `purnank(x)` | `int(x)` | Integer |
| `samuchay(x)` | `set(x)` | Set |
| `suchi(x)` | `list(x)` | List |
| `suchi_batao(x)` | `dir(x)` | Show attribute list |
| `yadrichhik()` | `random.random()` | Random float 0-1 |
| `adhiktam(a, b)` | `max(a, b)` | Maximum |
| `nyuntam(a, b)` | `min(a, b)` | Minimum |
| `agla(x)` | `next(x)` | Next |
| `vastu()` | `object()` | Object |
| `kholo(f)` | `open(f)` | Open |
| `ghat(x, y)` | `pow(x, y)` | Power |
| `ulta(x)` | `reversed(x)` | Reversed |
| `gun_badlo(o, a, v)` | `setattr(o, a, v)` | Change attribute |
| `tukda(a, b, c)` | `slice(a, b, c)` | Slice |
| `kramwar(x)` | `sorted(x)` | Sequential |
| `shabd(x)` | `str(x)` | Word/string |
| `uper()` | `super()` | Superclass |
| `yog(x)` | `sum(x)` | Sum |
| `yugm(x)` | `tuple(x)` | Tuple |
| `prakar(x)` | `type(x)` | Type |

## JugaadLang Built-in Fun Functions

These are custom functions injected at runtime (not in Python stdlib):

| Function | Description |
|---|---|
| `chai()` | "Chai pi lo" message |
| `himmat()` | Hidden feature motivation |
| `ghaas_chhoo()` | Touch grass reminder |
| `bachao()` | StackOverflow search |
| `fortune()` | Random programmer fortune |
| `jugaad()` | Random debugging tip |
| `nazar()` | Block bad vibes/bugs |
| `ashirwad()` | Elder blessings |
| `dhanya_waad()` | Gratitude message |
| `bhagwan_bhala_kare()` | Prayer for errors |
| `paisa_wasool()` | Free OSS reminder |
| `bas_kar_bhai()` | Sleep reminder |
| `chilla_mat()` | Calm down reminder |
| `kundli()` | Code horoscope |
| `kismat(start, end)` | Random integer |
| `pasand(list)` | Random choice from list |
| `sikka()` | Coin flip (Head/Tail) |
| `yadrichhik()` | Random float 0-1 |
| `saaf()` | Clear terminal |
| `ruk(seconds)` | Sleep/pause |
| `bahar()` | Exit program |
| `namaste()` | Welcome banner |
| `debug(var)` | Debug info |
| `version()` | Show version |
| `madad()` | Full help menu 