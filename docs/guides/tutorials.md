# Tutorials and learning paths

Choose a path, then practice by changing a working example.

## Beginner path

1. [Install JugaadLang](installation.html) and run [your first program](index.html).
2. Learn [values and collections](variables.html).
3. Combine [expressions](operators.html) with [conditions and loops](control-flow.html).
4. Extract repeated logic into [functions](functions.html).
5. Complete the chai bill program below and add [error handling](debugging.html).

## Coming from Python

Read the [keyword mapping](keywords.html), [syntax reference](syntax.html), and [standard library](stdlib.html). JugaadLang transpiles to Python, but its parser and available built-ins define which source constructs work; it is not a promise that every Python program runs unchanged.

## Build a chai bill

Create `chai_bill.jug`. The program adds the cost of two orders and applies a discount when the subtotal reaches 100.

```jugaadlang
banao bill(orders, daam):
    subtotal = 0
    ghumo cup mein orders:
        subtotal += cup * daam
    agar subtotal >= 100:
        wapas subtotal - 10
    wapas subtotal

orders = [2, 3]
bolo("Total: " + str(bill(orders, 20)))
```

Run `jug run chai_bill.jug`.

Expected output:

```text
Total: 90
```

The five cups cost 100 before the discount. Try changing the orders to `[1, 2]`: the total should become 60, with no discount.

## Extend it

- Reject negative cup counts with `udao ValueError(...)`.
- Store named prices in a dictionary.
- Write the receipt to a disposable file with the `faili` module.
- Add tests for an empty order, a small order, and the exact discount boundary.

## Contributor path

Read [contributing](contributing.html), trace a statement through the [architecture](architecture.html), then explore the [internal API](api.html). Add a small regression test before changing language behavior.
