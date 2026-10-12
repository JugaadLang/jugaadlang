# Variables and data types

Assign with `=`. Names are case-sensitive, and types are determined at runtime. Prefer descriptive names such as `kul_daam` instead of `x`.

## Values

| Kind | Example | Notes |
| --- | --- | --- |
| Integer | `umar = 21` | Whole numbers |
| Float | `daam = 12.5` | Decimal numbers |
| String | `naam = "Asha"` | Unicode text |
| Boolean | `taiyaar = sahi` | `sahi` / `galat` map to Python booleans |
| Empty value | `result = kuch_nahi` | Maps to Python `None` |
| List | `ank = [10, 20]` | Ordered, mutable collection |
| Tuple | `bindu = (2, 3)` | Ordered, immutable collection |
| Dictionary | `chai = {"daam": 15}` | Key/value pairs |
| Set | `alag = {1, 2, 3}` | Unique values |

## Work with collections

Indexes begin at zero. List methods and dictionary access follow Python's model.

```jugaadlang
phal = ["aam", "seb"]
phal.append("kela")
bolo(phal[0])
bolo(len(phal))
chai = {"daam": 15, "cup": 2}
bolo(chai["daam"] * chai["cup"])
```

Expected output:

```text
aam
3
30
```

## Strings and templates

`f"..."` formats values in place, including the `!r`/`!s`/`!a` conversions and width specifiers Python supports. `t"..."` builds a template object (PEP 750, Python 3.14+); `roop` renders any template back to text.

```jugaadlang
naam = "Asha"
daam = 12.5
bolo(f"Namaste {naam}, daam = {daam:.2f}")
bolo(f"{naam!r:>6}")
chitthi = t"Namaste {naam}!"
bolo(roop(chitthi))
```

Expected output:

```text
Namaste Asha, daam = 12.50
'Asha'
Namaste Asha!
```

Use templates when the pieces matter as data — SQL, HTML, or log messages are built from `template.strings` and `template.interpolations` instead of one concatenated string. `bolo` on a template prints the object itself, so pass it through `roop` when you want text. On Python 3.13 and older `t"..."` compiles to a plain f-string, and `roop` returns it unchanged.

## Unpack collections

`*` splices list or set elements and `**` merges dictionary keys. The same marks work directly inside comprehensions, so nested containers flatten in one expression.

```jugaadlang
jodon = [[1, 2], [3]]
sab = [*l ghumo l mein jodon]
bolo(sab)
bolo([*sab, 4])
daftar = [{"a": 1}, {"b": 2}]
bolo({**d ghumo d mein daftar})
```

Expected output:

```text
[1, 2, 3]
[1, 2, 3, 4]
{'a': 1, 'b': 2}
```

## Convert explicitly

Input and file contents are text. Use `int`, `float`, or `str` when converting between text and numbers. Invalid numeric text raises `ValueError`.

```jugaadlang
daam = int("25")
bolo(daam + 5)
bolo("Total: " + str(daam))
```

Expected output:

```text
30
Total: 25
```

## Mutation and sharing

Assigning a list to another variable does not copy it. Both names refer to the same list. Use `list(original)` for a shallow copy when you need a separate outer collection.

Continue with [operators](operators.html), [functions and scope](functions.html), or [handling conversion errors](debugging.html).
