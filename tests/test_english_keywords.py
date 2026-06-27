"""
Tests for JugaadLang English/Python Keyword Interop.

Verifies that all English keyword equivalents (if, def, class, for, while,
return, True, False, None, etc.) work identically to their Hindi counterparts
at the lexer, parser, and runtime levels.
"""

from jugaadlang.lexer.tokens import TokenType
from jugaadlang.lexer.lexer import Lexer
from jugaadlang.parser.parser import Parser
from jugaadlang.runtime.interpreter import JugaadInterpreter
from jugaadlang.ast_nodes.nodes import (
    Module,
    ExprStmt,
    Call,
    Name,
    Assign,
    If,
    While,
    For,
    FunctionDef,
    ClassDef,
    Constant,
    Break,
    Continue,
    Pass,
    Return,
    Raise,
    Try,
    Assert,
    Import,
    ImportFrom,
    Global,
    Nonlocal,
    Delete,
    With,
    BoolOp,
    Compare,
    Lambda,
    IfExp,
    Match,
    MatchAs,
    MatchSingleton,
    MatchValue,
    Await,
    Yield,
    YieldFrom,
    List,
    Tuple,
    Starred,
)


# ═════════════════════════════════════════════════════════════════════════════
#  LEXER TESTS
# ═════════════════════════════════════════════════════════════════════════════

class TestEnglishKeywordsLexer:
    """Verify English keywords produce the same token types as Hindi ones."""

    def test_control_flow_keywords(self):
        """Control flow: if, elif, else, for, while"""
        src = "if elif else for while"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.AGAR,    # if
            TokenType.SHAYAD,  # elif
            TokenType.WARNA,   # else
            TokenType.GHUMO,   # for
            TokenType.JABTAK,  # while
        ], f"Got: {types}"

    def test_loop_control_keywords(self):
        """Loop control: break, continue, pass"""
        src = "break continue pass"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.RUKJA,        # break
            TokenType.CHALTE_RAHO,  # continue
            TokenType.THEEK_HAI,    # pass
        ], f"Got: {types}"

    def test_function_class_keywords(self):
        """Function/class: def, return, class, lambda, yield"""
        src = "def return class lambda yield"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.BANAO,          # def
            TokenType.WAPAS,          # return
            TokenType.USTAD,          # class
            TokenType.CHOTA_FUNKSHAN,  # lambda
            TokenType.BAANTO,         # yield
        ], f"Got: {types}"

    def test_keyword_constants(self):
        """Constants: True, False, None"""
        src = "True False None"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.SAHI,       # True
            TokenType.GALAT,      # False
            TokenType.KUCH_NAHI,  # None
        ], f"Got: {types}"

    def test_boolean_operators(self):
        """Boolean/logical: and, or, not, in, is"""
        src = "and or not in is"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.AUR,   # and
            TokenType.YA,    # or
            TokenType.NAHI,  # not
            TokenType.MEIN,  # in
            TokenType.HAI,   # is
        ], f"Got: {types}"

    def test_exception_keywords(self):
        """Exception handling: try, except, finally, raise"""
        src = "try except finally raise"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.KOSHISH,   # try
            TokenType.GADBAD,    # except
            TokenType.AAKHIR_ME, # finally
            TokenType.UDAO,      # raise
        ], f"Got: {types}"

    def test_import_keywords(self):
        """Imports: import, from, as"""
        src = "import from as"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.LAO,  # import
            TokenType.SE,   # from
            TokenType.AS,   # as
        ], f"Got: {types}"

    def test_declaration_keywords(self):
        """Declarations: global, nonlocal, assert, del, with, async, await"""
        src = "global nonlocal assert del with async await match case call"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        assert types == [
            TokenType.SABKA,        # global
            TokenType.NONLOCAL,     # nonlocal
            TokenType.ASSERT,       # assert
            TokenType.DEL,          # del
            TokenType.WITH,         # with
            TokenType.TEZ,          # async
            TokenType.INTEZAAR,     # await
            TokenType.AGAR_MATCH,   # match
            TokenType.KAAND,        # case
            TokenType.BULAWO,       # call
        ], f"Got: {types}"

    def test_io_keywords(self):
        """I/O: print, input"""
        src = 'print("hello") input("name")'
        lexer = Lexer(src)
        tokens = lexer.tokenize()

        # Verify 'print' tokenizes as BOLO
        assert tokens[0].type == TokenType.BOLO
        assert tokens[0].value == "print"

        # Verify 'input' tokenizes as POOCHHO
        input_tok = [t for t in tokens if t.type == TokenType.POOCHHO]
        assert len(input_tok) == 1, "Should have one POOCHHO token for 'input'"
        assert input_tok[0].value == "input"

    def test_print_is_keyword(self):
        """'print' tokenizes as BOLO keyword"""
        src = "print"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        # First non-EOF token should be BOLO
        non_eof = [t for t in tokens if t.type != TokenType.EOF]
        assert non_eof[0].type == TokenType.BOLO
        assert non_eof[0].value == "print"

    def test_input_is_keyword(self):
        """'input' tokenizes as POOCHHO keyword"""
        src = "input"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        non_eof = [t for t in tokens if t.type != TokenType.EOF]
        assert non_eof[0].type == TokenType.POOCHHO
        assert non_eof[0].value == "input"

    def test_yield_keywords(self):
        """'yield' and 'baanto' both tokenize as BAANTO"""
        src = "yield baanto"
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        non_eof = [t for t in tokens if t.type != TokenType.EOF]
        assert len(non_eof) == 2
        assert non_eof[0].type == TokenType.BAANTO
        assert non_eof[0].value == "yield"
        assert non_eof[1].type == TokenType.BAANTO
        assert non_eof[1].value == "baanto"


