"""
Tests for JugaadLang Parser.
"""

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
from jugaadlang.parser.parser import Parser


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
