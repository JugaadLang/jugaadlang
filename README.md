<div align="center">
  <h1>JugaadLang 🇮🇳</h1> 
   
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
7. [Documentation](#-documentation)
8. [Standard Library (Stdlib)](#standard-library-stdlib)
9. [Funny Error System](#funny-error-system)
10. [Developer Tooling & Testing](#developer-tooling--testing)

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
jug run hello.jg
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
jug run hello.jg
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
jug run hello.jg
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
jug
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
| `jug run file.jg`   | Run a program         |
| `jug build file.jg` | Build project         |
| `jug repl`          | Open REPL             |
| `jug install pkg`   | Install package       |
| `jug update`        | Update packages       |
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
| `dir` | `suchi_batao` | Show list | Lists attributes of an object |
| `divmod` | `bhag_shesh` | Quotient-Remainder | Returns (quotient, remainder) |
| `enumerate` | `ginti` | Counting / Enumerate | Returns indexed list generator |
| `exec` | `chalao` | Run / Execute | Executes dynamic Python code |
| `filter` | `chhano` | Filter | Filters elements through a function |
| `float` | `dashamlav` | Decimal | Converts value to floating-point number |
| `frozenset` | `jama_huya` | Frozen / Solidified | Creates an immutable set |
| `getattr` | `gun_lao` | Get attribute | Returns attribute value of object |
| `hasattr` | `gun_hai` | Has attribute | Checks if attribute exists on object |
| `help` | `madad` | Help | Starts built-in help text utility |
| `id` | `pehchan` | Identity / ID | Returns unique identity of object |
| `int` | `purnank` | Integer | Converts value to standard integer |
| `isinstance` | `prakar_hai` | Is type of | Checks if object is instance of class |
| `issubclass` | `subclass_hai` | Is subclass of | Checks if class is subclass of another |
| `len` | `lambaee` | Length | Returns length of a sequence |
| `list` | `suchi` | List / Sequence | Creates/converts to list |
| `map` | `manchitra` | Map / Chart | Applies function to every item in iterable |
| `max` | `adhiktam` | Maximum | Returns largest item |
| `min` | `nyuntam` | Minimum | Returns smallest item |
| `next` | `agla` | Next | Retrieves next item from iterator |
| `object` | `vastu` | Object | Base class object creator |
| `open` | `kholo` | Open | Opens a file handle |
| `ord` | `kram` | Order / Rank | Returns Unicode code point of character |
| `pow` | `ghat` | Power / Exponent | Raises number to power (x ** y) |
| `range` | `avdhi` | Range / Span | Generates a sequence of numbers |
| `repr` | `pratinidh` | Representation | Returns string representation of object |
| `reversed` | `ulta` | Reversed | Returns reversed order iterator |
| `round` | `gol` | Round | Rounds a number to given precision |
| `set` | `samuchay` | Set / Collection | Creates/converts to set |
| `setattr` | `gun_badlo` | Change attribute | Modifies attribute value of object |
| `slice` | `tukda` | Slice | Returns slice object for indexes |
| `sorted` | `kramwar` | Sorted / Sequential | Returns sorted copy of iterable |
| `str` | `shabd` | String / Word | Converts object to string |
| `sum` | `yog` | Sum / Addition | Returns sum of items in iterable |
| `super` | `uper` | Super / Above | Returns proxy object for parent class |
| `tuple` | `yugm` | Pair / Tuple | Creates/converts to tuple |
| `type` | `prakar` | Type / Kind | Returns the type of an object |
| `zip` | `jod` | Join / Combine | Combines iterables element-wise |

---

## 100% Python Feature Parity ✅

JugaadLang now provides **complete Hindi built-in function mappings** for the entire Python cheatsheet. Every built-in function explicitly listed in the standard Python reference has a Hindi equivalent:

| Category | Mappings | Coverage |
| :--- | :--- | :--- |
| **Basic Operations** | `bolo`(print), `poochho`(input), `purnank`(int), `dashamlav`(float), `shabd`(str), `prakar`(type), `lambaee`(len), `pehchan`(id), `suchi_batao`(dir) | ✅ 100% |
| **Numbers & Math** | `maan`(abs), `yog`(sum), `adhiktam`(max), `nyuntam`(min), `gol`(round), `ghat`(pow), `avdhi`(range), `kismat`(randint), `yadrichhik`(random), `pasand`(choice) | ✅ 100% |
| **Strings** | `shabd`(str), `akshar`(chr), `kram`(ord), `lambaee`(len), `binary`(bin) | ✅ 100% |
| **Lists** | `suchi`(list), `kramwar`(sorted), `ulta`(reversed), `ginti`(enumerate), `chhano`(filter), `manchitra`(map), `jod`(zip) | ✅ 100% |
| **Tuples** | `yugm`(tuple) | ✅ 100% |
| **Sets** | `samuchay`(set), `jama_huya`(frozenset) | ✅ 100% |
| **Dictionaries** | `kosh`(dict), `gun_lao`(getattr), `gun_hai`(hasattr), `gun_badlo`(setattr), `gun_hatao`(delattr) | ✅ 100% |
| **Control Flow** | `avdhi`(range), `ginti`(enumerate), `sab`(all), `koi_bhi`(any) | ✅ 100% |
| **Functions** | `manchitra`(map), `chhano`(filter), `jod`(zip), `chota_funkshan`(lambda) | ✅ 100% |
| **OOP** | `ustad`(class), `khud`(self), `uper`(super), `prakar_hai`(isinstance), `subclass_hai`(issubclass), `vastu`(object), `bulaane_yogya`(callable) | ✅ 100% |
| **Exceptions** | `koshish`(try), `gadbad`(except), `udao`(raise), `pakka`(assert) | ✅ 100% |
| **File I/O** | `kholo`(open), `tukda`(slice) | ✅ 100% |
| **Modules** | `lao`(import), `se`(from), `jaise`(as), `chalao`(exec) | ✅ 100% |
| **Random** | `kismat`(randint), `pasand`(choice), `yadrichhik`(random), `sikka`(coin) | ✅ 100% |

> 💡 **Every Python built-in function from the standard cheatsheet now has a Hindi mapping.**
> You can write 100% of Python's core functionality using Hindi keywords and function names.

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

---

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

| File | Description |
|---|---|
| [**docs/README.md**](docs/README.md) | 📖 Documentation index — start here to navigate all docs |
| [**docs/Specs.md**](docs/Specs.md) | 📗 Full language specification — syntax, keywords, control flow, OOP, async, pattern matching |
| [**docs/keywords.md**](docs/keywords.md) | 📖 Complete keyword reference — Hindi/English dual keyword system with all built-in mappings |
| [**docs/errors.md**](docs/errors.md) | 🎭 All 24 funny error messages documented with Hindi titles, English translations, and examples |
| [**docs/stdlib.md**](docs/stdlib.md) | 📦 Standard library reference — `ganit`, `faili`, `json`, `samay`, `tantra`, `crypto`, `database`, `web` |
| [**docs/architecture.md**](docs/architecture.md) | 🏛️ System architecture — transpilation pipeline, component descriptions, directory structure |
| [**docs/cli.md**](docs/cli.md) | 💻 CLI command reference — all `jug` commands with examples |
| [**docs/api.md**](docs/api.md) | 🔧 Internal API reference — classes, methods, and data structures for all modules |
| [**docs/contributing.md**](docs/contributing.md) | 🤝 Contributor's guide — development setup, coding standards, adding features, release process |
| [**docs/grammar.ebnf**](docs/grammar.ebnf) | 📐 Formal EBNF grammar for the JugaadLang language |

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