# ═════════════════════════════════════════════════════════════════════════════
#  PARSER TESTS
# ═════════════════════════════════════════════════════════════════════════════

class TestEnglishKeywordsParser:
    """Verify English keywords produce correct AST nodes."""

    def test_if_statement(self):
        """if cond: body"""
        src = "if True:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, If)
        assert isinstance(stmt.test, Constant)
        assert stmt.test.value is True
        assert len(stmt.body) == 1

    def test_if_elif_else(self):
        """if/elif/else chain"""
        src = "if x > 0:\n    pass\nelif x == 0:\n    pass\nelse:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, If)
        # elif becomes a nested If in orelse
        assert len(stmt.orelse) == 1
        assert isinstance(stmt.orelse[0], If)
        # else is the orelse of the inner if
        assert len(stmt.orelse[0].orelse) > 0

    def test_for_loop(self):
        """for target in iter: body"""
        src = "for i in range(10):\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, For)
        assert isinstance(stmt.target, Name)
        assert stmt.target.id == "i"

    def test_for_else_loop(self):
        """for...else with English keywords"""
        src = "for i in range(5):\n    pass\nelse:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, For)
        assert len(stmt.orelse) > 0

    def test_while_loop(self):
        """while cond: body"""
        src = "while True:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, While)
        assert isinstance(stmt.test, Constant)
        assert stmt.test.value is True

    def test_while_else_loop(self):
        """while...else with English keywords"""
        src = "while False:\n    pass\nelse:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, While)
        assert len(stmt.orelse) > 0

    def test_function_def(self):
        """def name(args): body"""
        src = "def add(x, y):\n    return x + y\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, FunctionDef)
        assert stmt.name == "add"
        assert len(stmt.args.args) == 2

    def test_function_return(self):
        """return statement"""
        src = "def foo():\n    return 42\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, FunctionDef)
        ret = stmt.body[0]
        assert isinstance(ret, Return)
        assert ret.value is not None

    def test_class_def(self):
        """class Name: body"""
        src = "class Animal:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, ClassDef)
        assert stmt.name == "Animal"

    def test_class_inheritance(self):
        """class Child(Parent): body"""
        src = "class Dog(Animal):\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, ClassDef)
        assert stmt.name == "Dog"
        assert len(stmt.bases) == 1

    def test_break_continue_pass(self):
        """break, continue, pass as simple statements"""
        src = "while True:\n    break\n    continue\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, While)
        assert isinstance(stmt.body[0], Break)
        assert isinstance(stmt.body[1], Continue)
        assert isinstance(stmt.body[2], Pass)

    def test_try_except(self):
        """try/except with English keywords"""
        src = "try:\n    pass\nexcept:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Try)
        assert len(stmt.handlers) == 1

    def test_try_except_else_finally(self):
        """try/except/else/finally"""
        src = "try:\n    pass\nexcept:\n    pass\nelse:\n    pass\nfinally:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Try)
        assert len(stmt.orelse) > 0
        assert len(stmt.finalbody) > 0

    def test_raise_statement(self):
        """raise Exception"""
        src = "raise ValueError('x')\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        # 'raise' is parsed as a Raise statement, not an ExprStmt
        assert isinstance(stmt, Raise)
        assert stmt.exc is not None

    def test_import_statement(self):
        """import module"""
        src = "import math\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Import)
        assert stmt.names[0].name == "math"

    def test_from_import(self):
        """from module import name"""
        src = "from math import sqrt\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, ImportFrom)
        assert stmt.module == "math"
        assert stmt.names[0].name == "sqrt"

    def test_import_as(self):
        """import module as alias"""
        src = "import numpy as np\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Import)
        assert stmt.names[0].asname == "np"

    def test_global_nonlocal_assert_del(self):
        """global, nonlocal, assert, del"""
        src = "global x\nnonlocal y\nassert True\ndel z\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        assert isinstance(ast_mod.body[0], Global)
        assert isinstance(ast_mod.body[1], Nonlocal)
        assert isinstance(ast_mod.body[2], Assert)
        assert isinstance(ast_mod.body[3], Delete)

    def test_with_statement(self):
        """with ctx as var: body"""
        src = "with open('f') as f:\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, With)

    def test_lambda(self):
        """lambda x: expr"""
        src = "lambda x: x + 1\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, ExprStmt)
        assert isinstance(stmt.value, Lambda)

    def test_match_case(self):
        """match/case with English keywords"""
        src = "match x:\n    case 1:\n        pass\n    case _:\n        pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Match)
        assert len(stmt.cases) == 2
        assert isinstance(stmt.cases[0].pattern, MatchValue)
        assert isinstance(stmt.cases[1].pattern, MatchAs)

    def test_async_def(self):
        """async def fn(): await ..."""
        src = "async def fetch():\n    await get_data()\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, FunctionDef)
        assert stmt.is_async is True
        assert isinstance(stmt.body[0], ExprStmt)
        assert isinstance(stmt.body[0].value, Await)

    def test_not_in_operator(self):
        """'not in' comparison operator using English keywords"""
        src = "x = 5 not in [1, 2, 3]\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Assign)
        assert isinstance(stmt.value, Compare)
        assert stmt.value.ops == ["mein_nahi"]

    def test_is_not_operator(self):
        """'is not' comparison operator using English keywords"""
        src = "x = None is not 5\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Assign)
        assert isinstance(stmt.value, Compare)
        assert stmt.value.ops == ["nahi_hai"]

    def test_chained_not_in(self):
        """Chained 'not in' comparisons"""
        src = "result = x not in a not in b\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Assign)
        assert isinstance(stmt.value, Compare)
        assert len(stmt.value.ops) == 2
        assert stmt.value.ops == ["mein_nahi", "mein_nahi"]

    def test_true_false_none_constants(self):
        """True, False, None as keyword constants"""
        src = "a = True\nb = False\nc = None\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        assert ast_mod.body[0].value.value is True
        assert ast_mod.body[1].value.value is False
        assert ast_mod.body[2].value.value is None


