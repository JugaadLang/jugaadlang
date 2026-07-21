"""
Tests for JugaadLang Transformer — JL AST to Python AST conversion.

Covers all keyword mappings, built-in name mappings, and AST node visitors.
"""

from __future__ import annotations

import ast

import pytest

from jugaadlang.lexer.lexer import Lexer
from jugaadlang.parser.parser import Parser
from jugaadlang.transformer.to_python import JugaadToPythonTransformer


def _transform(source: str) -> ast.Module:
    """Helper: lex, parse, and transform JugaadLang source to Python AST."""
    tokens = Lexer(source).tokenize()
    jl_ast = Parser(tokens, source=source).parse()
    transformer = JugaadToPythonTransformer()
    return transformer.transform(jl_ast)


def _unparse(source: str) -> str:
    """Helper: lex, parse, transform, and unparse to Python source string."""
    py_ast = _transform(source)
    return ast.unparse(py_ast)


# ── Trailing newline note ──────────────────────────────────────────────
# ast.unparse() in Python 3.10+ does not consistently produce a trailing
# newline for all constructs. All expected values below omit trailing \n.
# We use rstrip() on comparisons where needed.
# ── Quote style note ───────────────────────────────────────────────────
# ast.unparse() uses single quotes for strings. We match that convention.


@pytest.mark.parametrize(
    ("jug_source", "expected_py"),
    [
        # ── Core keyword mappings ──
        ('bolo("hi")', "print('hi')"),
        ("bolo(42)", "print(42)"),
        # Expression statement pass-through
        ("x + y", "x + y"),
        # ── if / elif / else ──
        ("agar sahi:\n    theek_hai", "if True:\n    pass"),
        (
            'agar x > 5:\n    bolo("ok")\nshayad x > 3:\n    bolo("maybe")\nwarna:\n    bolo("no")',
            "if x > 5:\n    print('ok')\nelif x > 3:\n    print('maybe')\nelse:\n    print('no')",
        ),
        # ── for loop ──
        (
            "ghumo i mein range(5):\n    bolo(i)",
            "for i in range(5):\n    print(i)",
        ),
        # ── while loop ──
        (
            "jabtak x > 0:\n    x = x - 1",
            "while x > 0:\n    x = x - 1",
        ),
        # ── function def ──
        (
            "banao greet(naam):\n    bolo(naam)",
            "def greet(naam):\n    print(naam)",
        ),
        # ── class def ──
        (
            "ustad Animal:\n    theek_hai",
            "class Animal:\n    pass",
        ),
        # ── return ──
        (
            "banao add(a, b):\n    wapas a + b",
            "def add(a, b):\n    return a + b",
        ),
        # ── import ──
        ("lao ganit", "import ganit"),
        # ── from / import ──
        ("se math lao sqrt", "from math import sqrt"),
        # ── import with alias ──
        ("lao ganit jaise g", "import ganit as g"),
        # ── from / import with alias ──
        ("se math lao sqrt jaise s", "from math import sqrt as s"),
        # ── break ──
        (
            "ghumo i mein range(10):\n    agar i == 5:\n        rukja\n    bolo(i)",
            "for i in range(10):\n    if i == 5:\n        break\n    print(i)",
        ),
        # ── continue ──
        (
            "ghumo i mein range(10):\n    agar i % 2 == 0:\n        chalte_raho\n    bolo(i)",
            "for i in range(10):\n    if i % 2 == 0:\n        continue\n    print(i)",
        ),
        # ── pass (theek_hai) ──
        ("agar sahi:\n    theek_hai", "if True:\n    pass"),
        # ── raise ──
        ("udao RuntimeError('fail')", "raise RuntimeError('fail')"),
        # ── try / except / finally ──
        (
            "koshish:\n    x = 1 / 0\ngadbad:\n    x = -1\naakhir_me:\n    bolo('done')",
            "try:\n    x = 1 / 0\nexcept:\n    x = -1\nfinally:\n    print('done')",
        ),
        # ── assert ──
        ("pakka x > 0, 'must be positive'", "assert x > 0, 'must be positive'"),
        # ── delete ──
        ("hatao x", "del x"),
        # ── global ──
        ("sabka x\nx = 10", "global x\nx = 10"),
        # ── nonlocal ──
        ("gair_local x\nx = 20", "nonlocal x\nx = 20"),
        # ── async / await ──
        (
            "tez banao fetch():\n    intezaar sleep(1)\n    wapas 42",
            "async def fetch():\n    await sleep(1)\n    return 42",
        ),
        # ── with (ke_saath) ──
        (
            "ke_saath open('f') jaise f:\n    bolo(f)",
            "with open('f') as f:\n    print(f)",
        ),
    ],
)
def test_statement_keyword_mappings(jug_source: str, expected_py: str) -> None:
    """Verify that JugaadLang statement keywords map to correct Python AST."""
    result = _unparse(jug_source)
    assert result == expected_py, (
        f"\nJugaadLang: {jug_source!r}\nExpected:  {expected_py!r}\nGot:       {result!r}"
    )


