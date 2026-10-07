# Control flow

Control flow chooses which statements run and how often. Every indented block follows a colon.

## Make a decision

```jugaadlang
ank = 75
agar ank >= 90:
    bolo("Bahut badhiya")
shayad ank >= 60:
    bolo("Pass")
warna:
    bolo("Phir koshish karo")
```

Expected output:

```text
Pass
```

Only the first matching branch runs. `shayad` and `warna` are optional.

## Repeat over a sequence

`ghumo` iterates through a collection. `range(1, 4)` includes 1 and excludes 4.

```jugaadlang
ghumo i mein range(1, 4):
    bolo(i)
```

Expected output:

```text
1
2
3
```

## Repeat while a condition holds

Update the condition inside a `jabtak` loop so it can finish.

```jugaadlang
baaki = 3
jabtak baaki > 0:
    bolo(baaki)
    baaki -= 1
```

Expected output:

```text
3
2
1
```

## Skip or stop

`chalte_raho` skips the rest of the current iteration. `rukja` exits the innermost loop. `theek_hai` is a placeholder statement for a block you will fill in later.

```jugaadlang
ghumo i mein range(5):
    agar i == 1:
        chalte_raho
    agar i == 3:
        rukja
    bolo(i)
```

Expected output:

```text
0
2
```

Next, move repeated logic into [functions](functions.html) or build the [chai bill tutorial](tutorials.html). For exception control flow, see [debugging](debugging.html).
