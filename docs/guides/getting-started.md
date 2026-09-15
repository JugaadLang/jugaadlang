# Getting started

Code karo Hindi mein. JugaadLang uses Roman Hindi keywords, indentation-based blocks, and Python's runtime. This guide takes you from an empty file to a running program.

## Before you begin

Install Python 3.10 or newer and JugaadLang using the [installation guide](installation.html). Check your terminal with `jug --version`.

## Your first program

Create a UTF-8 file named `namaste.jug`:

```jugaadlang
naam = "Duniya"
bolo("Namaste, " + naam + "!")
```

Expected output:

```text
Namaste, Duniya!
```

Run it from the folder containing the file:

```bash
jug run namaste.jug
```

`bolo` prints a value. `naam` stores a string; you do not need a declaration keyword. A `.jug` file is a text file containing JugaadLang source.

## Add a decision

Blocks start with a colon and use indentation. Use four spaces consistently.

```jugaadlang
chai = 2
agar chai > 0:
    bolo("Chai taiyaar!")
warna:
    bolo("Chai banao.")
```

Expected output:

```text
Chai taiyaar!
```

## Choose your next step

- **New to programming?** Follow [variables](variables.html), [control flow](control-flow.html), then the [chai bill tutorial](tutorials.html).
- **Coming from Python?** Read [syntax](syntax.html) and the [keyword mapping](keywords.html).
- **Building something?** Explore [functions and modules](functions.html) and the [standard library](stdlib.html).
- **Contributing?** Start with the [contributor guide](contributing.html) and [architecture](architecture.html).

## Try the interactive shell

Run `jug repl` to experiment without creating a file. Press Enter twice to submit a multiline block. Use Ctrl+C to interrupt input and Ctrl+D to leave the shell.

For command options, see the [CLI reference](cli.html). If a command fails, start with [debugging](debugging.html).
