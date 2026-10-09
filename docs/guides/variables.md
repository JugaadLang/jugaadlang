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
