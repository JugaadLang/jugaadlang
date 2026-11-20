
from __future__ import annotations

import unicodedata
from typing import Iterator, Optional

from .tokens import KEYWORDS, Token, TokenType


class LexerError(Exception):
    """Raised when the lexer encounters unexpected input."""

    def __init__(self, message: str, line: int, col: int, source_line: str = ""):
        super().__init__(message)
        self.line = line
        self.col = col
        self.source_line = source_line


def _is_id_start(ch: str) -> bool:
    return ch == "_" or (bool(ch) and ch.isidentifier() and not ch.isdigit())


def _is_id_cont(ch: str) -> bool:
    return ch == "_" or (bool(ch) and ("a" + ch).isidentifier())


class Lexer:
    """JugaadLang tokenizer."""

    def __init__(self, source: str, filename: str = "<stdin>") -> None:
        self.source = source.replace("\r\n", "\n").replace("\r", "\n")
        if self.source.startswith("\ufeff"):
            self.source = self.source[1:]

        self.filename = filename
        self._pos = 0
        self._line = 1
        self._col = 1
        self._indent_stack = [0]
        self._source_lines = self.source.splitlines()
        self._bracket_stack: list[tuple[str, int, int]] = []

    def _current(self) -> str:
        return self.source[self._pos] if self._pos < len(self.source) else ""

    def _peek(self, offset: int = 1) -> str:
        idx = self._pos + offset
        return self.source[idx] if idx < len(self.source) else ""

    def _advance(self) -> str:
        if self._pos >= len(self.source):
            return ""

        ch = self.source[self._pos]
        self._pos += 1

        if ch == "\n":
            self._line += 1
            self._col = 1
        else:
            self._col += 1

        return ch

    def _make(self, ttype: TokenType, value: str, line: int, col: int) -> Token:
        return Token(ttype, value, line, col)

    def _source_line_at(self, line: int) -> str:
        return self._source_lines[line - 1] if 0 < line <= len(self._source_lines) else ""

    def _error(self, message: str, line: Optional[int] = None,
               col: Optional[int] = None) -> LexerError:
        line = line or self._line
        col = col or self._col
        return LexerError(message, line, col, self._source_line_at(line))

    def tokenize(self) -> list[Token]:
        from ..events.bus import event_bus

        event_bus.emit("LEXING_STARTED", {
            "filename": self.filename,
            "source_length": len(self.source)
        })

        tokens = list(self._generate())

        event_bus.emit("LEXING_COMPLETED", {
            "filename": self.filename,
            "token_count": len(tokens)
        })
        return tokens

    def _generate(self) -> Iterator[Token]:
        at_line_start = True
        last_was_newline = True

        while self._pos < len(self.source):
            line, col = self._line, self._col
            ch = self._current()

            if at_line_start:
                if self._bracket_stack:
                    while self._current() in (" ", "\t"):
                        self._advance()
                    at_line_start = False
                    continue

                indent = 0
                while self._current() in (" ", "\t"):
                    if self._current() == "\t":
                        indent = (indent // 8 + 1) * 8
                    else:
                        indent += 1
                    self._advance()

                ch = self._current()

                if ch in ("", "\n", "#") or (ch == "/" and self._peek() == "/"):
                    if ch == "\n":
                        self._advance()
                    elif ch in ("#", "/"):
                        while self._current() not in ("", "\n"):
                            self._advance()
                        if self._current() == "\n":
                            self._advance()
                    continue

                previous = self._indent_stack[-1]

                if indent > previous:
                    self._indent_stack.append(indent)
                    yield self._make(TokenType.INDENT, "", line, 1)

                elif indent < previous:
                    while len(self._indent_stack) > 1 and self._indent_stack[-1] > indent:
                        self._indent_stack.pop()
                        yield self._make(TokenType.DEDENT, "", line, 1)

                    if self._indent_stack[-1] != indent:
                        raise self._error("Inconsistent indentation", line, col)

                at_line_start = False
                continue

            if ch == "\n":
                self._advance()
                if not self._bracket_stack:
                    yield self._make(TokenType.NEWLINE, "\n", line, col)
                    last_was_newline = True
                at_line_start = True
                continue

            if ch in (" ", "\t"):
                self._advance()
                continue

            if ch == "\ufeff":
                raise self._error("BOM is only allowed at the beginning of the source")

            if ch == "#":
                self._scan_line_comment()
                continue

            if ch == "/" and self._peek() == "/":
                self._scan_line_comment_slash()
                continue

            if ch == "/" and self._peek() == "*":
                self._scan_block_comment()
                continue

            if self._string_prefix() is not None:
                yield self._scan_string(line, col)
                last_was_newline = False
                continue

            if ch.isdigit() or (ch == "." and self._peek().isdigit()):
                yield from self._scan_number(line, col)
                last_was_newline = False
                continue

            if _is_id_start(ch):
                yield self._scan_identifier(line, col)
                last_was_newline = False
                continue

            tok = self._scan_operator(line, col)

            if tok is None:
                raise self._error(f"Unexpected character: {ch!r}", line, col)

            opening = {
                TokenType.LPAREN: ")",
                TokenType.LBRACKET: "]",
                TokenType.LBRACE: "}",
            }

            closing = {
                TokenType.RPAREN: ")",
                TokenType.RBRACKET: "]",
                TokenType.RBRACE: "}",
            }

            if tok.type in opening:
                self._bracket_stack.append((opening[tok.type], line, col))

            elif tok.type in closing:
                if not self._bracket_stack:
                    raise self._error("Unexpected closing bracket", line, col)

                expected, _, _ = self._bracket_stack[-1]
                if tok.value != expected:
                    raise self._error(
                        f"Mismatched bracket: expected {expected!r}",
                        line,
                        col
                    )
                self._bracket_stack.pop()

            yield tok
            last_was_newline = False

        if self._bracket_stack:
            expected, line, col = self._bracket_stack[-1]
            raise self._error(
                f"Unclosed bracket: expected {expected!r}",
                line,
                col
            )

        if not last_was_newline and self._pos > 0:
            yield self._make(TokenType.NEWLINE, "\n", self._line, self._col)

        while len(self._indent_stack) > 1:
            self._indent_stack.pop()
            yield self._make(TokenType.DEDENT, "", self._line, self._col)

        yield self._make(TokenType.EOF, "", self._line, self._col)

    def _scan_line_comment(self) -> None:
        while self._current() not in ("", "\n"):
            self._advance()

    def _scan_line_comment_slash(self) -> None:
        self._advance()
        self._advance()
        while self._current() not in ("", "\n"):
            self._advance()

    def _scan_block_comment(self) -> None:
        line, col = self._line, self._col
        self._advance()
        self._advance()

        while self._pos < len(self.source):
            if self._current() == "*" and self._peek() == "/":
                self._advance()
                self._advance()
                return
            self._advance()

        raise self._error("Unclosed block comment (*/ missing)", line, col)

    def _string_prefix(self) -> Optional[str]:
        pos = self._pos
        src = self.source

        if pos < len(src) and src[pos] in ("'", '"'):
            return ""

        for length in (2, 1):
            if pos + length < len(src) and src[pos + length] in ("'", '"'):
                prefix = src[pos:pos + length]
                if (
                    all(c in "ft" for c in prefix)
                    and len(set(prefix)) == len(prefix)
                ):
                    return prefix

        return None

    def _scan_string(self, line: int, col: int) -> Token:
        prefix = self._string_prefix() or ""

        if "f" in prefix and "t" in prefix:
            raise self._error("f and t prefixes cannot be combined", line, col)

        is_fstring = "f" in prefix
        is_tstring = "t" in prefix

        for _ in prefix:
            self._advance()

        quote = self._advance()
        triple = False

        if self._current() == quote and self._peek() == quote:
            self._advance()
            self._advance()
            triple = True

        result: list[str] = []

        while self._pos < len(self.source):
            ch = self._current()

            if triple:
                if (
                    ch == quote
                    and self._peek() == quote
                    and self._peek(2) == quote
                ):
                    self._advance()
                    self._advance()
                    self._advance()
                    break
            else:
                if ch == quote:
                    self._advance()
                    break
                if ch == "\n":
                    raise self._error("Newline inside single-line string", line, col)

            if ch == "\\":
                self._advance()
                esc = self._current()

                if not esc:
                    raise self._error("Incomplete string escape", line, col)

                self._advance()

                escapes = {
                    "n": "\n", "t": "\t", "r": "\r",
                    "\\": "\\", "'": "'", '"': '"',
                    "a": "\a", "b": "\b", "f": "\f", "v": "\v",
                }

                if esc in escapes:
                    result.append(escapes[esc])

                elif esc in "01234567":
                    digits = esc
                    for _ in range(2):
                        if self._current() in "01234567":
                            digits += self._advance()
                        else:
                            break
                    result.append(chr(int(digits, 8)))

                elif esc in ("x", "u", "U"):
                    count = {"x": 2, "u": 4, "U": 8}[esc]
                    result.append(self._scan_hex_escape(count, esc, line, col))

                elif esc == "N":
                    result.append(self._scan_named_escape(line, col))

                elif esc == "\n":
                    continue

                else:
                    result.extend(("\\", esc))

            else:
                result.append(self._advance())

        else:
            raise self._error("Unterminated string", line, col)

        token_type = (
            TokenType.TSTRING if is_tstring
            else TokenType.FSTRING if is_fstring
            else TokenType.STRING
        )

        return self._make(token_type, "".join(result), line, col)

    def _scan_hex_escape(self, count: int, esc: str,
                         line: int, col: int) -> str:
        digits = ""

        for _ in range(count):
            ch = self._current()
            if not ch or ch not in "0123456789abcdefABCDEF":
                raise self._error(f"Invalid \\{esc} escape", line, col)
            digits += self._advance()

        value = int(digits, 16)

        try:
            return chr(value)
        except ValueError:
            raise self._error("Invalid Unicode code point", line, col) from None

    def _scan_named_escape(self, line: int, col: int) -> str:
        if self._current() != "{":
            raise self._error("Expected { after \\N", line, col)

        self._advance()
        chars = []

        while self._pos < len(self.source) and self._current() != "}":
            chars.append(self._advance())

        if self._current() != "}":
            raise self._error("Unclosed Unicode character name", line, col)

        self._advance()
        name = "".join(chars)

        try:
            return unicodedata.lookup(name)
        except KeyError:
            raise self._error(f"Unknown Unicode character: {name}", line, col) from None

    def _scan_number(self, line: int, col: int) -> Iterator[Token]:
        start = self._pos
        is_float = False

        if self._current() == "0" and self._peek() in "xXoObB":
            prefix = self._peek().lower()
            self._advance()
            self._advance()

            allowed = {
                "x": "0123456789abcdefABCDEF",
                "o": "01234567",
                "b": "01",
            }[prefix]

            digits = 0
            previous_underscore = False

            while self._current():
                ch = self._current()

                if ch == "_":
                    if digits == 0 or previous_underscore:
                        raise self._error("Invalid underscore in number", line, col)
                    previous_underscore = True
                    self._advance()

                elif ch in allowed:
                    digits += 1
                    previous_underscore = False
                    self._advance()

                else:
                    break

            if digits == 0 or previous_underscore:
                raise self._error("Invalid integer literal", line, col)

            raw = self.source[start:self._pos].replace("_", "")
            yield self._make(TokenType.INT, raw, line, col)
            return

        digits = 0
        previous_underscore = False

        while self._current().isdigit() or self._current() == "_":
            ch = self._advance()

            if ch == "_":
                if digits == 0 or previous_underscore:
                    raise self._error("Invalid underscore in number", line, col)
                previous_underscore = True
            else:
                digits += 1
                previous_underscore = False

        if previous_underscore:
            raise self._error("Number cannot end with underscore", line, col)

        if self._current() == "." and self._peek() != ".":
            is_float = True
            self._advance()

            while self._current().isdigit() or self._current() == "_":
                ch = self._advance()
                if ch == "_":
                    if previous_underscore:
                        raise self._error("Invalid underscore in number", line, col)
                    previous_underscore = True
                else:
                    previous_underscore = False

            if previous_underscore:
                raise self._error("Number cannot end with underscore", line, col)

        if self._current() in ("e", "E"):
            is_float = True
            self._advance()

            if self._current() in ("+", "-"):
                self._advance()

            exp_start = self._pos
            while self._current().isdigit():
                self._advance()

            if self._pos == exp_start:
                raise self._error("Exponent requires digits", line, col)

        if _is_id_start(self._current()):
            raise self._error("Invalid character after number", line, col)

        raw = self.source[start:self._pos].replace("_", "")
        yield self._make(
            TokenType.FLOAT if is_float else TokenType.INT,
            raw,
            line,
            col
        )

    def _scan_identifier(self, line: int, col: int) -> Token:
        start = self._pos

        while self._current() and _is_id_cont(self._current()):
            self._advance()

        word = self.source[start:self._pos]
        return self._make(KEYWORDS.get(word, TokenType.IDENTIFIER), word, line, col)

    def _scan_operator(self, line: int, col: int) -> Optional[Token]:
        three = self.source[self._pos:self._pos + 3]
        two = self.source[self._pos:self._pos + 2]
        ch = self._current()

        three_map = {
            "**=": TokenType.DOUBLESTAR_ASSIGN,
            "//=": TokenType.DOUBLESLASH_ASSIGN,
            "<<=": TokenType.LSHIFT_ASSIGN,
            ">>=": TokenType.RSHIFT_ASSIGN,
            "...": TokenType.ELLIPSIS,
        }

        two_map = {
            "==": TokenType.EQ, "!=": TokenType.NEQ,
            "<=": TokenType.LTE, ">=": TokenType.GTE,
            "**": TokenType.DOUBLESTAR, "//": TokenType.DOUBLESLASH,
            "->": TokenType.ARROW, ":=": TokenType.WALRUS,
            "+=": TokenType.PLUS_ASSIGN, "-=": TokenType.MINUS_ASSIGN,
            "*=": TokenType.STAR_ASSIGN, "/=": TokenType.SLASH_ASSIGN,
            "%=": TokenType.PERCENT_ASSIGN, "@=": TokenType.AT_ASSIGN,
            "&=": TokenType.AMP_ASSIGN, "|=": TokenType.PIPE_ASSIGN,
            "^=": TokenType.CARET_ASSIGN, "<<": TokenType.LSHIFT,
            ">>": TokenType.RSHIFT,
        }

        one_map = {
            "+": TokenType.PLUS, "-": TokenType.MINUS,
            "*": TokenType.STAR, "/": TokenType.SLASH,
            "%": TokenType.PERCENT, "=": TokenType.ASSIGN,
            "<": TokenType.LT, ">": TokenType.GT,
            "(": TokenType.LPAREN, ")": TokenType.RPAREN,
            "[": TokenType.LBRACKET, "]": TokenType.RBRACKET,
            "{": TokenType.LBRACE, "}": TokenType.RBRACE,
            ",": TokenType.COMMA, ".": TokenType.DOT,
            ":": TokenType.COLON, ";": TokenType.SEMICOLON,
            "@": TokenType.AT, "~": TokenType.TILDE,
            "&": TokenType.AMP, "|": TokenType.PIPE,
            "^": TokenType.CARET,
        }

        if three in three_map:
            value, token_type = three, three_map[three]
        elif two in two_map:
            value, token_type = two, two_map[two]
        elif ch in one_map:
            value, token_type = ch, one_map[ch]
        else:
            return None

        for _ in value:
            self._advance()

        return self._make(token_type, value, line, col)

