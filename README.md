<div align="center">
  <h1>JugaadLang 🇮🇳</h1> 
  <h2> Please🙏 star ⭐ the repo 🤝❤</h2>
   
<p> Code karo Hindi mein, Duniya hila do! 🚀</p>
<p align="center" >
  <img src="https://github.com/JugaadLang/jugaadlang/blob/main/website/assets/icon.png" width="180" alt="JugaadLang Logo">
</p>

JugaadLang is a modern, beginner-friendly, fun programming language inspired by Python, designed for Indian developers. It replaces Python's core keywords with English-spelled Hindi (Roman Hindi) terms and features custom funny error diagnostic outputs, a built-in package manager, and standard libraries.

JugaadLang transpiles directly to native Python AST, meaning it runs with zero runtime performance overhead and provides full compatibility with the entire Python ecosystem.

<a href="https://www.producthunt.com/products/jugaadlang-code-karo-hindi-mein?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-jugaadlang-code-karo-hindi-mein" target="_blank" rel="noopener noreferrer"><img alt="JugaadLang — Code karo Hindi mein  - Code karo Hindi mein, Duniya hila do 🇮🇳 | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1168029&amp;theme=light&amp;t=1781108995735"></a>




---
[![JugaadLang CI](https://github.com/JugaadLang/jugaadlang/actions/workflows/ci.yml/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/ci.yml)
[![JugaadLang Release](https://github.com/JugaadLang/jugaadlang/actions/workflows/release.yml/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/release.yml)
[![CodeQL](https://github.com/JugaadLang/jugaadlang/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/github-code-scanning/codeql)

[![VS Code Extension](https://github.com/JugaadLang/jugaadlang/actions/workflows/vscode-extension.yml/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/vscode-extension.yml)
[![PR Create Automate Message](https://github.com/JugaadLang/jugaadlang/actions/workflows/pr-create-automate-message.yml/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/pr-create-automate-message.yml)
[![Pull Request Labeler](https://github.com/JugaadLang/jugaadlang/actions/workflows/autolabler.yml/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/autolabler.yml)
[![Issue Create Automate Message](https://github.com/JugaadLang/jugaadlang/actions/workflows/issue-create-automate-message.yml/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/issue-create-automate-message.yml)
[![Dependency Graph](https://github.com/JugaadLang/jugaadlang/actions/workflows/dependabot/update-graph/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/dependabot/update-graph)
[![Dependabot Updates](https://github.com/JugaadLang/jugaadlang/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/JugaadLang/jugaadlang/actions/workflows/dependabot/dependabot-updates)

![Windows](https://img.shields.io/badge/Windows-Supported-blue)
![Linux](https://img.shields.io/badge/Linux-Supported-green)
![macOS](https://img.shields.io/badge/macOS-Supported-lightgrey)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![Open Source](https://img.shields.io/badge/Open%20Source-❤️-red)

</div>

## Table of Contents
1. [Core Philosophy](#core-philosophy)
2. [Installation](#installation)
3. [Language Keywords Reference](#language-keywords-reference)
4. [Example Usage](#example-usage)
5. [Built-in Fun Functions](#built-in-fun-functions)
6. [Ecosystem & Tooling](#ecosystem--tooling)
   - [CLI Runner](#cli-runner)
   - [Interactive REPL](#interactive-repl)
   - [Package Manager](#package-manager)
   - [VS Code Extension](#vs-code-extension)
7. [Standard Library (Stdlib)](#standard-library-stdlib)
8. [Funny Error System](#funny-error-system)
9. [Automated Testing](#automated-testing)

---

## Core Philosophy
1. **Python simplicity:** Clear, indentation-based block syntax.
2. **Hindi-English keywords:** Express logic in the language you think in.
3. **Humorous diagnostics:** Error messages that make you laugh, not crash.
4. **Zero-overhead transpilation:** Compiles to Python bytecode and executes in the native Python VM.

---

## Installation

Get started with JugaadLang in just a few minutes.

## Requirements

Before installing JugaadLang, make sure you have:

* Python 3.10 or later
* pip package manager

Check your Python version:

```bash
python --version
```

or

```bash
python3 --version
```

---

# 🪟 Windows

### Install

```powershell
pip install jugaadlang
```

### Verify Installation

```powershell
jug --version
```

Expected output:

```text
JugaadLang v1.0.2 🇮🇳

```

### Run Your First Program

Create a file named `hello.jug`

```jugaad
bolo("Namaste Duniya 🚀")
```

Run it:

```powershell
jug run hello.jug
```

Output:

```text
Namaste Duniya 🚀
```

---

# 🐧 Linux

### Install

**Option A: Using Homebrew (Recommended)**

```bash
brew tap jugaadlang/tap
brew install jugaadlang
```

**Option B: Using pip**

```bash
pip3 install jugaadlang
```

### Verify Installation

```bash
jug --version
```

### Run

```bash
jug run hello.jug
```

---

# 🍎 macOS

### Install

**Option A: Using Homebrew (Recommended)**

```bash
brew tap jugaadlang/tap
brew install jugaadlang
```

**Option B: Using pip**

```bash
pip3 install jugaadlang
```

### Verify Installation

```bash
jug --version
```

### Run

```bash
jug run hello.jug
```

---

# 🚀 Install Latest Development Version

Install directly from GitHub:

```bash
pip install git+https://github.com/JugaadLang/jugaadlang.git
```

Verify:

```bash
jug --version
```

---

# 📦 Package Manager

JugaadLang includes a built-in package manager.

### Install Package

```bash
jug install chai
```

### Search Package

```bash
jug search chai
```

### Update Packages

```bash
jug update
```

### Remove Package

```bash
jug remove chai
```

---

# ⚡ Interactive REPL

Start the JugaadLang shell:

```bash
jug repl
```

Example:

```text
>>> bolo("Namaste")
Namaste
```

---

# 🔧 Common Commands

| Command                | Description           |
| ---------------------- | --------------------- |
| `jug run file.jug`  | Run a program         |
| `jug compile file.jug` | Transpile to Python |
| `jug repl`          | Open REPL             |
| `jug install pkg`   | Install package       |
| `jug update pkg`    | Update a package      |
| `jug search pkg`    | Search package        |
| `jug remove pkg`    | Remove package        |
| `jug doctor`        | Diagnose installation |
| `jug --version`     | Show version          |
| `jug --help`        | Show help             |

---

# 🎉 Success

---

## Language Keywords Reference

| Python Keyword | JugaadLang | Hindi Literal Meaning |
| :--- | :--- | :--- |
| `print` | `bolo` | Say / Speak |
| `input` | `poochho` | Ask |
| `if` | `agar` | If |
| `elif` | `shayad` | Maybe / Perhaps |
| `else` | `warna` | Otherwise |
| `for` | `ghumo` | Iterate / Roam |
| `while` | `jabtak` | Until / As long as |
| `def` | `banao` | Create / Make |
| `return` | `wapas` | Return / Back |
| `class` | `ustad` | Master / Teacher |
| `self` | `khud` | Self |
| `import` | `lao` | Import / Bring |
| `from` | `se` | From |
| `break` | `rukja` | Stop! |
| `continue` | `chalte_raho` | Keep going |
| `try` | `koshish` | Try / Attempt |
| `except` | `gadbad` | Problem / Exception |
| `finally` | `aakhir_me` | In the end |
| `raise` | `udao` | Throw / Raise |
| `True` | `sahi` | Correct / True |
| `False` | `galat` | Wrong / False |
| `None` | `kuch_nahi` | Nothing / None |
| `and` | `aur` | And |
| `or` | `ya` | Or |
| `not` | `nahi` | Not |
| `async` | `tez` | Fast / Async |
| `await` | `intezaar` | Wait / Await |
| `yield` | `baanto` | Distribute / Yield |
| `pass` | `theek_hai` | Fine / Pass |
| `global` | `sabka` | Everyone's / Global |
| `lambda` | `chota_funkshan` | Little function |
| `in` | `mein` | In |
| `is` | `hai` | Is |
| `match` | `agar_match` | Pattern match subject block |
| `case` | `kaand` | Case block in pattern match |

---

## Standard Built-in Function Mappings

JugaadLang supports Roman Hindi wrappers for standard Python built-in functions. They map directly to Python's built-ins:

| Python Built-in | JugaadLang | Hindi Translation | Description |
| :--- | :--- | :--- | :--- |
| `abs` | `maan` | Value / Magnitude | Absolute value of a number |
| `all` | `sab` | All | True if all items in iterable are true |
| `any` | `koi_bhi` | Any / Anyone | True if any item in iterable is true |
| `bin` | `binary` | Binary | Binary representation of an integer |
| `bool` | `satyata` | Truth value | Evaluates boolean value |
| `callable` | `bulaane_yogya` | Callable | Checks if object is callable |
| `chr` | `akshar` | Character | Returns character from Unicode point |
| `delattr` | `gun_hatao` | Remove attribute | Deletes attribute from object |
| `dict` | `kosh` | Dictionary / Lexicon | Returns a dictionary (map) |
| `divmod` | `bhag_shesh` | Quotient-Remainder | Returns (quotient, remainder) |
| `enumerate` | `ginti` | Counting / Enumerate | Returns indexed list generator |
| `exec` | `chalao` | Run / Execute | Executes dynamic Python code |
| `filter` | `chhano` | Filter | Filters elements through a function |
| `getattr` | `gun_lao` | Get attribute | Returns attribute value of object |
| `hasattr` | `gun_hai` | Has attribute | Checks if attribute exists on object |
| `help` | `madad` | Help | Starts built-in help text utility |
| `id` | `pehchan` | Identity / ID | Returns unique identity of object |
| `int` | `purnank` | Integer | Converts value to standard integer |
| `isinstance` | `prakar_hai` | Is type of | Checks if object is instance of class |
| `issubclass` | `subclass_hai` | Is subclass of | Checks if class is subclass of another |
| `len` | `lambaee` | Length | Returns length of a sequence |
| `list` | `suchi` | List / Sequence | Creates/converts to list |
| `max` | `adhiktam` | Maximum | Returns largest item |
| `min` | `nyuntam` | Minimum | Returns smallest item |
| `next` | `agla` | Next | Retrieves next item from iterator |
| `object` | `vastu` | Object | Base class object creator |
| `open` | `kholo` | Open | Opens a file handle |
| `pow` | `ghat` | Power / Exponent | Raises number to power (x ** y) |
| `reversed` | `ulta` | Reversed | Returns reversed order iterator |
| `setattr` | `gun_badlo` | Change attribute | Modifies attribute value of object |
| `slice` | `tukda` | Slice | Returns slice object for indexes |
| `sorted` | `kramwar` | Sorted / Sequential | Returns sorted copy of iterable |
| `str` | `shabd` | String / Word | Converts object to string |
| `sum` | `yog` | Sum / Addition | Returns sum of items in iterable |
| `type` | `prakar` | Type / Kind | Returns the type of an object |

---

## Example Usage

### 1. Simple Control Flow (`hello.jug`)
```jugaadlang
# Ask for user name
poochho naam

agar naam == "Sumangal":
    bolo("Legend mil gaya! 😎")
warna:
    bolo("Namaste " + naam)
```

Run it:
```bash
jug run hello.jug
```

### 2. Classes & Functions (`oop.jug`)
```jugaadlang
ustad Developer:
    banao shuru(khud, naam, language):
        khud.naam = naam
        khud.language = language

    banao batao(khud):
        bolo(khud.naam + " code likh raha hai " + khud.language + " mein!")

dev = Developer("Sumangal", "JugaadLang")
dev.batao()

### 3. Pattern Matching (`match.jug`)
```jugaadlang
banao test_match(x):
    agar_match x:
        kaand sahi:
            wapas "boolean true"
        kaand 1:
            wapas "one"
        kaand [a, b]:
            wapas "sequence of " + str(a) + " and " + str(b)
        kaand _:
            wapas "something else"

bolo(test_match(1))
bolo(test_match(sahi))
bolo(test_match([10, 20]))
```
```

---

## Built-in Fun Functions
Enjoy several custom interactive built-ins directly at runtime:
* `chai()`: Prints a warm cup of ASCII tea (`☕ Chai pi lo.`)
* `himmat()`: Prints a motivational programming boost (`🔥 Hidden feature detected.`)
* `ghaas_chhoo()`: Gently reminds you to go touch some grass (`🌱 Bahar ghoom aao.`)
* `bachao()`: Starts a mock search for help (`🚨 StackOverflow search shuru.`)
* `fortune()`: Tells a programmer's fortune (`🔮 Bug line 347 mein ho sakta hai.`)
* `jugaad()`: Gives a random hacking/debugging tip.
* `nazar()`: Blocks bad vibes and bugs (`🧿 Nazar suraksha kavach active! Bad vibes/bugs blocked. 🧿`).
* `ashirwad()`: Boosts runtime success rate with elder blessings (`👵 Sadbhavna aur aashirwad active! Success rate boosted to 100%! 👵`).
* `dhanya_waad()`: Expresses polite gratitude (`🙏 Dhanyawaad! Code chalaane ke liye aapka aabhari hoon. Keep coding! 🙏`).
* `bhagwan_bhala_kare()`: Prays for errors to disappear (`📿 Hey bhagwan, iss error ko apne aap thik kar do! Please! 📿`).
* `paisa_wasool()`: Reminds you that JugaadLang is free (`💸 Paisa Wasool! JugaadLang is 100% free and open-source, your money is safe! 💸`).
* `bas_kar_bhai()`: Advises to stop coding and sleep (`🛑 Bas kar bhai! Kitna code likhega? So ja thodi der. 🛑`).
* `chilla_mat()`: Calms you down during debugging (`🤫 Chilla mat, deep breath le aur debug kar. 🤫`).
* `kundli()`: Performs astrological diagnostics on your code to see if Shani or Rahu are transit-blocking your variables/loops.

---

## Ecosystem & Tooling

### CLI Runner
* **Run a file:** `jug run main.jug` (supports script argument passing like `jug run main.jug arg1 arg2`)
* **Check syntax:** `jug check main.jug`
* **Static type-checking:** `jug typecheck main.jug` (performs static analysis using `mypy` behind the scenes)
* **Transpile to Python source:** `jug compile main.jug -o main.py`
* **Create a boilerplate project:** `jug new my_project`

### Interactive REPL
Launch a beautiful interactive terminal shell:
```bash
jug repl
```
Features auto-completion for all keywords, live syntax highlighting, input history, and double-Enter multiline block detection.

### Package Manager
Integrate pip packages or custom bundles:
* **Install:** `jug install web` (installs Flask, requests, httpx, and aiohttp)
* **Remove:** `jug remove web`
* **Update:** `jug update web`
* **Search:** `jug search query`

### VS Code Extension
Launch the extension from `vscode_extension/`. Features full syntax highlighting for `.jug` files, 25+ snippets, hovered keyword documentation in Hindi, and a status bar icon.

---

## Standard Library (Stdlib)

Import standard libraries using `lao` (e.g. `lao ganit`):
1. **`ganit`**: Hindi wrappers for arithmetic/geometry (e.g. `ganit.sin`, `ganit.pi`, `ganit.sqrt`).
2. **`web`**: HTTP request wrappers (`web.get`, `web.post`) and **JugaadWeb** framework with `@web.agar_route("/")` and `web.chalao()`.
3. **`faili`**: Clean file system API (`faili.padho`, `faili.likho`, `faili.jodo`).
4. **`json`**: Native parser (`json.banao_string`, `json.banao_object`).
5. **`samay`**: DateTime operations (`samay.abhibhi()`, `samay.aaj()`, `samay.soja()`).
6. **`tantra`**: Access system variables (`tantra.argv`, `tantra.exit()`, `tantra.platform`).
7. **`crypto`**: Hash encryption (`crypto.sha256`, `crypto.base64_encode`).
8. **`database`**: SQLite ORM (**JugaadORM**) backing tables with `bachao()` and `filter()`.
9. **Fun Libraries**: `chai`, `jokes`, `motivation`, `fortune`, `memes`, `catfacts`.

---

## Funny Error System

Tired of dry Tracebacks? JugaadLang features humorous Hindi exceptions:

#### SyntaxError
```text
🤦 Bhai kya likh diya?
Faili: hello.jug Line 3, Col 12

  agar x ==
            ^

Error Details: Expected value.
Keyboard strike par hai kya?
```

#### NameError
```text
🕵️ Variable 'x' dhundte dhundte thak gaya.
Faili: hello.jug Line 12

  > bolo(x)

Kya gadbad hai?
  'x' mila hi nahi.

Possible reasons:
  • Typo kiya hai
  • Variable declare karna bhool gaye
  • Universe collapse ho gaya
```

#### DivisionByZero
```text
💀 Zero se divide?
Faili: hello.jug Line 5

Kya gadbad hai?
  Newton bhi confuse ho gaya. Maths seekh lo thoda.
```

---

## Developer Tooling & Testing

For local development and testing, we provide a unified helper script `run.sh` to automate tasks:

```bash
# Clean previous builds, run tests, and perform editable installation
./run.sh all

# Run test suite dynamically under the active Python environment
./run.sh test

# Clean build artifacts and package wheels/tarballs
./run.sh build

# Install JugaadLang locally in editable mode with all development dependencies
./run.sh install
```

All test cases are written using `pytest` inside the `tests/` directory.