# ── Built-in function name mappings ────────────────────────────────────────


@pytest.mark.parametrize(
    ("jug_expr", "expected_py_expr"),
    [
        ("maan(-10)", "abs(-10)"),
        ("sab([sahi, sahi])", "all([True, True])"),
        ("koi_bhi([galat, sahi])", "any([False, True])"),
        ("binary(255)", "bin(255)"),
        ("satyata(1)", "bool(1)"),
        ("akshar(65)", "chr(65)"),
        ("kosh([(1, 'a')])", "dict([(1, 'a')])"),
        ("bhag_shesh(10, 3)", "divmod(10, 3)"),
        ("ginti(['a', 'b'])", "enumerate(['a', 'b'])"),
        ("chhano(f, items)", "filter(f, items)"),
        ("gun_lao(obj, 'attr')", "getattr(obj, 'attr')"),
        ("gun_hai(obj, 'attr')", "hasattr(obj, 'attr')"),
        ("pehchan(x)", "id(x)"),
        ("purnank('42')", "int('42')"),
        ("prakar_hai(x, int)", "isinstance(x, int)"),
        ("subclass_hai(Dog, Animal)", "issubclass(Dog, Animal)"),
        ("lambaee([1, 2, 3])", "len([1, 2, 3])"),
        ("suchi(range(5))", "list(range(5))"),
        ("adhiktam([1, 5, 2])", "max([1, 5, 2])"),
        ("nyuntam([1, 5, 2])", "min([1, 5, 2])"),
        ("agla(iterator)", "next(iterator)"),
        ("vastu()", "object()"),
        ("ghat(2, 10)", "pow(2, 10)"),
        ("ulta([1, 2, 3])", "reversed([1, 2, 3])"),
        ("tukda(1, 10, 2)", "slice(1, 10, 2)"),
        ("kramwar([3, 1, 2])", "sorted([3, 1, 2])"),
        ("shabd(42)", "str(42)"),
        ("yog([1, 2, 3])", "sum([1, 2, 3])"),
        ("prakar(x)", "type(x)"),
        ("khud.naam", "self.naam"),
        ("khud.show()", "self.show()"),
    ],
)
def test_builtin_name_mappings(jug_expr: str, expected_py_expr: str) -> None:
    """Verify that Roman Hindi built-in names map to Python built-ins."""
    source = f"x = {jug_expr}"
    result = _unparse(source)
    expected = f"x = {expected_py_expr}"
    assert result == expected, (
        f"\nJugaadLang: {source!r}\nExpected:  {expected!r}\nGot:       {result!r}"
    )


# ── Class / method special mappings ─────────────────────────────────────


def test_shuru_maps_to_init() -> None:
    """Verify that 'shuru' method name maps to '__init__'."""
    source = "ustad A:\n    banao shuru(khud):\n        khud.x = 10"
    result = _unparse(source)
    expected = "class A:\n\n    def __init__(self):\n        self.x = 10"
    assert result == expected


def test_khud_in_args_maps_to_self() -> None:
    """Verify that 'khud' parameter name maps to 'self'."""
    source = "ustad A:\n    banao show(khud):\n        bolo(khud.x)"
    result = _unparse(source)
    expected = "class A:\n\n    def show(self):\n        print(self.x)"
    assert result == expected


# ── PoochhoStmt (input shorthand) ─────────────────────────────────────


def test_poochho_statement() -> None:
    """Verify that 'poochho naam' becomes 'naam = input()'."""
    source = "poochho naam"
    result = _unparse(source)
    expected = "naam = input()"
    assert result == expected


# ── Assignments ─────────────────────────────────────────────────────────


