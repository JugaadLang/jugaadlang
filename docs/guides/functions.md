# Functions and modules

Functions give a name to reusable behavior. Modules group related behavior behind an import.

## Define and call a function

Use `banao` to define a function and `wapas` to return a value. Arguments may have defaults.

```jugaadlang
banao kul_daam(cup, daam=15):
    wapas cup * daam

bolo(kul_daam(3))
bolo(kul_daam(2, 20))
```

Expected output:

```text
45
40
```

Assignments inside a function normally create local variables. Pass data in and return results instead of relying on global state. Use `sabka` only when you intentionally need to assign a global name.

## Import a module

Use `lao` for a module and `se ... lao ...` for a named import. JugaadLang resolves its standard library names and can import installed Python modules.

```jugaadlang
lao ganit
se math lao sqrt
bolo(ganit.square(5))
bolo(sqrt(16))
```

Expected output:

```text
25
4.0
```

See the [standard library](stdlib.html) for available modules. Third-party Python packages must be installed in the environment used by `jug`. For module resolution details, consult the [architecture](architecture.html); do not assume a `.jug` file is automatically importable as a Python module.

## Classes

Use `ustad` to define a class. The constructor is `shuru`, and `khud` refers to the instance.

```jugaadlang
ustad Chai:
    banao shuru(khud, daam):
        khud.daam = daam

    banao bill(khud, cup):
        wapas khud.daam * cup

chai = Chai(12)
bolo(chai.bill(3))
```

Expected output:

```text
36
```

The [syntax reference](syntax.html) and [keyword reference](keywords.html) cover annotations, generators, and asynchronous keywords. Start with ordinary functions before introducing those features.
