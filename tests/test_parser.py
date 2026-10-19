"""
Tests for JugaadLang Parser.
"""

import pytest

from jugaadlang.ast_nodes.nodes import (
    Assign,
    Await,
    Call,
    ClassDef,
    Constant,
    ExprStmt,
    FunctionDef,
    If,
    IfExp,
    Lambda,
    Match,
    MatchAs,
    MatchClass,
    MatchSequence,
    MatchSingleton,
    MatchValue,
    Module,
    Name,
    Slice,
    Subscript,
)
from jugaadlang.lexer.lexer import Lexer
from jugaadlang.parser.parser import ParseError, Parser


def test_parse_expression_stmt():
    src = 'bolo("hello")'
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    assert isinstance(ast_mod, Module)
    assert len(ast_mod.body) == 1
    stmt = ast_mod.body[0]
    assert isinstance(stmt, ExprStmt)
    assert isinstance(stmt.value, Call)
    assert isinstance(stmt.value.func, Name)
    assert stmt.value.func.id == "bolo"


def test_parse_assignment():
    src = "x = 10"
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, Assign)
    assert len(stmt.targets) == 1
    assert isinstance(stmt.targets[0], Name)
    assert stmt.targets[0].id == "x"
    assert isinstance(stmt.value, Constant)
    assert stmt.value.value == 10


def test_parse_if_statement():
    src = "agar sahi:\n    theek_hai\n"
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, If)
    assert isinstance(stmt.test, Constant)
    assert stmt.test.value is True


def test_parse_function_def():
    src = "banao add(x, y):\n    wapas x + y\n"
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, FunctionDef)
    assert stmt.name == "add"
    assert len(stmt.args.args) == 2
    assert stmt.args.args[0].arg == "x"
    assert stmt.args.args[1].arg == "y"


def test_parse_class_inheritance():
    src = "ustad Child(Parent):\n    theek_hai\n"
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, ClassDef)
    assert stmt.name == "Child"
    assert len(stmt.bases) == 1
    assert isinstance(stmt.bases[0], Name)
    assert stmt.bases[0].id == "Parent"


def test_parse_slicing():
    src = "x[1:5:2]"
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, ExprStmt)
    sub = stmt.value
    assert isinstance(sub, Subscript)
    assert isinstance(sub.value, Name)
    assert sub.value.id == "x"
    assert isinstance(sub.slice, Slice)
    assert sub.slice.lower is not None and sub.slice.lower.value == 1  # ty: ignore[unresolved-attribute]
    assert sub.slice.upper is not None and sub.slice.upper.value == 5  # ty: ignore[unresolved-attribute]
    assert sub.slice.step is not None and sub.slice.step.value == 2  # ty: ignore[unresolved-attribute]


def test_parse_lambda():
    src = "chota_funkshan x, y: x + y"
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, ExprStmt)
    lam = stmt.value
    assert isinstance(lam, Lambda)
    assert len(lam.args.args) == 2
    assert lam.args.args[0].arg == "x"
    assert lam.args.args[1].arg == "y"


def test_parse_ternary():
    src = "x agar sahi warna y"
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, ExprStmt)
    ternary = stmt.value
    assert isinstance(ternary, IfExp)
    assert isinstance(ternary.body, Name)
    assert ternary.body.id == "x"
    assert isinstance(ternary.test, Constant)
    assert ternary.test.value is True
    assert isinstance(ternary.orelse, Name)
    assert ternary.orelse.id == "y"


def test_parse_async_await():
    src = "tez banao main():\n    intezaar fetch()\n"
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, FunctionDef)
    assert stmt.is_async is True

    await_stmt = stmt.body[0]
    assert isinstance(await_stmt, ExprStmt)
    assert isinstance(await_stmt.value, Await)
    assert isinstance(await_stmt.value.value, Call)


