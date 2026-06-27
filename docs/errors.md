# JugaadLang Error Messages 🎭

JugaadLang turns boring Python errors into **humorous Hindi messages** that entertain while they inform. Every error type has a custom funny title, an elaborate desi explanation, and (for syntax errors) a fancy caret-highlighted display.

---

## Custom Exception Hierarchy

JugaadLang defines its own exception classes for internal use:

```
JugaadError
 ├── JugaadSyntaxError      → Syntax errors ("🤦 Bhai kya likh diya?")
 └── JugaadRuntimeError
      ├── JugaadNameError        → Variable not found
      ├── JugaadTypeError        → Type mismatch
      └── JugaadZeroDivisionError→ Division by zero
```

These are raised directly by the lexer, parser, and transformer before any Python code runs.

---

## All Funny Error Messages

### 1. `SyntaxError` / `JugaadSyntaxError`
**Title:** 🤦 *Bhai kya likh diya?*

| | |
|---|---|
| **Hindi message** | `Keyboard strike par hai kya? Code check karo.` |
| **English** | Did you drop your keyboard? Check your code. |
| **When it occurs** | Invalid syntax — missing colon, mismatched brackets, wrong indentation, etc. |
| **Display** | Full caret-highlighted source line with `^` pointing to the error location. |

---

### 2. `NameError`
**Title:** 🕵️ *Variable `x` dhundte dhundte thak gaya.*

| | |
|---|---|
| **Hindi message** | `'x' mila hi nahi. Possible reasons:\n  • Typo kiya hai\n  • Variable declare karna bhool gaye\n  • Universe collapse ho gaya` |
| **English** | I'm tired of searching for variable `x`. It wasn't found. Possible reasons: typo, forgot to declare it, or the universe collapsed. |
| **When it occurs** | Accessing a variable that doesn't exist in the current scope. |
| **Smart feature** | Automatically extracts the missing variable name from the error and inserts it into the title. |

---

### 3. `ZeroDivisionError`
**Title:** 💀 *Zero se divide?*

| | |
|---|---|
| **Hindi message** | `Newton bhi confuse ho gaya. Maths seekh lo thoda.` |
| **English** | Even Newton is confused. Learn some math. |
| **When it occurs** | Attempting to divide a number by zero. |

---

### 4. `TypeError`
**Title:** 🤔 *Type mismatch ho gaya.*

| | |
|---|---|
| **Hindi message** | `Galat data-type use kiya hai. Computation shock me chala gaya.` |
| **English** | Wrong data type used. The computation went into shock. |
| **When it occurs** | Performing an operation on incompatible types (e.g., `"hello" + 5`). |

---

### 5. `IndexError`
**Title:** 📭 *List mein itna nahi hai!*

| | |
|---|---|
| **Hindi message** | `List ke bahar chala gaya! Itna bada index kahan se mila?` |
| **English** | Gone outside the list! Where did you get such a big index? |
| **When it occurs** | Accessing a list/tuple index that exceeds its length. |
| **Smart feature** | Automatically extracts the list object and index value from the stack frame and shows: `Index X maanga, list mein sirf Y items. Hisaab lagao!` |

---

### 6. `KeyError`
**Title:** 🔑 *Key gayab hai!*

| | |
|---|---|
| **Hindi message** | `Dictionary mein ye key to hai hi nahi. Dhyan se check karo.` |
| **English** | This key isn't in the dictionary. Check carefully. |
| **When it occurs** | Accessing a dictionary key that doesn't exist. |

---

### 7. `AttributeError`
**Title:** 🚫 *Attribute mila hi nahi.*

| | |
|---|---|
| **Hindi message** | `Object me ye feature/method nahi hai boss.` |
| **English** | This object doesn't have that feature/method, boss. |
| **When it occurs** | Accessing an attribute or method that doesn't exist on an object. |

---

### 8. `ModuleNotFoundError`
**Title:** 📦 *Module missing!*

