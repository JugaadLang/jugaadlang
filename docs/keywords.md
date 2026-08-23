# JugaadLang Keywords Reference

## Keyword Mapping

Every Python keyword has a Hindi (Roman Hindi) equivalent. All keywords are case-sensitive and lowercase.

### Control Flow

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `agar` | `if` | If | `agar x > 5: bolo("bada hai")` |
| `shayad` | `elif` | Maybe/Perhaps | `shayad x == 5: bolo("barabar")` |
| `warna` | `else` | Otherwise | `warna: bolo("chota hai")` |
| `ghumo` | `for` | Roam/Iterate | `ghumo i mein range(5):` |
| `jabtak` | `while` | As long as | `jabtak x > 0:` |
| `rukja` | `break` | Stop! | `rukja` |
| `chalte_raho` | `continue` | Keep going | `chalte_raho` |
| `theek_hai` | `pass` | It's fine | `theek_hai` |

### Functions & Classes

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `banao` | `def` | Create/Make | `banao add(a, b): wapas a + b` |
| `wapas` | `return` | Return/Go back | `wapas result` |
| `ustad` | `class` | Master/Teacher | `ustad Car:` |
| `khud` | `self` | Self | `khud.naam = naam` |
| `shuru` | `__init__` | Start | Method name for constructor |
| `chota_funkshan` | `lambda` | Little function | `chota_funkshan x: x + 1` |
| `baanto` | `yield` | Distribute | `baanto value` |

### Exception Handling

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `koshish` | `try` | Try/Attempt | `koshish:` |
| `gadbad` | `except` | Problem | `gadbad ValueError:` |
| `aakhir_me` | `finally` | In the end | `aakhir_me:` |
| `udao` | `raise` | Throw | `udao ValueError("kuch gadbad hai")` |

### Imports

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `lao` | `import` | Bring | `lao math` |
| `se` | `from` | From | `se math lao sqrt` |
| `jaise` | `as` | Like | `lao numpy jaise np` |

### Boolean & Operators

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `sahi` | `True` | Correct | `agar sahi:` |
| `galat` | `False` | Wrong | `jabtak galat:` |
| `kuch_nahi` | `None` | Nothing | `x = kuch_nahi` |
| `aur` | `and` | And | `agar x > 0 aur x < 10:` |
| `ya` | `or` | Or | `agar x == 0 ya x == 1:` |
| `nahi` | `not` | Not | `agar nahi x:` |
| `mein` | `in` | In | `ghumo x mein list:` |
| `mein_nahi` | `not in` | Not in | `agar 5 mein_nahi list:` |
| `hai` | `is` | Is | `agar x hai kuch_nahi:` |
| `nahi_hai` | `is not` | Is not | `agar x nahi_hai y:` |

### Async

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `tez` | `async` | Fast | `tez banao fetch():` |
| `intezaar` | `await` | Wait | `intezaar fetch()` |

### Declarations

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `sabka` | `global` | Everyone's | `sabka x` |
| `gair_local` | `nonlocal` | Non-local | `gair_local x` |
| `pakka` | `assert` | Guaranteed | `pakka x > 0, "positive hona chahiye"` |
| `hatao` | `del` | Remove | `hatao x` |
| `ke_saath` | `with` | With | `ke_saath open("file") as f:` |

### Pattern Matching (Python 3.10+)

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `agar_match` | `match` | If matches | `agar_match value:` |
| `kaand` | `case` | Case/situation | `kaand sahi:` |

### I/O Keywords

| Keyword | Python Equivalent | Hindi Meaning | Example |
|---|---|---|---|
| `bolo` | `print` | Speak | `bolo("Hello")` |
| `poochho` | `input` | Ask | `poochho naam` |
| `bulawo` | (call sugar) | Call | `bulawo func()` |

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
| `gun_hatao(o, a)` | `delattr(o, a)` | Remove attribute |
| `kosh()` | `dict()` | Dictionary |
| `bhag_shesh(a, b)` | `divmod(a, b)` | Quotient-remainder |
| `ginti(x)` | `enumerate(x)` | Counting |
| `chhano(f, x)` | `filter(f, x)` | Filter |
| `gun_lao(o, a)` | `getattr(o, a)` | Get attribute |
| `gun_hai(o, a)` | `hasattr(o, a)` | Has attribute |
| `madad()` | `help()` | Help |
| `pehchan(x)` | `id(x)` | Identity |
| `purnank(x)` | `int(x)` | Integer |
| `prakar_hai(x, t)` | `isinstance(x, t)` | Is of type |
| `subclass_hai(c, b)` | `issubclass(c, b)` | Is subclass |
| `lambaee(x)` | `len(x)` | Length |
| `suchi(x)` | `list(x)` | List |
| `adhiktam(a, b)` | `max(a, b)` | Maximum |
| `nyuntam(a, b)` | `min(a, b)` | Minimum |
| `agla(x)` | `next(x)` | Next |
| `vastu()` | `object()` | Object |
| `ghat(x, y)` | `pow(x, y)` | Power |
| `ulta(x)` | `reversed(x)` | Reversed |
| `gun_badlo(o, a, v)` | `setattr(o, a, v)` | Change attribute |
| `tukda(a, b, c)` | `slice(a, b, c)` | Slice |
| `kramwar(x)` | `sorted(x)` | Sequential |
| `shabd(x)` | `str(x)` | Word/string |
| `yog(x)` | `sum(x)` | Sum |
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
| `kismat(start, end)` | Random number |
| `sikka()` | Coin flip (Head/Tail) |
| `saaf()` | Clear terminal |
| `ruk(seconds)` | Sleep/pause |
| `bahar()` | Exit program |
| `namaste()` | Welcome banner |
| `debug(var)` | Debug info |
| `version()` | Show version |
| `madad()` | Full help menu 