def test_parse_pattern_matching():
    src = """
agar_match x:
    kaand 1:
        bolo("one")
    kaand sahi agar x:
        bolo("true and truthy")
    kaand [a, b]:
        bolo(a)
    kaand Point(x, y=2):
        bolo(x)
    kaand _:
        bolo("wildcard")
"""
    tokens = Lexer(src).tokenize()
    parser = Parser(tokens, source=src)
    ast_mod = parser.parse()

    stmt = ast_mod.body[0]
    assert isinstance(stmt, Match)
    assert len(stmt.cases) == 5

    # Check cases
    case0 = stmt.cases[0]
    assert isinstance(case0.pattern, MatchValue)
    assert isinstance(case0.pattern.value, Constant)
    assert case0.pattern.value.value == 1

    case1 = stmt.cases[1]
    assert isinstance(case1.pattern, MatchSingleton)
    assert case1.pattern.value is True
    assert isinstance(case1.guard, Name)
    assert case1.guard.id == "x"

    case2 = stmt.cases[2]
    assert isinstance(case2.pattern, MatchSequence)
    assert len(case2.pattern.patterns) == 2
    assert isinstance(case2.pattern.patterns[0], MatchAs)
    assert case2.pattern.patterns[0].name == "a"

    case3 = stmt.cases[3]
    assert isinstance(case3.pattern, MatchClass)
    assert isinstance(case3.pattern, MatchClass) and case3.pattern.cls.id == "Point"  # ty: ignore[unresolved-attribute]
    assert len(case3.pattern.patterns) == 1
    assert case3.pattern.kwd_attrs == ["y"]
    assert isinstance(case3.pattern.kwd_patterns[0], MatchValue)

    case4 = stmt.cases[4]
    assert isinstance(case4.pattern, MatchAs)
    assert case4.pattern.name is None


def parse_source(src: str):
    tokens = Lexer(src).tokenize()
    return Parser(tokens, source=src).parse()


def test_parse_function_arguments_valid_combination():
    ast_mod = parse_source(
        "banao f(a, b=1, *args, c=2, **kwargs):\n    wapas c\n"
    )
    func = ast_mod.body[0]
    assert isinstance(func, FunctionDef)
    arguments = func.args
    assert [item.arg for item in arguments.args] == ["a", "b"]
    assert len(arguments.defaults) == 1
    assert arguments.vararg is not None and arguments.vararg.arg == "args"
    assert [item.arg for item in arguments.kwonlyargs] == ["c"]
    assert len(arguments.kw_defaults) == 1
    assert arguments.kw_defaults[0] is not None
    assert arguments.kwarg is not None and arguments.kwarg.arg == "kwargs"


def test_parse_required_keyword_only_parameter():
    ast_mod = parse_source("banao f(*args, b):\n    wapas b\n")
    arguments = ast_mod.body[0].args
    assert arguments.args == []
    assert [item.arg for item in arguments.kwonlyargs] == ["b"]
    assert arguments.kw_defaults == [None]


def test_parse_required_keyword_only_after_default():
    ast_mod = parse_source("banao f(a=1, *args, b):\n    theek_hai\n")
    arguments = ast_mod.body[0].args
    assert [item.arg for item in arguments.args] == ["a"]
    assert [item.arg for item in arguments.kwonlyargs] == ["b"]


def test_parse_khud_maps_to_self():
    ast_mod = parse_source("ustad Box:\n    banao __init__(khud, val=1):\n        theek_hai\n")
    arguments = ast_mod.body[0].body[0].args
    assert [item.arg for item in arguments.args] == ["self", "val"]


@pytest.mark.parametrize(
    "src",
    [
        "banao f(a=1, b):\n    wapas b\n",
        "banao f(a=1, b, c=3):\n    theek_hai\n",
        "banao f(a=1, b, *args):\n    theek_hai\n",
    ],
)
def test_parse_required_after_default_is_rejected(src):
    with pytest.raises(ParseError) as excinfo:
        parse_source(src)
    assert "needs a default value" in str(excinfo.value)
    assert "'b'" in str(excinfo.value)


@pytest.mark.parametrize(
    "src",
    [
        "banao f(a, a):\n    theek_hai\n",
        "banao f(khud, khud):\n    theek_hai\n",
        "banao f(a, *a):\n    theek_hai\n",
        "banao f(**a, a):\n    theek_hai\n",
        "banao f(*args, **args):\n    theek_hai\n",
        "f = chota_funkshan a, a: a\n",
    ],
)
def test_parse_duplicate_parameter_is_rejected(src):
    with pytest.raises(ParseError) as excinfo:
        parse_source(src)
    assert "declared more than once" in str(excinfo.value)


@pytest.mark.parametrize(
    "src",
    [
        "banao f(*a, *b):\n    theek_hai\n",
        "banao f(**a, **b):\n    theek_hai\n",
    ],
)
def test_parse_second_vararg_or_kwarg_is_rejected(src):
    with pytest.raises(ParseError) as excinfo:
        parse_source(src)
    assert "already has a" in str(excinfo.value)

