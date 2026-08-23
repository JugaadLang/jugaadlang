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
