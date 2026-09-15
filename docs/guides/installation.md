# Installation and setup

JugaadLang requires Python 3.10 or newer. Its `jug` command runs programs, opens the REPL, and provides development tools.

## Create an environment

Check `python --version`. On Windows, use `py` if `python` is unavailable; on macOS or Linux, use `python3` if needed.

```bash
python -m venv .venv
```

Activate it in your terminal:

| Terminal | Command |
| --- | --- |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS / Linux shell | `source .venv/bin/activate` |

If PowerShell prevents activation, you can use `.venv\Scripts\python.exe` and `.venv\Scripts\jug.exe` directly instead of changing system policy.

## Install the language

```bash
python -m pip install jugaadlang
jug --version
jug doctor
```

The version command prints the installed release. `jug doctor` checks the local environment. Follow [getting started](index.html) to run your first file.

## Optional web dependencies

For the optional web integrations:

```bash
python -m pip install "jugaadlang[web]"
```

The [standard library reference](stdlib.html) explains the HTTP client and web framework APIs.

## Upgrade

```bash
python -m pip install --upgrade jugaadlang
```

Use the same Python environment for installation and execution. If `jug` is not found, activate the environment and check `python -m pip show jugaadlang`.

## Editor setup

Save source files with the `.jug` extension. The [VS Code extension](https://marketplace.visualstudio.com/items?itemName=jugaadlang.jugaadlang) provides language support. A plain text editor and terminal also work.

For an editable checkout, tests, and pull requests, see [contributing](contributing.html).