| | |
|---|---|
| **Hindi message** | `Dhundne se bhi nahi mila. Install kiya hai kya? (jug install check karo)` |
| **English** | Couldn't find it even after searching. Did you install it? (Check `jug install`) |
| **When it occurs** | Trying to import a module that isn't installed. |

---

### 9. `ValueError`
**Title:** 🎭 *Value galat hai boss!*

| | |
|---|---|
| **Hindi message** | `Function ko sahi value do na. Ye kya bhej diya?` |
| **English** | Give the function the right value. What did you even send? |
| **When it occurs** | A function receives an argument with the right type but inappropriate value (e.g., `int("abc")`). |

---

### 10. `ImportError`
**Title:** 📥 *Import gadbad ho gaya.*

| | |
|---|---|
| **Hindi message** | `Kuch laane mein problem hai. Module ka naam check karo.` |
| **English** | There's a problem importing something. Check the module name. |
| **When it occurs** | An import statement fails (different from "not found" — module exists but import fails). |

---

### 11. `FileNotFoundError`
**Title:** 📁 *File mili hi nahi!*

| | |
|---|---|
| **Hindi message** | `Jagah sahi hai? File gayab ho gayi? Check karo path.` |
| **English** | Is the location correct? Did the file disappear? Check the path. |
| **When it occurs** | Trying to open a file that doesn't exist at the specified path. |

---

### 12. `PermissionError`
**Title:** 🚫 *Ijjazat nahi hai!*

| | |
|---|---|
| **Hindi message** | `Permission nahi mili. Root bano ya sudo lagao.` |
| **English** | Permission denied. Become root or use sudo. |
| **When it occurs** | Insufficient permissions to read/write a file or execute a command. |

---

### 13. `TimeoutError`
**Title:** ⏰ *Time khatam ho gaya!*

| | |
|---|---|
| **Hindi message** | `Kaafi wait kar liya. Kuch gadbad hai operation mein.` |
| **English** | Waited long enough. Something's wrong with the operation. |
| **When it occurs** | An operation exceeds its time limit. |

---

### 14. `ConnectionError`
**Title:** 🔌 *Connection nahi ho raha!*

| | |
|---|---|
| **Hindi message** | `Internet band hai ya server so gaya. Dobara try karo.` |
| **English** | Internet is off or the server fell asleep. Try again. |
| **When it occurs** | Network connection failures. |

---

### 15. `RecursionError`
**Title:** 🔄 *Loop mein phans gaye!*

| | |
|---|---|
| **Hindi message** | `Recursion itni deep aa gayi ki stack ka dhakkan khul gaya. Base case daalo.` |
| **English** | The recursion went so deep the stack lid flew off. Add a base case. |
| **When it occurs** | Maximum recursion depth exceeded (infinite or too-deep recursion). |

---

### 16. `StopIteration`
**Title:** 🏁 *Iterator khatam ho gaya.*

| | |
|---|---|
| **Hindi message** | `Aur kuch nahi bacha. Next call mat karo ab.` |
| **English** | Nothing left. Don't call next now. |
| **When it occurs** | Calling `next()` on an iterator that has no more items. |

---

### 17. `MemoryError`
**Title:** 🧠 *Yaad kam pad gayi.*

| | |
|---|---|
| **Hindi message** | `RAM ka saath nahi de rahi. Kuch band karo ya RAM badhao.` |
| **English** | RAM isn't supporting you. Close some programs or add more RAM. |
| **When it occurs** | The system runs out of memory. |

---

### 18. `OverflowError`
**Title:** 📈 *Hadd se zyada ho gaya!*

| | |
|---|---|
| **Hindi message** | `Number itna bada ki calculator bhi haar gaya.` |
| **English** | The number is so big even the calculator gave up. |
| **When it occurs** | A numeric calculation exceeds the representable range. |

---

### 19. `FloatingPointError`
**Title:** 🎯 *Point mein gadbad.*