# ═════════════════════════════════════════════════════════════════════════════
#  RUNTIME TESTS
# ═════════════════════════════════════════════════════════════════════════════

class TestEnglishKeywordsRuntime:
    """Verify English keywords execute correctly at runtime."""

    def test_if_runtime(self):
        """if/elif/else at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
x = 5
result = ""
if x > 0:
    result = "positive"
elif x == 0:
    result = "zero"
else:
    result = "negative"
""")
        assert interp.globals["result"] == "positive"

    def test_for_loop_runtime(self):
        """for loop at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
total = 0
for i in range(4):
    total = total + i
""")
        assert interp.globals["total"] == 6

    def test_for_else_runtime(self):
        """for...else at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
flag = False
for i in range(3):
    if i == 10:
        break
else:
    flag = True
""")
        assert interp.globals["flag"] is True

    def test_while_loop_runtime(self):
        """while loop at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
count = 0
x = 5
while x > 0:
    x = x - 1
    count = count + 1
""")
        assert interp.globals["count"] == 5

    def test_function_def_and_call(self):
        """def and return at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
def add(a, b):
    return a + b
result = add(3, 4)
""")
        assert interp.globals["result"] == 7

    def test_class_def_and_use(self):
        """class with methods at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
class Counter:
    def __init__(self, start):
        self.val = start
    def inc(self):
        self.val = self.val + 1
    def get(self):
        return self.val

c = Counter(10)
c.inc()
c.inc()
result = c.get()
""")
        assert interp.globals["result"] == 12

    def test_class_inheritance(self):
        """class inheritance with English keywords"""
        interp = JugaadInterpreter()
        interp.run("""
class Animal:
    def speak(self):
        return "generic"

class Dog(Animal):
    def speak(self):
        return "woof"

a = Animal()
d = Dog()
animal_sound = a.speak()
dog_sound = d.speak()
""")
        assert interp.globals["animal_sound"] == "generic"
        assert interp.globals["dog_sound"] == "woof"

    def test_try_except_runtime(self):
        """try/except at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
caught = False
try:
    x = 1 / 0
except ZeroDivisionError:
    caught = True
""")
        assert interp.globals["caught"] is True

    def test_try_except_else_finally_runtime(self):
        """try/except/else/finally at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
else_hit = False
finally_hit = False
try:
    x = 10
except:
    pass
else:
    else_hit = True
finally:
    finally_hit = True
""")
        assert interp.globals["else_hit"] is True
        assert interp.globals["finally_hit"] is True

    def test_raise_runtime(self):
        """raise at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
def check(x):
    if x < 0:
        raise ValueError("negative")
    return x

caught = False
try:
    check(-1)
except ValueError:
    caught = True
""")
        assert interp.globals["caught"] is True

    def test_break_continue_runtime(self):
        """break and continue at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
result = []
i = 0
while i < 10:
    i = i + 1
    if i == 3:
        continue
    if i == 7:
        break
    result.append(i)
""")
        assert interp.globals["result"] == [1, 2, 4, 5, 6]

    def test_pass_runtime(self):
        """pass at runtime -- should not error"""
        interp = JugaadInterpreter()
        interp.run("""
def empty():
    pass
result = empty()
""")
        assert interp.globals["result"] is None

    def test_import_runtime(self):
        """import at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
import ganit
x = ganit.sqrt(16)
""")
        assert interp.globals["x"] == 4.0

    def test_from_import_runtime(self):
        """from import at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
from ganit import sqrt
x = sqrt(25)
""")
        assert interp.globals["x"] == 5.0

    def test_import_as_alias_runtime(self):
        """import as alias at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
import ganit as g
x = g.sqrt(36)
""")
        assert interp.globals["x"] == 6.0

    def test_assert_runtime(self):
        """assert at runtime (should not raise)"""
        interp = JugaadInterpreter()
        interp.run("assert True, 'should pass'")

    def test_del_runtime(self):
        """del at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
x = 42
del x
""")
        assert "x" not in interp.globals

    def test_global_runtime(self):
        """global at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
x = 10
def modify():
    global x
    x = 20
modify()
""")
        assert interp.globals["x"] == 20

    def test_nonlocal_runtime(self):
        """nonlocal at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
def outer():
    x = 10
    def inner():
        nonlocal x
        x = 20
    inner()
    return x
result = outer()
""")
        assert interp.globals["result"] == 20

    def test_lambda_runtime(self):
        """lambda at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
f = lambda x, y: x * y
result = f(3, 4)
""")
        assert interp.globals["result"] == 12

    def test_not_in_runtime(self):
        """'not in' operator at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
result = 5 not in [1, 2, 3]
""")
        assert interp.globals["result"] is True

    def test_is_not_runtime(self):
        """'is not' operator at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
result = None is not 5
""")
        assert interp.globals["result"] is True

    def test_is_runtime(self):
        """'is' operator at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
x = None
result = x is None
""")
        assert interp.globals["result"] is True

    def test_and_or_not_runtime(self):
        """and/or/not logical operators at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
r1 = True and False
r2 = True or False
r3 = not True
""")
        assert interp.globals["r1"] is False
        assert interp.globals["r2"] is True
        assert interp.globals["r3"] is False

    def test_print_runtime(self, capsys):
        """print at runtime"""
        interp = JugaadInterpreter()
        interp.run('print("hello from english")')
        captured = capsys.readouterr()
        assert "hello from english" in captured.out

    def test_true_false_none_runtime(self):
        """True, False, None at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
a = True
b = False
c = None
""")
        assert interp.globals["a"] is True
        assert interp.globals["b"] is False
        assert interp.globals["c"] is None

    def test_bare_yield_generator(self):
        """Generator function with bare yield"""
        interp = JugaadInterpreter()
        interp.run("""
def count():
    yield 1
    yield 2
    yield 3

gen = count()
r1 = next(gen)
r2 = next(gen)
r3 = next(gen)
""")
        assert interp.globals["r1"] == 1
        assert interp.globals["r2"] == 2
        assert interp.globals["r3"] == 3

    def test_yield_from_generator(self):
        """Generator with yield from"""
        interp = JugaadInterpreter()
        interp.run("""
def inner():
    yield 10
    yield 20

def outer():
    yield from inner()
    yield 30

gen = outer()
r1 = next(gen)
r2 = next(gen)
r3 = next(gen)
""")
        assert interp.globals["r1"] == 10
        assert interp.globals["r2"] == 20
        assert interp.globals["r3"] == 30

    def test_yield_from_list(self):
        """yield from a list literal"""
        interp = JugaadInterpreter()
        interp.run("""
def gen():
    yield from [100, 200, 300]

results = list(gen())
""")
        assert interp.globals["results"] == [100, 200, 300]

    def test_baanto_hindi_yield_runtime(self):
        """Hindi 'baanto' as yield at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
def gen():
    baanto "namaste"
    baanto "duniya"

g = gen()
r1 = next(g)
r2 = next(g)
""")
        assert interp.globals["r1"] == "namaste"
        assert interp.globals["r2"] == "duniya"

    def test_baanto_se_yield_from_runtime(self):
        """Hindi 'baanto se' as yield from at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
def gen():
    baanto se [1, 2, 3]

result = list(gen())
""")
        assert interp.globals["result"] == [1, 2, 3]

    def test_yield_expression_value(self):
        """yield as expression (sending values into generator)"""
        interp = JugaadInterpreter()
        interp.run("""
def echo():
    received = yield
    yield received

gen = echo()
next(gen)  # prime
r1 = gen.send("hello")
""")
        assert interp.globals["r1"] == "hello"

    def test_yield_in_for_loop(self):
        """yield inside a for loop in a generator"""
        interp = JugaadInterpreter()
        interp.run("""
def gen():
    for i in range(3):
        yield i * 10

result = list(gen())
""")
        assert interp.globals["result"] == [0, 10, 20]


