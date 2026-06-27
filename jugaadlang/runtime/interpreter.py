"""
JugaadLang Runtime — Executes JugaadLang AST after transpiling to Python.
"""

from __future__ import annotations
import ast
import sys
import os
import random
import time
from typing import Any

from ..lexer.lexer import Lexer
from ..parser.parser import Parser
from ..transformer.to_python import JugaadToPythonTransformer
from ..ast_nodes.nodes import ExprStmt
from ..errors.messages import format_error
from .fun_builtins import FUN_BUILTINS


# ── Built-in functions ────────────────────────────────────────────────────────


def kismat(start: int, end: int) -> int:
    """Return a random number between start and end."""
    return random.randint(start, end)


def yadrichhik() -> float:
    """Return a random float between 0 and 1 (like random.random())."""
    return random.random()


def pasand(items: list[Any]) -> Any:
    """Choose a random element from a list (like random.choice())."""
    return random.choice(items)


def sikka() -> str:
    """Return 'Head' or 'Tail'."""
    return random.choice(["Head", "Tail"])


def saaf() -> None:
    """Clear terminal."""
    os.system("clear" if os.name == "posix" else "cls")


def ruk(seconds: float) -> None:
    """Sleep for given seconds."""
    time.sleep(seconds)


def bahar() -> None:
    """Exit program."""
    sys.exit()


def namaste() -> None:
    """Displays a welcome banner."""
    banner = """
       __                             ________                 
      / /_  ______ _____ _____ _____/ / / / /___ _____  ____ 
 __  / / / / / __ `/ __ `/ __ `/ __  / / / / __ `/ __ \\/ __ `
/ /_/ / /_/ / /_/ / /_/ / /_/ / /_/ / / / / /_/ / / / / /_/ /
\\____/\\__,_/\\__, /\\__,_/\\__,_/\\__,_/_/_/_/\\__,_/_/ /_/\\__, / 
           /____/                                    /____/  
"""
    print(banner)
    print("Welcome to JugaadLang! The desi way to code. 🇮🇳")


def version() -> None:
    """Show JugaadLang version."""
    from ..__init__ import __version__

    print(f"JugaadLang Version: {__version__}")


def madad() -> None:
    """Show available commands and functions."""
    help_text = """
📚 JugaadLang Full Help Menu 📚

--- Standard I/O ---
bolo(x)            : Print x to console.
poochho(prompt)    : Read input from console.

--- Data Types & Conversion ---
purnank(x)         : Convert to Integer.
dashamlav(x)        : Convert to Float / Decimal.
shabd(x)           : Convert to String / Text.
suchi(x)           : Convert to List.
yugm(x)            : Convert to Tuple.
samuchay(x)        : Convert to Set.
jama_huya(x)       : Convert to FrozenSet.
suchi_batao(x)     : Show list of attributes (dir).
kosh(x)            : Convert to Dictionary.
satyata(x)         : Convert to Boolean (True/False).
prakar(x)          : Get type of x.
pratinidh(x)       : Get representation (repr).
kram(c)            : Get Unicode code point of character.

--- Math & Logic ---
yog(x)             : Sum.
adhiktam(a, b)     : Max value.
nyuntam(a, b)      : Min value.
maan(x)            : Absolute value.
gol(x, n)          : Round x to n decimal places.
ghat(x, y)         : x raised to power y (pow).
avdhi(start, end)  : Generate range of numbers.
lambaee(x)         : Length of x.

--- Functional Programming ---
manchitra(f, seq)  : Apply function f to each item in seq (map).
jod(seq1, seq2)    : Combine sequences element-wise (zip).

--- Random Functions ---
kismat(start, end) : Returns a random integer.
pasand(list)       : Choose a random element from a list.
sikka()            : Returns "Head" or "Tail".
yadrichhik()       : Returns a random float between 0 and 1.

--- OOP ---
uper()             : Call superclass method (super).

--- System Functions ---
saaf()             : Clear terminal.
ruk(seconds)       : Sleep for `seconds` seconds.
bahar()            : Exit program.

--- Fun & Desi Functions ---
namaste()          : Displays a welcome banner.
chai()             : Motivational message.
jugaad()           : Random coding tip.
himmat()           : Hidden feature message.
ghaas_chhoo()      : Touch grass message.
bachao()           : StackOverflow rescue.
fortune()          : Random tech fortune.
nazar()            : Ward off evil eye.
ashirwad()         : Success blessing.
paisa_wasool()     : Value for money message.
kundli()           : Code horoscope.

--- Developer Functions ---
debug(variable)    : Print debug information about a variable.
version()          : Show JugaadLang version.
madad()            : Show this help menu.
"""
    print(help_text)


def himmat() -> None:
    """Print a hidden feature message."""
    print("🔥 Hidden feature detected. Aapke andar himmat hai!")


def bachao() -> None:
    """Print a stackoverflow search message."""
    print("🚨 StackOverflow search shuru. Bachao bachao!")


def fortune() -> None:
    """Print a random funny fortune."""
    fortunes = [
        "🔮 Bug line 347 mein ho sakta hai.",
        "🔮 Agla deploy Friday ko mat karna.",
        "🔮 Error resolved ho chuka hai, bas code likhna baaki hai.",
        "🔮 Shani bhaari hai aapke variable declarations par.",
        "🔮 Chai cup mein garam hai, compiler keyboard par ready hai.",
    ]
    print(random.choice(fortunes))