def test_simple_assignment() -> None:
    """Verify simple assignment translation."""
    source = "x = 42"
    result = _unparse(source)
    expected = "x = 42"
    assert result == expected


def test_augmented_assignment() -> None:
    """Verify augmented assignment translation."""
    source = "x += 10"
    result = _unparse(source)
    expected = "x += 10"
    assert result == expected


def test_annotated_assignment() -> None:
    """Verify type-annotated assignment translation."""
    source = "x: purnank = 42"
    result = _unparse(source)
    expected = "x: int = 42"
    assert result == expected


# ── Boolean / binary / unary operators ─────────────────────────────────


@pytest.mark.parametrize(
    ("jug_expr", "expected_py_expr"),
    [
        ("sahi aur galat", "True and False"),
        ("sahi ya galat", "True or False"),
        ("nahi sahi", "not True"),
        ("x + y", "x + y"),
        ("x - y", "x - y"),
        ("x * y", "x * y"),
        ("x / y", "x / y"),
        ("x % y", "x % y"),
        ("x ** y", "x ** y"),
        ("x << 1", "x << 1"),
        ("x >> 1", "x >> 1"),
        ("x | y", "x | y"),
        ("x ^ y", "x ^ y"),
        ("x & y", "x & y"),
        ("x @ y", "x @ y"),
    ],
)
def test_binary_operators(jug_expr: str, expected_py_expr: str) -> None:
    """Verify binary operator mappings."""
    source = f"x = {jug_expr}"
    result = _unparse(source)
    expected = f"x = {expected_py_expr}"
    assert result == expected, (
        f"\nJugaadLang: {source!r}\nExpected:  {expected!r}\nGot:       {result!r}"
    )


@pytest.mark.parametrize(
    ("jug_expr", "expected_py_expr"),
    [
        ("-x", "-x"),
        ("+x", "+x"),
        ("~x", "~x"),
        ("nahi x", "not x"),
    ],
)
def test_unary_operators(jug_expr: str, expected_py_expr: str) -> None:
    """Verify unary operator mappings."""
    source = f"x = {jug_expr}"
    result = _unparse(source)
    expected = f"x = {expected_py_expr}"
    assert result == expected, (
        f"\nJugaadLang: {source!r}\nExpected:  {expected!r}\nGot:       {result!r}"
    )


# ── Comparison operators ────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("jug_expr", "expected_py_expr"),
    [
        ("x == y", "x == y"),
        ("x != y", "x != y"),
        ("x < y", "x < y"),
        ("x <= y", "x <= y"),
        ("x > y", "x > y"),
        ("x >= y", "x >= y"),
        ("x mein [1, 2]", "x in [1, 2]"),
        ("x mein_nahi [1, 2]", "x not in [1, 2]"),
        ("x hai y", "x is y"),
        ("x nahi_hai y", "x is not y"),
    ],
)
def test_comparison_operators(jug_expr: str, expected_py_expr: str) -> None:
    """Verify comparison operator mappings including Hindi keyword operators."""
    source = f"x = {jug_expr}"
    result = _unparse(source)
    expected = f"x = {expected_py_expr}"
    assert result == expected, (
        f"\nJugaadLang: {source!r}\nExpected:  {expected!r}\nGot:       {result!r}"
    )


# ── Comprehensions ──────────────────────────────────────────────────────


def test_list_comprehension() -> None:
    """Verify list comprehension translation."""
    source = "vals = [x * 2 ghumo x mein range(5)]"
    result = _unparse(source)
    expected = "vals = [x * 2 for x in range(5)]"
    assert result == expected


def test_dict_comprehension() -> None:
    """Verify dict comprehension translation."""
    source = "d = {x: x * 2 ghumo x mein range(3)}"
    result = _unparse(source)
    expected = "d = {x: x * 2 for x in range(3)}"
    assert result == expected


def test_set_comprehension() -> None:
    """Verify set comprehension translation."""
    source = "s = {x ghumo x mein range(3)}"
    result = _unparse(source)
    expected = "s = {x for x in range(3)}"
    assert result == expected


def test_generator_expression() -> None:
    """Verify generator expression translation."""
    source = "g = (x ghumo x mein range(5))"
    result = _unparse(source)
    expected = "g = (x for x in range(5))"
    assert result == expected


# ── Ternary / If expression ────────────────────────────────────────────────