| | |
|---|---|
| **Hindi message** | `Floating point ki precision ne dhoka de diya. Round karke dekho.` |
| **English** | Floating point precision betrayed you. Try rounding. |
| **When it occurs** | Floating-point arithmetic operation fails. |

---

### 20. `EOFError`
**Title:** 📄 *File achanak khatam!*

| | |
|---|---|
| **Hindi message** | `Padhte padhte end aa gaya. Aur kuch data nahi hai.` |
| **English** | Reached the end while reading. There's no more data. |
| **When it occurs** | `input()` or file reading reaches end-of-file unexpectedly. |

---

### 21. `UnicodeError`
**Title:** 🔤 *Unicode samajh nahi aaya.*

| | |
|---|---|
| **Hindi message** | `Characters encoding ki problem. UTF-8 try karo.` |
| **English** | Character encoding problem. Try UTF-8. |
| **When it occurs** | Encoding/decoding text with the wrong character encoding. |

---

### 22. `KeyboardInterrupt`
**Title:** ⌨️ *Ctrl+C! Kaunsi shakti hai ye?*

| | |
|---|---|
| **Hindi message** | `Achha choro, aadha kaam theek hai. Agli baar file se chalao.` |
| **English** | Alright, leave it. Half the work is fine. Next time run from a file. |
| **When it occurs** | User presses Ctrl+C to interrupt the program. |

---

### 23. `AssertionError`
**Title:** 🎯 *Assert ka pakka fail!*

| | |
|---|---|
| **Hindi message** | `Na maanne wali baat galat nikli. Dhyan se check karo.` |
| **English** | The stubborn assertion turned out wrong. Check carefully. |
| **When it occurs** | An `assert` statement fails. |

---

### 24. `NotImplementedError`
**Title:** 🏗️ *Abhi baki hai!*

| | |
|---|---|
| **Hindi message** | `Ye feature abhi implement nahi hua. Khud likhdo.` |
| **English** | This feature hasn't been implemented yet. Write it yourself. |
| **When it occurs** | An abstract method or unimplemented feature is called. |

---

### Fallback (Unknown Error)
**Title:** 💥 *Gadbad Ho Gayi (`ExceptionType`)*

| | |
|---|---|
| **Hindi message** | The original Python error message is displayed as-is. |
| **English** | Something went wrong (with the actual exception type name). |
| **When it occurs** | Any error type that doesn't have a custom funny message yet. |

---

## Error Display Format

All runtime errors are displayed with this structure:

```
🤦/💀/🕵️ Funny Hindi Title
Faili: <filename> Line <line_no>

  > source code line with issue

Kya gadbad hai?
  Detailed Hindi explanation body

Original System Error: <actual Python exception>
```

Syntax errors get a special **caret-highlighted** display:

```
🤦 Bhai kya likh diya?
Faili: <filename> Line <line_no>, Col <col>

  source code line
            ^

Error Details: <syntax error message>
Keyboard strike par hai kya?
```

---

## Error Flow

```
JugaadLang Source Code
        │
        ▼
  ┌─ Lexer ──► LexerError (format_syntax_error)
  │
  ├─ Parser ──► JugaadSyntaxError / ParseError
  │
  ├─ Transformer ──► Python AST (no errors here)
  │
  ├─ compile() ──► SyntaxError (format_syntax_error)
  │
  └─ exec() ──► Runtime Error (format_error)
                      │
                      └─► FUNNY_ERRORS lookup
                            │
                            ├─ Found → Custom funny message
                            │
                            └─ Not Found → Fallback: "💥 Gadbad Ho Gayi"
```

---

## Adding a New Funny Error

To add a new error message, edit `jugaadlang/errors/messages.py` and add an entry to the `FUNNY_ERRORS` dictionary:

```python
"MyCustomError": {
    "title": "🎯 Your funny title",
    "body": "Your elaborate Hindi explanation with \\n newlines.",
},
```

The error type name must match the Python exception class name exactly (case-sensitive).
