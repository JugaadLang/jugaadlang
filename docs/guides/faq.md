# Frequently asked questions

## Do I need to know Hindi?

No. Keywords use Roman Hindi, and the [keyword reference](keywords.html) pairs them with Python equivalents. The guides explain each keyword as it is introduced.

## Do I need Python installed?

Yes. JugaadLang requires Python 3.10 or newer and executes compiled code through Python. Follow [installation](installation.html) to keep it in a virtual environment.

## Why does a boolean print as True or False?

`sahi` and `galat` map to Python boolean values. Printing them uses Python's spelling. `kuch_nahi` similarly maps to `None`.

## Why is jug not found after installation?

The command may belong to a different environment. Activate the environment where you installed the package and run `python -m pip show jugaadlang`. On Windows you can invoke `.venv\Scripts\jug.exe` directly.

## Can I use Python libraries?

Installed Python modules can be imported with `lao` or `se ... lao ...`. Install packages into the same environment as JugaadLang. See [functions and modules](functions.html) and the [CLI reference](cli.html).

## Is this a browser playground?

This documentation explains how to run programs locally. Code blocks are examples, not an in-browser interpreter. Use `jug run` or `jug repl` to execute them.

## Where should I report a bug?

Open an [issue](https://github.com/JugaadLang/jugaadlang/issues) with your JugaadLang and Python versions, the smallest reproducing program, expected behavior, and actual output. For security reports, follow the repository's [security policy](https://github.com/JugaadLang/jugaadlang/blob/main/SECURITY.md).

## How can I improve these docs?

Use the “Edit this page” link on any article. The portal is generated from Markdown; the [contributor guide](contributing.html) explains how to build and check it locally.