def jugaad_help() -> None:
    """Print standard jugaad tips."""
    tips = [
        "🛠️ Restart karke dekho, 90% bugs solve ho jaate hain.",
        "🛠️ Print statement dalkar debug karo, debugger to shauk ke liye hai.",
        "🛠️ Commit karke so jao, subah tak apne aap thik ho jayega.",
        "🛠️ StackOverflow se copy karte waqt variable name change karna na bhoolna.",
    ]
    print(random.choice(tips))


def dhanya_waad() -> None:
    """Print a polite but funny Indian thank you."""
    print("🙏 Dhanyawaad! Code chalaane ke liye aapka aabhari hoon. Keep coding! 🙏")


def chilla_mat() -> None:
    """Print a message to calm down when compiler throws errors."""
    print("🤫 Chilla mat, deep breath le aur debug kar. 🤫")


# ── Interpreter ───────────────────────────────────────────────────────────────


class JugaadInterpreter:
    """
    Executes JugaadLang code.
    Maintains a persistent global execution context, ideal for REPL session reuse.
    """

    def __init__(self, filename: str = "<stdin>") -> None:
        self.filename = filename

        # Persistent global namespace
        self.globals: dict[str, Any] = {
            "__builtins__": __builtins__,
            # Built-in variables
            "bolo": print,
            "poochho": input,
            # Built-in funny functions
            "kismat": kismat,
            "sikka": sikka,
            "yadrichhik": yadrichhik,
            "pasand": pasand,
            "saaf": saaf,
            "ruk": ruk,
            "bahar": bahar,
            "namaste": namaste,
            "version": version,
            "himmat": himmat,
            "bachao": bachao,
            "jugaad": jugaad_help,
            "dhanya_waad": dhanya_waad,
            "chilla_mat": chilla_mat,
            # Mappings for builtins
            "maan": abs,
            "sab": all,
            "koi_bhi": any,
            "binary": bin,
            "satyata": bool,
            "bulaane_yogya": callable,
            "akshar": chr,
            "dashamlav": float,
            "gun_hatao": delattr,
            "gol": round,
            "jama_huya": frozenset,
            "jod": zip,
            "kosh": dict,
            "kram": ord,
            "bhag_shesh": divmod,
            "ginti": enumerate,
            "chalao": exec,
            "chhano": filter,
            "gun_lao": getattr,
            "gun_hai": hasattr,
            "madad": madad,
            "manchitra": map,
            "pehchan": id,
            "pratinidh": repr,
            "purnank": int,
            "prakar_hai": isinstance,
            "subclass_hai": issubclass,
            "lambaee": len,
            "suchi": list,
            "suchi_batao": dir,
            "adhiktam": max,
            "nyuntam": min,
            "agla": next,
            "avdhi": range,
            "vastu": object,
            "kholo": open,
            "ghat": pow,
            "ulta": reversed,
            "gun_badlo": setattr,
            "tukda": slice,
            "kramwar": sorted,
            "shabd": str,
            "samuchay": set,
            "yog": sum,
            "prakar": type,
            "uper": super,
            "yugm": tuple,
        }
        self.globals.update(FUN_BUILTINS)

        # Set up stdlib import path
        stdlib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "stdlib"))
        if stdlib_path not in sys.path:
            sys.path.insert(0, stdlib_path)

    def run(self, source: str) -> None:
        """Run JugaadLang source code as statements (exec mode)."""
        try:
            # 1. Lexical analysis
            lexer = Lexer(source, self.filename)
            tokens = lexer.tokenize()

            # 2. Syntax analysis
            parser = Parser(tokens, self.filename, source)
            ast_mod = parser.parse()

            # 3. Transpile to Python AST
            transformer = JugaadToPythonTransformer(self.filename)
            py_ast = transformer.transform(ast_mod)

            # 4. Compile Python AST to bytecode
            code_obj = compile(py_ast, self.filename, "exec")

            # 5. Execute bytecode in the persistent namespace
            exec(code_obj, self.globals, self.globals)
        except Exception as e:
            # Print funny error message and re-raise / handle
            formatted = format_error(e, source, self.filename)
            print(formatted, file=sys.stderr)
            raise

    def run_expression(self, source: str) -> Any:
        """
        Evaluate JugaadLang source.
        If it's a single expression, evaluate and return its value (eval mode).
        Otherwise, execute as standard statements (exec mode).
        """
        try:
            lexer = Lexer(source, self.filename)
            tokens = lexer.tokenize()
            parser = Parser(tokens, self.filename, source)
            ast_mod = parser.parse()

            # If the source is a single expression statement, evaluate it and return the result
            if len(ast_mod.body) == 1 and isinstance(ast_mod.body[0], ExprStmt):
                expr_node = ast_mod.body[0].value

                transformer = JugaadToPythonTransformer(self.filename)
                py_expr_ast = transformer.visit(expr_node)

                py_expr = ast.Expression(body=py_expr_ast)
                ast.fix_missing_locations(py_expr)

                code_obj = compile(py_expr, self.filename, "eval")
                return eval(code_obj, self.globals, self.globals)
            else:
                # Compile and execute as a normal module block
                transformer = JugaadToPythonTransformer(self.filename)
                py_ast = transformer.transform(ast_mod)
                code_obj = compile(py_ast, self.filename, "exec")
                exec(code_obj, self.globals, self.globals)
                return None
        except Exception as e:
            formatted = format_error(e, source, self.filename)
            print(formatted, file=sys.stderr)
            raise
