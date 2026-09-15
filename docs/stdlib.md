# JugaadLang Standard Library Reference

All standard library modules are imported with `lao` (the Hindi equivalent of `import`).

Start with [functions and modules](functions.html) for import syntax, or [installation](installation.html) for optional dependencies. Examples that write files should be run in a disposable working folder.

## `paath` — Text and strings

Import with `lao paath`.

| Function | Behavior |
| --- | --- |
| `ulta(text)` | Reverse the text |
| `palindrome_hai(text)` | Check a palindrome, ignoring case and spaces |
| `shabd_gino(text)` | Count whitespace-separated words |
| `akshar_gino(text)` | Count characters |
| `bada(text)`, `chota(text)` | Uppercase or lowercase text |
| `title_banao(text)` | Title-case words |
| `saaf(text)` | Trim leading and trailing whitespace |
| `badlo(text, purana, naya)` | Replace occurrences of a substring |
| `shamil_hai(text, khoj)` | Check whether a substring is present |
| `dohrao(text, n)` | Repeat text `n` times |

```jugaadlang
lao paath
bolo(paath.ulta("chai"))
bolo(paath.shabd_gino("Code karo Hindi mein"))
```

Expected output:

```text
iahc
4
```

---

## 1. `ganit` — Mathematics

Hindi wrappers for Python's `math` module.

**Import:** `lao ganit`

### Constants
| Name | Value |
|---|---|
| `ganit.pi` | π (3.14159...) |
| `ganit.e` | e (2.71828...) |
| `ganit.tau` | τ (6.28318...) |
| `ganit.inf` | ∞ |
| `ganit.nan` | NaN |

### Trigonometric Functions
| Function | Python Equivalent |
|---|---|
| `ganit.sin(x)` | `math.sin(x)` |
| `ganit.cos(x)` | `math.cos(x)` |
| `ganit.tan(x)` | `math.tan(x)` |
| `ganit.asin(x)` | `math.asin(x)` |
| `ganit.acos(x)` | `math.acos(x)` |
| `ganit.atan(x)` | `math.atan(x)` |
| `ganit.atan2(y, x)` | `math.atan2(y, x)` |

### Hyperbolic Functions
| Function | Python Equivalent |
|---|---|
| `ganit.sinh(x)` | `math.sinh(x)` |
| `ganit.cosh(x)` | `math.cosh(x)` |
| `ganit.tanh(x)` | `math.tanh(x)` |

### Exponential & Logarithmic
| Function | Python Equivalent |
|---|---|
| `ganit.exp(x)` | `math.exp(x)` |
| `ganit.log(x)` | `math.log(x)` |
| `ganit.log10(x)` | `math.log10(x)` |
| `ganit.log2(x)` | `math.log2(x)` |

### Helpers
| Function | Python Equivalent |
|---|---|
| `ganit.sqrt(x)` | `math.sqrt(x)` |
| `ganit.ceil(x)` | `math.ceil(x)` |
| `ganit.floor(x)` | `math.floor(x)` |
| `ganit.square(x)` | `x * x` |
| `ganit.cube(x)` | `x * x * x` |
| `ganit.factorial(x)` | `math.factorial(x)` |
| `ganit.gcd(a, b)` | `math.gcd(a, b)` |
| `ganit.degrees(r)` | `math.degrees(r)` |
| `ganit.radians(d)` | `math.radians(d)` |
| `ganit.is_nan(x)` | `math.isnan(x)` |
| `ganit.is_inf(x)` | `math.isinf(x)` |

### Example
```jugaadlang
lao ganit
bolo(ganit.pi)
bolo(ganit.sqrt(16))
bolo(ganit.sin(ganit.pi / 2))
```

---

## 2. `faili` — File System Operations

**Import:** `lao faili`

| Function | Description | Python Equivalent |
|---|---|---|
| `faili.padho(path)` | Read file contents | `open().read()` |
| `faili.likho(path, content)` | Write to file (overwrite) | `open().write()` |
| `faili.jodo(path, content)` | Append to file | `open().append()` |
| `faili.mitao(path)` | Delete file or directory | `os.remove()` / `shutil.rmtree()` |
| `faili.hai_kya(path)` | Check if path exists | `os.path.exists()` |
| `faili.list_karo(path)` | List directory contents | `os.listdir()` |
| `faili.folder_banao(path)` | Create directory tree | `os.makedirs()` |

### Example
```jugaadlang
lao faili
faili.likho("notes.txt", "JugaadLang code likha!")
text = faili.padho("notes.txt")
bolo(text)
faili.folder_banao("myproject/src")
```

---

## 3. `json` — JSON Parser

**Import:** `lao json`

| Function | Description | Python Equivalent |
|---|---|---|
| `json.banao_string(obj, indent)` | Serialize to JSON string | `json.dumps()` |
| `json.banao_object(string)` | Parse JSON string | `json.loads()` |

Also re-exports all standard Python `json` module functions (`load`, `dump`, etc.).

### Example
```jugaadlang
lao json

data = {"naam": "Sumu", "umar": 20}
text = json.banao_string(data, indent=2)
bolo(text)

parsed = json.banao_object(text)
bolo(parsed["naam"])
```

---

## 4. `samay` — Date and Time

**Import:** `lao samay`