def test_ternary_if_exp() -> None:
    """Verify ternary expression translation."""
    source = "res = 'yes' agar sahi warna 'no'"
    result = _unparse(source)
    expected = "res = 'yes' if True else 'no'"
    assert result == expected


# ── Lambda ──────────────────────────────────────────────────────────────


def test_lambda() -> None:
    """Verify lambda expression translation."""
    source = "f = chota_funkshan x: x * 2"
    result = _unparse(source)
    expected = "f = lambda x: x * 2"
    assert result == expected


# ── Pattern matching ───────────────────────────────────────────────────


def test_match_simple_value() -> None:
    """Verify simple value pattern matching."""
    source = (
        "agar_match x:\n"
        "    kaand 1:\n"
        "        bolo('one')\n"
        "    kaand 2:\n"
        "        bolo('two')"
    )
    result = _unparse(source)
    expected = (
        "match x:\n"
        "    case 1:\n"
        "        print('one')\n"
        "    case 2:\n"
        "        print('two')"
    )
    assert result == expected


def test_match_singleton() -> None:
    """Verify singleton pattern matching (True/False/None)."""
    source = (
        "agar_match x:\n"
        "    kaand sahi:\n"
        "        bolo('true')\n"
        "    kaand kuch_nahi:\n"
        "        bolo('none')"
    )
    result = _unparse(source)
    expected = (
        "match x:\n"
        "    case True:\n"
        "        print('true')\n"
        "    case None:\n"
        "        print('none')"
    )
    assert result == expected


def test_match_sequence() -> None:
    """Verify sequence pattern matching."""
    source = (
        "agar_match x:\n"
        "    kaand [a, b]:\n"
        "        bolo(a + b)"
    )
    result = _unparse(source)
    expected = (
        "match x:\n"
        "    case [a, b]:\n"
        "        print(a + b)"
    )
    assert result == expected


def test_match_wildcard() -> None:
    """Verify wildcard pattern in match."""
    source = (
        "agar_match x:\n"
        "    kaand _:\n"
        "        bolo('anything')"
    )
    result = _unparse(source)
    expected = (
        "match x:\n"
        "    case _:\n"
        "        print('anything')"
    )
    assert result == expected


# ── For-else / while-else ──────────────────────────────────────────────


def test_for_else() -> None:
    """Verify for-else translation."""
    source = (
        "ghumo i mein range(5):\n"
        "    bolo(i)\n"
        "warna:\n"
        "    bolo('done')"
    )
    result = _unparse(source)
    expected = (
        "for i in range(5):\n"
        "    print(i)\n"
        "else:\n"
        "    print('done')"
    )
    assert result == expected


def test_while_else() -> None:
    """Verify while-else translation."""
    source = (
        "jabtak galat:\n"
        "    theek_hai\n"
        "warna:\n"
        "    bolo('done')"
    )
    result = _unparse(source)
    expected = (
        "while False:\n"
        "    pass\n"
        "else:\n"
        "    print('done')"
    )
    assert result == expected


# ── F-strings ──────────────────────────────────────────────────────────


def test_fstring_basic() -> None:
    """Verify basic f-string translation."""
    source = 'bolo(f"Hello {naam}")'
    result = _unparse(source)
    expected = "print(f'Hello {naam}')"
    assert result == expected


def test_fstring_expression() -> None:
    """Verify f-string with expression translation."""
    source = 'bolo(f"Sum: {x + y}")'
    result = _unparse(source)
    expected = "print(f'Sum: {x + y}')"
    assert result == expected


# ── Attribute access and subscripts ────────────────────────────────────


def test_attribute_access() -> None:
    """Verify attribute access translation."""
    source = "x = obj.method"
    result = _unparse(source)
    expected = "x = obj.method"
    assert result == expected


def test_subscript() -> None:
    """Verify subscript access translation."""
    source = "x = items[0]"
    result = _unparse(source)
    expected = "x = items[0]"
    assert result == expected


def test_slice() -> None:
    """Verify slice notation translation."""
    source = "x = items[1:10:2]"
    result = _unparse(source)
    expected = "x = items[1:10:2]"
    assert result == expected


# ── Class inheritance ─────────────────────────────────────────────────


def test_class_inheritance() -> None:
    """Verify class inheritance translation."""
    source = "ustad Dog(Animal):\n    theek_hai"
    result = _unparse(source)
    expected = "class Dog(Animal):\n    pass"
    assert result == expected


