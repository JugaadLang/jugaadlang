# JugaadLang CLI Reference

## Usage

```
jug [OPTIONS] COMMAND [ARGS]...
```

## Global Options

| Option | Description |
|---|---|
| `--version` | Show version and exit |
| `--help` | Show help message and exit |

## Commands

### `jug run FILE [ARGS...]`

Run a JugaadLang `.jug` file.

- **File**: Path to a `.jug` file (other extensions work with a warning)
- **ARGS**: Additional arguments passed to the script (accessible via `tantra.argv`)

```bash
jug run main.jug
jug run main.jug arg1 arg2
```

### `jug repl`

Start the interactive JugaadLang REPL (Read-Eval-Print Loop).

- Syntax highlighting via Pygments
- Auto-completion for all keywords
- History persistence (`~/.jugaadlang/repl_history.txt`)
- Double-Enter to execute multi-line blocks

```bash
jug repl
```

### `jug install PACKAGE`

Install a package or custom bundle.

- **PACKAGE**: PyPI package name or bundle alias

| Alias | Installs |
|---|---|
| `web` | flask, requests, httpx, aiohttp |
| `dev` | pytest, pytest-cov, black, mypy, ruff |
| `ml` | numpy, pandas, scikit-learn, matplotlib |
| `*` | Any PyPI package (passthrough) |

```bash
jug install web
jug install flask
```

### `jug remove PACKAGE`

Uninstall a package or bundle.

```bash
jug remove web
```

### `jug update PACKAGE`

Update a package or bundle to the latest version.

```bash
jug update web
```

### `jug search QUERY`

Search for packages in PyPI and JugaadLang standard library.

```bash
jug search chai
jug search requests
```

### `jug new PROJECT_NAME`

Create a new JugaadLang project boilerplate.

```bash
jug new my_project
```

Creates:
```
my_project/
├── main.jug        # Boilerplate .jug file
└── README.md       # Project README
```

### `jug compile FILE -o OUTPUT`

Transpile a JugaadLang `.jug` file to equivalent Python source code.

- `-o, --output FILE`: Write output to a file (otherwise prints to stdout)

```bash
jug compile main.jug -o main.py
jug compile main.jug    # prints Python source to stdout
```

### `jug check FILE`

Validate a JugaadLang file's syntax without executing it.

```bash
jug check main.jug
```

### `jug typecheck FILE`

Type-check a JugaadLang file using mypy (behind the scenes).

```bash
jug typecheck main.jug
```

### `jug doctor`

Diagnose the JugaadLang installation (Python version, core imports, and optional extras).

```bash
jug doctor
```

## Examples

```bash
# Run a file
jug run hello.jug

# Start REPL
jug repl

# Install a bundle
jug install web

# Create a new project
jug new myapp

# Transpile to Python
jug compile myapp/main.jug -o myapp/main.py

# Check syntax
jug check myapp/main.jug
```
