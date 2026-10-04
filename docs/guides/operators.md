# Operators and expressions

Expressions combine values and produce a result. Use parentheses when they make an expression easier to read.

## Arithmetic and comparison

| Operators | Meaning |
| --- | --- |
| `+`, `-`, `*`, `/` | Addition, subtraction, multiplication, division |
| `%`, `**` | Remainder and exponentiation |
| `==`, `!=` | Equal and not equal |
| `<`, `<=`, `>`, `>=` | Ordered comparison |
| `=`, `+=`, `-=` | Assignment and updating a variable |

```jugaadlang
bolo(2 + 3 * 4)
bolo((2 + 3) * 4)
bolo(7 % 3)
bolo(2 ** 3)
```

Expected output:

```text
14
20
1
8
```

Multiplication binds more tightly than addition. Parentheses change the order. `/` produces a floating-point result for integer operands.

## Logic

Use `aur` (and), `ya` (or), and `nahi` (not). `aur` and `ya` short-circuit, so the second expression is only evaluated when needed.

```jugaadlang
umar = 20
ticket = sahi
bolo(umar >= 18 aur ticket)
bolo(nahi ticket)
bolo("aam" mein ["seb", "aam"])
```

Expected output:

```text
True
False
True
```

Printed boolean values use Python's `True` and `False` spelling. Use `mein` for membership, `hai` for identity, and `==` for comparing values. The keyword reference also lists `mein_nahi` and `nahi_hai`.

## Avoid ambiguous intent

Use `==` in a condition, not assignment `=`. Do not compare strings and numbers without conversion. See [variables](variables.html) for conversions and [control flow](control-flow.html) for conditions in programs.