def test_class_with_methods() -> None:
    """Verify class with multiple methods translation."""
    source = (
        "ustad Animal:\n"
        "    banao shuru(khud, naam):\n"
        "        khud.naam = naam\n"
        "    banao speak(khud):\n"
        "        bolo(khud.naam)"
    )
    result = _unparse(source)
    expected = (
        "class Animal:\n"
        "\n"
        "    def __init__(self, naam):\n"
        "        self.naam = naam\n"
        "\n"
        "    def speak(self):\n"
        "        print(self.naam)"
    )
    assert result == expected


# ── Decorators ─────────────────────────────────────────────────────────


def test_decorator() -> None:
    """Verify decorator translation."""
    source = "@staticmethod\nbanao helper():\n    theek_hai"
    result = _unparse(source)
    expected = "@staticmethod\ndef helper():\n    pass"
    assert result == expected


# ── Type annotations ───────────────────────────────────────────────────


def test_function_type_annotations() -> None:
    """Verify function type annotation translation."""
    source = "banao add(a: purnank, b: purnank) -> purnank:\n    wapas a + b"
    result = _unparse(source)
    expected = "def add(a: int, b: int) -> int:\n    return a + b"
    assert result == expected


# ── Multiple statements ────────────────────────────────────────────────


def test_multiple_statements() -> None:
    """Verify multiple statements are all translated."""
    source = "x = 10\nbolo(x)"
    result = _unparse(source)
    expected = "x = 10\nprint(x)"
    assert result == expected


def test_nested_statements() -> None:
    """Verify nested control flow translation."""
    source = (
        "agar x > 0:\n"
        "    agar x > 10:\n"
        "        bolo('big')\n"
        "    warna:\n"
        "        bolo('small')"
    )
    result = _unparse(source)
    assert "if x > 0:" in result
    assert "if x > 10:" in result
    assert "print('big')" in result
    assert "print('small')" in result


# ── Async comprehensions ──────────────────────────────────────────────


def test_async_for() -> None:
    """Verify async for loop translation."""
    source = "tez ghumo i mein async_gen():\n    bolo(i)"
    result = _unparse(source)
    expected = "async for i in async_gen():\n    print(i)"
    assert result == expected


# ── Empty module ────────────────────────────────────────────────────────


def test_empty_module() -> None:
    """Verify an empty module produces an empty Python module."""
    source = ""
    result = _unparse(source)
    expected = ""
    assert result == expected


# ── Try / except with specific exception ────────────────────────────────


def test_try_except_specific() -> None:
    """Verify try/except with specific exception type."""
    source = (
        "koshish:\n"
        "    x = 1 / 0\n"
        "gadbad ZeroDivisionError:\n"
        "    bolo('zero')"
    )
    result = _unparse(source)
    expected = (
        "try:\n"
        "    x = 1 / 0\n"
        "except ZeroDivisionError:\n"
        "    print('zero')"
    )
    assert result == expected


def test_try_except_with_alias() -> None:
    """Verify try/except with exception alias."""
    source = (
        "koshish:\n"
        "    x = 1 / 0\n"
        "gadbad ZeroDivisionError jaise e:\n"
        "    bolo(e)"
    )
    result = _unparse(source)
    expected = (
        "try:\n"
        "    x = 1 / 0\n"
        "except ZeroDivisionError as e:\n"
        "    print(e)"
    )
    assert result == expected


# ── Try / else / except ────────────────────────────────────────────────────


def test_try_else() -> None:
    """Verify try/else translation."""
    source = (
        "koshish:\n"
        "    x = 1 / 0\n"
        "gadbad:\n"
        "    x = -1\n"
        "warna:\n"
        "    bolo('ok')"
    )
    result = _unparse(source)
    expected = (
        "try:\n"
        "    x = 1 / 0\n"
        "except:\n"
        "    x = -1\n"
        "else:\n"
        "    print('ok')"
    )
    assert result == expected


# ── For loop with multiple targets ──────────────────────────────────────


def test_for_with_multiple_targets() -> None:
    """Verify for loop with tuple unpacking."""
    source = "ghumo k, v mein items.items():\n    bolo(k + v)"
    result = _unparse(source)
    expected = "for k, v in items.items():\n    print(k + v)"
    assert result == expected
