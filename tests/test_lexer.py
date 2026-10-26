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


def test_leading_bom_is_ignored():
    plain = 'bolo("hello")\nx = 1\n'
    with_bom = "\ufeff" + plain

    plain_tokens = Lexer(plain).tokenize()
    bom_tokens = Lexer(with_bom).tokenize()

    assert [(t.type, t.value, t.line, t.col) for t in plain_tokens] == [
        (t.type, t.value, t.line, t.col) for t in bom_tokens
    ]
    assert bom_tokens[0].type == TokenType.BOLO
    assert bom_tokens[0].line == 1
    assert bom_tokens[0].col == 1


def test_bom_in_the_middle_is_rejected():
    src = 'bolo("first")\n\ufeffbolo("second")\n'
    with pytest.raises(LexerError) as exc_info:
        Lexer(src).tokenize()
    assert "BOM" in str(exc_info.value)
def test_multiline_list_has_no_layout_tokens_inside_brackets():
    src = "x = [\n    1,\n    2,\n]\n"
    tokens = Lexer(src).tokenize()

    types = [t.type for t in tokens]
    assert TokenType.INDENT not in types
    assert TokenType.DEDENT not in types
    # Only the line that closes the statement ends with a NEWLINE
    assert types.count(TokenType.NEWLINE) == 1
    values = [t.value for t in tokens if t.type == TokenType.INT]
    assert values == ["1", "2"]


def test_multiline_call_has_no_layout_tokens_inside_brackets():
    src = "bolo(\n    1,\n    2,\n)\n"
    tokens = Lexer(src).tokenize()

    types = [t.type for t in tokens]
    assert TokenType.INDENT not in types
    assert TokenType.DEDENT not in types
    assert types.count(TokenType.NEWLINE) == 1


def test_multiline_brackets_in_block_keep_indentation_balanced():
    src = "banao f():\n    x = [\n        1,\n    ]\n    wapas x\n"
    tokens = Lexer(src).tokenize()

    types = [t.type for t in tokens]
    # One INDENT for the function body and one DEDENT when it ends: the
    # bracket continuation lines must not add their own indentation tokens.
    assert types.count(TokenType.INDENT) == 1
    assert types.count(TokenType.DEDENT) == 1


def test_multiline_nested_brackets_are_tracked():
    src = "x = [\n    [\n        1,\n    ],\n    2,\n]\n"
    tokens = Lexer(src).tokenize()

    types = [t.type for t in tokens]
    assert TokenType.INDENT not in types
    assert TokenType.DEDENT not in types
    values = [t.value for t in tokens if t.type == TokenType.INT]
    assert values == ["1", "2"]

def test_octal_escapes_are_decoded():
    tokens = Lexer('"\\101\\102\\103"').tokenize()
    assert tokens[0].value == "ABC"


def test_short_octal_escapes_are_decoded():
    tokens = Lexer('"\\0\\7"').tokenize()
    assert tokens[0].value == "\x00\x07"


def test_octal_escape_uses_at_most_three_digits():
    tokens = Lexer('"\\1019"').tokenize()
    assert tokens[0].value == "A9"


def test_named_unicode_escape_is_decoded():
    tokens = Lexer('"\\N{SNOWMAN}"').tokenize()
    assert tokens[0].value == "\u2603"


def test_named_unicode_escape_is_case_insensitive():
    tokens = Lexer('"\\N{latin small letter a}"').tokenize()
    assert tokens[0].value == "a"


def test_unknown_named_unicode_escape_raises_lexer_error():
    with pytest.raises(LexerError):
        Lexer('"\\N{NOT A REAL NAME}"').tokenize()


def test_named_unicode_escape_needs_braces():
    with pytest.raises(LexerError):
        Lexer('"\\Nx"').tokenize()


def test_unclosed_named_unicode_escape_raises_lexer_error():
    with pytest.raises(LexerError):
        Lexer('"\\N{SNOWMAN"').tokenize()


def test_long_unicode_escape_is_decoded():
    tokens = Lexer('"\\U0001F600"').tokenize()
    assert tokens[0].value == "\U0001F600"


def test_malformed_long_unicode_escape_raises_lexer_error():
    with pytest.raises(LexerError):
        Lexer('"\\U0001F60"').tokenize()