# ═════════════════════════════════════════════════════════════════════════════
#  MIXED HINDI/ENGLISH TESTS
# ═════════════════════════════════════════════════════════════════════════════

class TestMixedKeywords:
    """Verify Hindi and English keywords can be mixed freely."""

    def test_mixed_if_for(self):
        """Hindi if (agar) with English for loop"""
        interp = JugaadInterpreter()
        interp.run("""
result = []
for i in range(5):
    agar i > 2:
        result.append(i)
""")
        assert interp.globals["result"] == [3, 4]

    def test_mixed_class_function(self):
        """English class with Hindi function (banao)"""
        interp = JugaadInterpreter()
        interp.run("""
class Calculator:
    banao add(khud, a, b):
        wapas a + b
    def sub(self, a, b):
        return a - b

c = Calculator()
r1 = c.add(10, 5)
r2 = c.sub(10, 5)
""")
        assert interp.globals["r1"] == 15
        assert interp.globals["r2"] == 5

    def test_mixed_comprehension(self):
        """English for-in with Hindi agar filter in comprehension"""
        interp = JugaadInterpreter()
        interp.run("""
result = [x for x in range(10) agar x % 2 == 0]
""")
        assert interp.globals["result"] == [0, 2, 4, 6, 8]

    def test_mixed_try_except(self):
        """English try with Hindi gadbad"""
        interp = JugaadInterpreter()
        interp.run("""
caught = False
try:
    x = 1 / 0
gadbad ZeroDivisionError:
    caught = True
""")
        assert interp.globals["caught"] is True

    def test_mixed_import_use(self):
        """Hindi lao with English as"""
        interp = JugaadInterpreter()
        interp.run("""
lao ganit as g
x = g.sqrt(100)
""")
        assert interp.globals["x"] == 10.0

    def test_mixed_constants(self):
        """Mix Hindi (sahi/galat) and English (True/False/None) constants"""
        interp = JugaadInterpreter()
        interp.run("""
a = True
b = galat
c = None
d = sahi
""")
        assert interp.globals["a"] is True
        assert interp.globals["b"] is False
        assert interp.globals["c"] is None
        assert interp.globals["d"] is True

    def test_mixed_while(self):
        """English while with Hindi condition"""
        interp = JugaadInterpreter()
        interp.run("""
count = 0
while count < 3:
    count = count + 1
    agar count == 2:
        continue
    result = count
""")
        assert interp.globals["result"] == 3

    def test_pure_english_program(self):
        """A complete program using only English keywords"""
        interp = JugaadInterpreter()
        interp.run("""
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def greet(self):
        return "Hello, " + self.name

p = Person("Alice", 30)
greeting = p.greet()

assert greeting == "Hello, Alice"
assert p.age == 30
""")
        assert interp.globals["greeting"] == "Hello, Alice"
        assert interp.globals["p"].age == 30

    def test_pure_hindi_program(self):
        """Same program using only Hindi keywords (should work identically)"""
        interp = JugaadInterpreter()
        interp.run("""
ustad Person:
    banao shuru(khud, naam, umar):
        khud.naam = naam
        khud.umar = umar
    banao namaste(khud):
        wapas "Namaste, " + khud.naam

p = Person("Ravi", 25)
greeting = p.namaste()

assert greeting == "Namaste, Ravi"
assert p.umar == 25
""")
        assert interp.globals["greeting"] == "Namaste, Ravi"
        assert interp.globals["p"].umar == 25