| Function/Constant | Description | Python Equivalent |
|---|---|---|
| `samay.samay` | Current timestamp | `time.time` |
| `samay.soja(seconds)` | Sleep | `time.sleep()` |
| `samay.ek_second_rukja()` | Sleep 1 second | `time.sleep(1)` |
| `samay.abhibhi()` | Current datetime | `datetime.datetime.now()` |
| `samay.aaj()` | Current date | `datetime.date.today()` |
| `samay.format_karo(dt, fmt)` | Format datetime | `datetime.strftime()` |

### Example
```jugaadlang
lao samay

abhi = samay.abhibhi()
bolo("Aaj ka time: " + samay.format_karo(abhi, "%H:%M:%S"))
aaj_ka_date = samay.aaj()
bolo("Aaj: " + str(aaj_ka_date))
```

---

## 5. `tantra` — System & Environment

**Import:** `lao tantra`

| Name | Description | Python Equivalent |
|---|---|---|
| `tantra.argv` | Command-line arguments | `sys.argv` |
| `tantra.path` | Module search path | `sys.path` |
| `tantra.platform` | OS platform name | `sys.platform` |
| `tantra.name` | OS name | `os.name` |
| `tantra.pid` | Process ID | `os.getpid()` |
| `tantra.environment` | Environment variables dict | `os.environ` |
| `tantra.exit(code)` | Exit program | `sys.exit()` |
| `tantra.folder_ka_naam()` | Current working directory | `os.getcwd()` |
| `tantra.badlo_folder(path)` | Change directory | `os.chdir()` |
| `tantra.shell_chalao(cmd)` | Run shell command | `subprocess.run()` |

### Example
```jugaadlang
lao tantra

bolo("OS: " + tantra.name)
bolo("Folder: " + tantra.folder_ka_naam())
bolo("Mere arguments: " + str(tantra.argv))
```

---

## 6. `crypto` — Cryptography

**Import:** `lao crypto`

| Function | Description |
|---|---|
| `crypto.sha256(text)` | SHA-256 hash |
| `crypto.md5(text)` | MD5 hash |
| `crypto.base64_encode(text)` | Base64 encode |
| `crypto.base64_decode(text)` | Base64 decode |

### Example
```jugaadlang
lao crypto

hash_val = crypto.sha256("Namaste Duniya")
bolo(hash_val)

encoded = crypto.base64_encode("JugaadLang")
bolo(encoded)
```

---

## 7. `database` — JugaadORM (SQLite ORM)

**Import:** `lao database`

### Field Types
| Field | SQL Type |
|---|---|
| `database.String()` | TEXT |
| `database.Integer(primary_key=False)` | INTEGER |
| `database.Float()` | REAL |
| `database.Boolean()` | INTEGER (0/1) |

### Model Methods
| Method | Description |
|---|---|
| `Model.banao_table()` | Create SQLite table |
| `Model.drop_table()` | Drop table |
| `Model.sab()` | Fetch all records |
| `Model.filter(**kwargs)` | Filter records |
| `instance.bachao()` | Insert or update record |
| `instance.mitao()` | Delete record |

### Example
```jugaadlang
lao database

ustad Student(database.Model):
    naam = database.String()
    umar = database.Integer()

Student.banao_table()

st = Student(naam="Sumangal", umar=20)
st.bachao()

results = Student.filter(naam="Sumangal")
ghumo s mein results:
    bolo("Student: " + s.naam + ", ID: " + str(s.id))
```

---

## 8. `web` — HTTP Client & JugaadWeb Framework

**Import:** `lao web`

### HTTP Client Functions
| Function | Description | Python Equivalent |
|---|---|---|
| `web.get(url)` | HTTP GET | `requests.get()` |
| `web.post(url, data)` | HTTP POST | `requests.post()` |
| `web.put(url, data)` | HTTP PUT | `requests.put()` |
| `web.delete(url)` | HTTP DELETE | `requests.delete()` |

### Global Request State
| Name | Description |
|---|---|
| `web.params` | Query parameters (during request handling) |
| `web.body` | Request body (during request handling) |

### JugaadWeb Framework

| Function | Description |
|---|---|
| `web.agar_route(path, methods=["GET"])` | Route decorator |
| `web.chalao(port=5000, host="127.0.0.1")` | Start web server |

### Example
```jugaadlang
lao web

@web.agar_route("/")
banao home():
    wapas {"message": "Namaste Duniya!"}

@web.agar_route("/data", ["GET", "POST"])
banao data():
    wapas {"params": web.params, "body": web.body}

web.chalao(port=5001)
```

---

## 9. Fun Standard Libraries

### `chai` — Tea Module
**Import:** `lao chai`
- `chai.piyo()` — Print ASCII tea art
- `chai.status()` — Return chai status string

### `jokes` — Programmer Jokes
**Import:** `lao jokes`
- `jokes.sunao()` — Print random programmer joke

### `motivation` — Motivation Quotes
**Import:** `lao motivation`
- `motivation.gyan()` — Print random motivational quote

### `fortune` — Fortune Telling
**Import:** `lao fortune`
- `fortune.batao()` — Print random developer fortune

### `memes` — ASCII Memes
**Import:** `lao memes`
- `memes.dikhao()` — Print random ASCII art meme

### `catfacts` — Cat Facts
**Import:** `lao catfacts`
- `catfacts.batao()` — Print random cat fact
