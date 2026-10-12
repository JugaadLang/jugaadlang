# Error handling and debugging

JugaadLang reports errors with Hindi diagnostics. Read the exception type, filename, and line information along with the friendly message.

## Catch an expected failure

`koshish`, `gadbad`, and `aakhir_me` correspond to try, except, and finally. Catch a specific exception you know how to handle.

```jugaadlang
koshish:
    ank = int("chai")
gadbad ValueError:
    bolo("Number likho.")
aakhir_me:
    bolo("Jaanch poori.")
```

Expected output:

```text
Number likho.
Jaanch poori.
```

Use `udao ValueError("message")` to reject an invalid value in your own code. A `wapas` inside a function can return a successful result; an exception communicates a failure the caller must handle.

## Catch several exceptions at once

List the types after `gadbad` without brackets (PEP 758 style). Brackets still work: `gadbad (ValueError, TypeError):`.

```jugaadlang
koshish:
    ank = int("do")
gadbad ValueError, TypeError:
    bolo("Sahi sankhya chahiye.")
```

Expected output:

```text
Sahi sankhya chahiye.
```

Add `as naam` to keep the exception object. Multiple types with `as` need brackets: `gadbad (ValueError, TypeError) as e:`.

## Common problems

| Error | Check |
| --- | --- |
| Syntax or indentation error | Missing colon, unmatched bracket, or inconsistent spaces |
| `NameError` | Spelling and whether the name was assigned before use |
| `TypeError` | Text versus numbers; argument count and types |
| `IndexError` | List size and zero-based indexes |
| `KeyError` | Whether the dictionary contains the key |
| `ModuleNotFoundError` | Import spelling and the active Python environment |
| `ZeroDivisionError` | Validate the denominator before dividing |

## A debugging workflow

1. Reduce the program to the smallest input that still fails.
2. Run `jug check main.jug` to check syntax without executing it.
3. Print intermediate values with `bolo`.
4. Run `jug compile main.jug -o main.py` to inspect the generated Python source.
5. Use `jug typecheck main.jug` for optional static checks; this command uses mypy and may require installing it.

Compilation and syntax checks do not prove runtime correctness. Exercise normal inputs, boundary values, and invalid inputs. See the [CLI reference](cli.html) and [coding guidelines](practices.html).