# ═════════════════════════════════════════════════════════════════════════════
#  EDGE CASE TESTS
# ═════════════════════════════════════════════════════════════════════════════

class TestEnglishKeywordsEdgeCases:
    """Edge cases for English keyword interop."""

    def test_print_variable_shadow(self):
        """'print' can be shadowed as a variable (like Python)"""
        interp = JugaadInterpreter()
        interp.run("""
print = 42
val = print
""")
        assert interp.globals["val"] == 42

    def test_input_as_variable(self):
        """'input' can be shadowed as a variable"""
        interp = JugaadInterpreter()
        interp.run("""
input = "hello"
val = input
""")
        assert interp.globals["val"] == "hello"

    def test_self_parameter_name(self):
        """'self' as regular parameter name (not a keyword)"""
        interp = JugaadInterpreter()
        interp.run("""
def foo(self):
    return self

obj = object()
result = foo(obj)
""")
        assert interp.globals["result"] is not None

    def test_else_with_if(self):
        """else with if uses the same token"""
        src = "if True:\n    pass\nelse:\n    pass\n"
        tokens = Lexer(src).tokenize()
        types = [t.type for t in tokens if t.type not in (TokenType.EOF, TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT)]
        # Should have: AGAR, SAHI, COLON, THEEK_HAI, WARNA, COLON, THEEK_HAI
        assert TokenType.WARNA in types

    def test_not_in_edge_cases(self):
        """not in with actual values not in the list"""
        interp = JugaadInterpreter()
        interp.run("""
a = 1
result_a = a not in [1, 2, 3]
result_b = 5 not in [1, 2, 3]
result_c = "x" not in ["a", "b", "c"]
""")
        # 1 IS in [1,2,3], so 'not in' should be False
        assert interp.globals["result_a"] is False
        # 5 is NOT in [1,2,3], so 'not in' should be True
        assert interp.globals["result_b"] is True
        assert interp.globals["result_c"] is True

    def test_ternary_if_else(self):
        """Ternary expression with English if/else keywords"""
        src = "x = 'yes' if True else 'no'\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Assign)
        assert isinstance(stmt.value, IfExp)
        assert isinstance(stmt.value.test, Constant)
        assert stmt.value.test.value is True
        assert stmt.value.body.value == "yes"
        assert stmt.value.orelse.value == "no"

    def test_ternary_runtime(self):
        """Ternary with English if/else at runtime"""
        interp = JugaadInterpreter()
        interp.run("""
r1 = "even" if 10 % 2 == 0 else "odd"
r2 = "odd" if 11 % 2 == 0 else "even"
""")
        assert interp.globals["r1"] == "even"
        assert interp.globals["r2"] == "even"

    def test_from_import_star(self):
        """from module import * with English keywords"""
        src = "from math import *\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, ImportFrom)
        assert len(stmt.names) == 1
        assert stmt.names[0].name == "*"

    def test_bare_yield(self):
        """Bare yield in a generator function"""
        src = "def gen():\n    yield\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        func = ast_mod.body[0]
        assert isinstance(func, FunctionDef)
        assert isinstance(func.body[0], ExprStmt)
        yield_node = func.body[0].value
        assert isinstance(yield_node, Yield)
        assert yield_node.value is None

    def test_yield_expr(self):
        """yield with a value"""
        src = "def gen():\n    yield 42\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        func = ast_mod.body[0]
        assert isinstance(func, FunctionDef)
        assert isinstance(func.body[0], ExprStmt)
        yield_node = func.body[0].value
        assert isinstance(yield_node, Yield)
        assert isinstance(yield_node.value, Constant)
        assert yield_node.value.value == 42

    def test_yield_from_expr(self):
        """yield from with an iterable"""
        src = "def gen():\n    yield from [1, 2, 3]\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        func = ast_mod.body[0]
        assert isinstance(func, FunctionDef)
        assert isinstance(func.body[0], ExprStmt)
        yf_node = func.body[0].value
        assert isinstance(yf_node, YieldFrom)
        assert isinstance(yf_node.value, List)

    def test_yield_in_assignment(self):
        """yield in an assignment context (delegating generator)"""
        src = "def gen():\n    x = yield 5\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        func = ast_mod.body[0]
        assert isinstance(func, FunctionDef)
        assert isinstance(func.body[0], Assign)
        yield_node = func.body[0].value
        assert isinstance(yield_node, Yield)
        assert isinstance(yield_node.value, Constant)
        assert yield_node.value.value == 5

    def test_baanto_hindi_yield(self):
        """Hindi 'baanto' as yield"""
        src = "def gen():\n    baanto 10\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        func = ast_mod.body[0]
        assert isinstance(func, FunctionDef)
        assert isinstance(func.body[0], ExprStmt)
        yield_node = func.body[0].value
        assert isinstance(yield_node, Yield)
        assert yield_node.value.value == 10

    def test_baanto_se_yield_from(self):
        """Hindi 'baanto se' as yield from"""
        src = "def gen():\n    baanto se (1, 2)\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        func = ast_mod.body[0]
        assert isinstance(func, FunctionDef)
        assert isinstance(func.body[0], ExprStmt)
        yf_node = func.body[0].value
        assert isinstance(yf_node, YieldFrom)
        assert isinstance(yf_node.value, Tuple)

    def test_match_case_with_underscore(self):
        """match/case _ wildcard works with English keywords"""
        src = """
match x:
    case _:
        pass
"""
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, Match)
        assert isinstance(stmt.cases[0].pattern, MatchAs)
        assert stmt.cases[0].pattern.name is None

    def test_async_for(self):
        """async for with English keywords"""
        src = "async for x in range(10):\n    pass\n"
        tokens = Lexer(src).tokenize()
        parser = Parser(tokens, source=src)
        ast_mod = parser.parse()
        stmt = ast_mod.body[0]
        assert isinstance(stmt, For)
        assert stmt.is_async is True
