"""
Tests for JugaadLang Lexer.
"""

import pytest

from jugaadlang.lexer.lexer import Lexer, LexerError
from jugaadlang.lexer.tokens import TokenType


def test_basic_tokens():
    src = 'bolo("Namaste Duniya")'
    lexer = Lexer(src)
    tokens = lexer.tokenize()

    # Expected: BOLO, LPAREN, STRING, RPAREN, EOF
    assert len(tokens) == 5
    assert tokens[0].type == TokenType.BOLO
    assert tokens[1].type == TokenType.LPAREN
    assert tokens[2].type == TokenType.STRING
    assert tokens[2].value == "Namaste Duniya"
    assert tokens[3].type == TokenType.RPAREN
    assert tokens[4].type == TokenType.EOF


def test_numbers():
    src = "123 45.67 0x1A 0b1010 0o75"
    lexer = Lexer(src)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.INT
    assert tokens[0].value == "123"

    assert tokens[1].type == TokenType.FLOAT
    assert tokens[1].value == "45.67"

    assert tokens[2].type == TokenType.INT
    assert tokens[2].value == "0x1A"

    assert tokens[3].type == TokenType.INT
    assert tokens[3].value == "0b1010"

    assert tokens[4].type == TokenType.INT
    assert tokens[4].value == "0o75"


def test_indentation():
    src = 'agar sahi:\n    bolo("sahi")\n'
    lexer = Lexer(src)
    tokens = lexer.tokenize()

    types = [t.type for t in tokens]
    # Expect: AGAR, SAHI, COLON, NEWLINE, INDENT, BOLO, LPAREN, STRING, RPAREN, NEWLINE, DEDENT, EOF
    assert TokenType.INDENT in types
    assert TokenType.DEDENT in types
    assert types[-1] == TokenType.EOF


def test_comments():
    # Verify that single line (# and //) and block comments (/* */) are correctly skipped
    src = "# this is a python-style comment\n// this is a C/JS style comment\n/* and this is a\nmultiline block comment */\nx = 10"
    lexer = Lexer(src)
    tokens = lexer.tokenize()

    # Filter out layout tokens for checking
    filtered_tokens = [t for t in tokens if t.type != TokenType.NEWLINE]

    # Expected: IDENTIFIER (x), ASSIGN (=), INT (10), EOF
    assert len(filtered_tokens) == 4
    assert filtered_tokens[0].type == TokenType.IDENTIFIER
    assert filtered_tokens[0].value == "x"
    assert filtered_tokens[1].type == TokenType.ASSIGN
    assert filtered_tokens[2].type == TokenType.INT
    assert filtered_tokens[2].value == "10"


def test_string_escapes():
    src = '"hello\\nworld\\tunicode\\u2615"'
    lexer = Lexer(src)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello\nworld\tunicode☕"


@pytest.mark.parametrize(
    "src",
    [
        '"\\u12"',  # truncated \u escape (source ends early)
        '"\\x1"',  # truncated \x escape (source ends early)
        '"\\uZZZZ"',  # \u with non-hex digits
        '"\\xZZ"',  # \x with non-hex digits
    ],
)
def test_malformed_unicode_escape_raises_lexer_error(src):
    # Malformed \u / \x escapes must surface as a LexerError, not an
    # unhandled IndexError/ValueError from the interpreter internals.
    with pytest.raises(LexerError):
        Lexer(src).tokenize()


@pytest.mark.parametrize(
    ("src", "message"),
    [
        ("0x", "Invalid hexadecimal literal: '0x'"),
        ("0x_", "Invalid hexadecimal literal: '0x_'"),
        ("0xZZ", "Invalid hexadecimal literal: '0xZZ'"),
        ("0xFFg", "Invalid hexadecimal literal: '0xFFg'"),
        ("0o", "Invalid octal literal: '0o'"),
        ("0o8", "Invalid octal literal: '0o8'"),
        ("0b", "Invalid binary literal: '0b'"),
        ("0b102", "Invalid binary literal: '0b102'"),
        ("0b2", "Invalid binary literal: '0b2'"),
        ("1e", "Invalid float literal: '1e'"),
        ("1e+", "Invalid float literal: '1e+'"),
        ("1e_", "Invalid float literal: '1e_'"),
        ("1.5_", "Invalid float literal: '1.5_'"),
        ("1e5x", "Invalid float literal: '1e5x'"),
        ("1_", "Invalid decimal literal: '1_'"),
        ("1__2", "Invalid decimal literal: '1__2'"),
    ],
)
def test_malformed_number_literal_raises_lexer_error(src, message):
    with pytest.raises(LexerError) as excinfo:
        Lexer(src).tokenize()
    assert str(excinfo.value) == message
    # The reported location is the start of the literal, not the end of the
    # run that was consumed while scanning it.
    assert excinfo.value.line == 1
    assert excinfo.value.col == 1


def test_malformed_number_reports_column_inside_statement():
    with pytest.raises(LexerError) as excinfo:
        Lexer("x = 0b102").tokenize()
    assert str(excinfo.value) == "Invalid binary literal: '0b102'"
    assert excinfo.value.line == 1
    assert excinfo.value.col == 5
    assert excinfo.value.source_line == "x = 0b102"


@pytest.mark.parametrize(
    "src",
    [
        "123",
        "45.67",
        "0x1A",
        "0x_FF",
        "0b1010",
        "0b_101",
        "0o75",
        "0o_755",
        "1e-3",
        "1E+3",
        "1_000_000",
        "1_000.000_1",
        "1e1_0",
        ".5",
        "1.",
        "1.e5",
    ],
)
def test_valid_number_literals_still_tokenize(src):
    tokens = Lexer(src).tokenize()
    number_tokens = [
        t for t in tokens if t.type in (TokenType.INT, TokenType.FLOAT)
    ]
    assert len(number_tokens) == 1
    assert number_tokens[0].value.replace("_", "") == src.replace("_", "")


def test_number_followed_by_keyword_still_tokenizes():
    # `2ya 3` used to work without a space and must keep working, so plain
    # integers do not swallow the following keyword the way malformed floats
    # and based literals do.
    tokens = Lexer("2ya 3").tokenize()
    types = [t.type for t in tokens]
    assert TokenType.INT in types
    assert TokenType.YA in types

