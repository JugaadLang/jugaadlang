"""
JugaadLang Lexer — Tokenizes .jug source code.

Supports:
  - Full indentation tracking (INDENT/DEDENT like Python)
  - JugaadLang keywords + English interop keywords
  - # line comments, // line comments, /* block comments */
  - Single/double/triple-quoted strings, f-strings
  - Integer literals: decimal, hex (0x), octal (0o), binary (0b), underscores
  - Float literals with optional exponent
  - All operators including **, //, ->, :=, ==, !=, <=, >=
  - Full Unicode + emoji support in identifiers and strings
"""

from __future__ import annotations

from typing import Iterator

from .tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    """Raised when the lexer encounters unexpected input."""

    def __init__(self, message: str, line: int, col: int, source_line: str = ""):
        super().__init__(message)
        self.line = line
        self.col = col
        self.source_line = source_line


# ─────────────────────────────────────────────────────────────────────────────
#  Character helpers
# ─────────────────────────────────────────────────────────────────────────────


def _is_id_start(ch: str) -> bool:
    """Can this character start an identifier?"""
    return ch.isalpha() or ch == "_" or (ord(ch) > 127)


def _is_id_cont(ch: str) -> bool:
    """Can this character continue an identifier?"""
    return ch.isalnum() or ch == "_" or (ord(ch) > 127)


# ─────────────────────────────────────────────────────────────────────────────
#  Lexer
# ─────────────────────────────────────────────────────────────────────────────


class Lexer:
    """
    JugaadLang tokenizer.

    Usage::

        lexer = Lexer(source_code, filename="hello.jug")
        tokens = lexer.tokenize()
    """

    def __init__(self, source: str, filename: str = "<stdin>") -> None:
        # Normalise line endings
        self.source: str = source.replace("\r\n", "\n").replace("\r", "\n")
        self.filename: str = filename
        self._pos: int = 0
        self._line: int = 1
        self._col: int = 1
        # Stack of indentation levels; starts with 0
        self._indent_stack: list[int] = [0]
        self._source_lines: list[str] = self.source.splitlines()

    # ── Public API ────────────────────────────────────────────────────

    def tokenize(self) -> list[Token]:
        """Return the full token list for the source."""
        from ..events.bus import event_bus
        event_bus.emit("LEXING_STARTED", {"filename": self.filename, "source_length": len(self.source)})
        tokens = list(self._generate())
        event_bus.emit("LEXING_COMPLETED", {"filename": self.filename, "token_count": len(tokens)})
        return tokens

    # ── Internal helpers ──────────────────────────────────────────────

    def _current(self) -> str:
        if self._pos < len(self.source):
            return self.source[self._pos]
        return ""

    def _peek(self, offset: int = 1) -> str:
        idx = self._pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return ""

    def _advance(self) -> str:
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
        idx = line - 1
        if 0 <= idx < len(self._source_lines):
            return self._source_lines[idx]
        return ""

    def _error(self, msg: str) -> LexerError:
        return LexerError(msg, self._line, self._col, self._source_line_at(self._line))

    # ── Main generator ────────────────────────────────────────────────

    def _generate(self) -> Iterator[Token]:
        """
        Core token generator.

        Algorithm:
          1. At each line start, compute indentation and emit INDENT/DEDENT.
          2. Skip whitespace (not newlines).
          3. Dispatch to individual scan methods.
          4. Emit NEWLINE at end of logical lines.
          5. Emit EOF at the end.
        """
        at_line_start = True

        while self._pos < len(self.source):
            line, col = self._line, self._col
            ch = self._current()

            # ── Handle line start (indentation) ───────────────────
            if at_line_start:
                # Count leading spaces/tabs
                indent_level = 0
                while self._pos < len(self.source) and self.source[self._pos] in (" ", "\t"):
                    if self.source[self._pos] == "\t":
                        indent_level = (indent_level // 8 + 1) * 8
                    else:
                        indent_level += 1
                    self._pos += 1
                    self._col += 1

                # Blank or comment-only line — skip
                cur = self._current()
                if cur == "\n" or cur == "" or (cur == "#") or (cur == "/" and self._peek() == "/"):
                    # Still at line start if next line
                    if cur == "\n":
                        self._advance()
                    elif cur == "#":
                        while self._pos < len(self.source) and self.source[self._pos] != "\n":
                            self._advance()
                        if self._current() == "\n":
                            self._advance()
                    elif cur == "/" and self._peek() == "/":
                        while self._pos < len(self.source) and self.source[self._pos] != "\n":
                            self._advance()
                        if self._current() == "\n":
                            self._advance()
                    # remain at_line_start = True
                    continue

                # Emit INDENT / DEDENT
                prev = self._indent_stack[-1]
                if indent_level > prev:
                    self._indent_stack.append(indent_level)
                    yield self._make(TokenType.INDENT, "", line, 1)
                elif indent_level < prev:
                    while self._indent_stack[-1] > indent_level:
                        self._indent_stack.pop()
                        yield self._make(TokenType.DEDENT, "", line, 1)
                    if self._indent_stack[-1] != indent_level:
                        raise self._error("Indentation galat hai bhai!")

                at_line_start = False
                continue  # Re-enter loop to process the actual token

            # ── Newline ───────────────────────────────────────────
            if ch == "\n":
                self._advance()
                yield self._make(TokenType.NEWLINE, "\n", line, col)
                at_line_start = True
                continue

            # ── Skip horizontal whitespace ────────────────────────
            if ch in (" ", "\t", "\r"):
                self._advance()
                continue

            # ── Comments ──────────────────────────────────────────
            if ch == "#":
                self._scan_line_comment()
                # Don't emit COMMENT tokens — just skip
                continue

            if ch == "/" and self._peek() == "/":
                self._scan_line_comment_slash()
                continue

            if ch == "/" and self._peek() == "*":
                self._scan_block_comment()
                continue

            # ── Strings ───────────────────────────────────────────
            if ch in ('"', "'") or (ch == "f" and self._peek() in ('"', "'")):
                tok = self._scan_string(line, col)
                yield tok
                continue

            # ── Numbers ───────────────────────────────────────────
            if ch.isdigit() or (ch == "." and self._peek().isdigit()):
                yield from self._scan_number(line, col)
                continue

            # ── Identifiers / Keywords ────────────────────────────
            if _is_id_start(ch):
                yield self._scan_identifier(line, col)
                continue

            # ── Operators & Delimiters ────────────────────────────
            tok = self._scan_operator(line, col)
            if tok:
                yield tok
                continue

            # ── Unknown character ─────────────────────────────────
            raise self._error(f"Ye character kya hai bhai: {ch!r}")

        # ── End of source: close open indents ─────────────────────
        while len(self._indent_stack) > 1:
            self._indent_stack.pop()
            yield self._make(TokenType.DEDENT, "", self._line, self._col)

        yield self._make(TokenType.EOF, "", self._line, self._col)

    # ── Comment scanners ──────────────────────────────────────────────

    def _scan_line_comment(self) -> str:
        start = self._pos
        while self._pos < len(self.source) and self.source[self._pos] != "\n":
            self._pos += 1
            self._col += 1
        return self.source[start : self._pos]

    def _scan_line_comment_slash(self) -> None:
        # Skip "//"
        self._advance()
        self._advance()
        while self._pos < len(self.source) and self.source[self._pos] != "\n":
            self._advance()

    def _scan_block_comment(self) -> None:
        # Skip "/*"
        line, col = self._line, self._col
        self._advance()
        self._advance()
        while self._pos < len(self.source):
            if self.source[self._pos] == "*" and self._peek() == "/":
                self._advance()
                self._advance()
                return
            self._advance()
        raise LexerError("Block comment band nahi hua (*/ missing)", line, col)

    # ── String scanner ────────────────────────────────────────────────

    def _scan_string(self, line: int, col: int) -> Token:
        is_fstring = False
        if self._current() == "f":
            is_fstring = True
            self._advance()

        quote_char = self._advance()  # ' or "
        triple = False

        # Check for triple quote
        if self._current() == quote_char and self._peek() == quote_char:
            self._advance()
            self._advance()
            triple = True

        buf: list[str] = []
        while True:
            if self._pos >= len(self.source):
                raise LexerError(
                    "String khatam nahi hua (closing quote missing)",
                    line,
                    col,
                    self._source_line_at(line),
                )

            ch = self.source[self._pos]

            if triple:
                if (
                    ch == quote_char
                    and self._pos + 1 < len(self.source)
                    and self.source[self._pos + 1] == quote_char
                    and self._pos + 2 < len(self.source)
                    and self.source[self._pos + 2] == quote_char
                ):
                    self._advance()
                    self._advance()
                    self._advance()
                    break
            else:
                if ch == quote_char:
                    self._advance()
                    break
                if ch == "\n":
                    raise LexerError(
                        "Single-line string mein newline nahi dal sakte",
                        line,
                        col,
                        self._source_line_at(line),
                    )

            if ch == "\\":
                self._advance()
                esc = self._advance()
                escape_map = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "\\": "\\",
                    "'": "'",
                    '"': '"',
                    "0": "\0",
                    "a": "\a",
                    "b": "\b",
                    "f": "\f",
                    "v": "\v",
                }
                if esc in escape_map:
                    buf.append(escape_map[esc])
                elif esc == "u":
                    # \uXXXX
                    buf.append(self._scan_hex_escape(4, "u", line, col))
                elif esc == "x":
                    # \xXX
                    buf.append(self._scan_hex_escape(2, "x", line, col))
                else:
                    buf.append("\\")
                    buf.append(esc)
            else:
                buf.append(self._advance())

        raw = "".join(buf)
        ttype = TokenType.FSTRING if is_fstring else TokenType.STRING
        return self._make(ttype, raw, line, col)

    def _scan_hex_escape(self, n_digits: int, esc_char: str, line: int, col: int) -> str:
        """Read `n_digits` hex digits for a \\u or \\x escape and return the decoded char.

        Raises a proper LexerError (instead of letting IndexError/ValueError from
        truncated or malformed escapes propagate as raw Python exceptions) when the
        source ends early or the digits aren't valid hex.
        """
        hex_chars = ""
        for _ in range(n_digits):
            if self._pos >= len(self.source):
                raise LexerError(
                    f"String khatam nahi hua (\\{esc_char} escape adhoora hai, "
                    f"{n_digits} hex digits chahiye)",
                    line,
                    col,
                    self._source_line_at(line),
                )
            hex_chars += self._advance()

        try:
            return chr(int(hex_chars, 16))
        except ValueError:
            raise LexerError(
                f"Galat \\{esc_char} escape sequence: {hex_chars!r} "
                f"({n_digits} hex digits hone chahiye)",
                line,
                col,
                self._source_line_at(line),
            ) from None

    # ── Number scanner ────────────────────────────────────────────────

    def _scan_number(self, line: int, col: int) -> Iterator[Token]:
        start = self._pos
        is_float = False

        if self._current() == "0" and self._peek() in ("x", "X"):
            # Hex
            self._advance()
            self._advance()
            while self._pos < len(self.source) and (
                self.source[self._pos] in "0123456789abcdefABCDEF_"
            ):
                self._advance()
            yield self._make(
                TokenType.INT, self.source[start : self._pos].replace("_", ""), line, col
            )
            return

        if self._current() == "0" and self._peek() in ("o", "O"):
            # Octal
            self._advance()
            self._advance()
            while self._pos < len(self.source) and self.source[self._pos] in "01234567_":
                self._advance()
            yield self._make(
                TokenType.INT, self.source[start : self._pos].replace("_", ""), line, col
            )
            return

        if self._current() == "0" and self._peek() in ("b", "B"):
            # Binary
            self._advance()
            self._advance()
            while self._pos < len(self.source) and self.source[self._pos] in "01_":
                self._advance()
            yield self._make(
                TokenType.INT, self.source[start : self._pos].replace("_", ""), line, col
            )
            return

        # Decimal / float
        while self._pos < len(self.source) and (
            self.source[self._pos].isdigit() or self.source[self._pos] == "_"
        ):
            self._advance()

        if self._pos < len(self.source) and self.source[self._pos] == "." and self._peek() != ".":
            is_float = True
            self._advance()
            while self._pos < len(self.source) and (
                self.source[self._pos].isdigit() or self.source[self._pos] == "_"
            ):
                self._advance()

        # Optional exponent
        if self._pos < len(self.source) and self.source[self._pos] in ("e", "E"):
            is_float = True
            self._advance()
            if self._pos < len(self.source) and self.source[self._pos] in ("+", "-"):
                self._advance()
            while self._pos < len(self.source) and self.source[self._pos].isdigit():
                self._advance()

        raw = self.source[start : self._pos].replace("_", "")
        ttype = TokenType.FLOAT if is_float else TokenType.INT
        yield self._make(ttype, raw, line, col)

    # ── Identifier / keyword scanner ──────────────────────────────────

    def _scan_identifier(self, line: int, col: int) -> Token:
        start = self._pos
        while self._pos < len(self.source) and _is_id_cont(self.source[self._pos]):
            self._advance()
        word = self.source[start : self._pos]
        ttype = KEYWORDS.get(word, TokenType.IDENTIFIER)
        return self._make(ttype, word, line, col)

    # ── Operator / delimiter scanner ──────────────────────────────────

    def _scan_operator(self, line: int, col: int) -> Token | None:
        ch = self._current()

        def adv1(t: TokenType, v: str) -> Token:
            self._advance()
            return self._make(t, v, line, col)

        def adv2(t: TokenType, v: str) -> Token:
            self._advance()
            self._advance()
            return self._make(t, v, line, col)

        def adv3(t: TokenType, v: str) -> Token:
            self._advance()
            self._advance()
            self._advance()
            return self._make(t, v, line, col)

        # Two-char then three-char operators first
        three = self.source[self._pos : self._pos + 3]
        two = self.source[self._pos : self._pos + 2]

        three_map = {
            "**=": TokenType.DOUBLESTAR_ASSIGN,
            "//=": TokenType.DOUBLESLASH_ASSIGN,
            "<<=": TokenType.LSHIFT_ASSIGN,
            ">>=": TokenType.RSHIFT_ASSIGN,
            "...": TokenType.ELLIPSIS,
        }
        if three in three_map:
            return adv3(three_map[three], three)

        two_map = {
            "==": TokenType.EQ,
            "!=": TokenType.NEQ,
            "<=": TokenType.LTE,
            ">=": TokenType.GTE,
            "**": TokenType.DOUBLESTAR,
            "//": TokenType.DOUBLESLASH,
            "->": TokenType.ARROW,
            ":=": TokenType.WALRUS,
            "+=": TokenType.PLUS_ASSIGN,
            "-=": TokenType.MINUS_ASSIGN,
            "*=": TokenType.STAR_ASSIGN,
            "/=": TokenType.SLASH_ASSIGN,
            "%=": TokenType.PERCENT_ASSIGN,
            "@=": TokenType.AT_ASSIGN,
            "&=": TokenType.AMP_ASSIGN,
            "|=": TokenType.PIPE_ASSIGN,
            "^=": TokenType.CARET_ASSIGN,
            "<<": TokenType.LSHIFT,
            ">>": TokenType.RSHIFT,
        }
        if two in two_map:
            return adv2(two_map[two], two)

        one_map = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
            "%": TokenType.PERCENT,
            "=": TokenType.ASSIGN,
            "<": TokenType.LT,
            ">": TokenType.GT,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            "[": TokenType.LBRACKET,
            "]": TokenType.RBRACKET,
            "{": TokenType.LBRACE,
            "}": TokenType.RBRACE,
            ",": TokenType.COMMA,
            ".": TokenType.DOT,
            ":": TokenType.COLON,
            ";": TokenType.SEMICOLON,
            "@": TokenType.AT,
            "~": TokenType.TILDE,
            "&": TokenType.AMP,
            "|": TokenType.PIPE,
            "^": TokenType.CARET,
        }
        if ch in one_map:
            return adv1(one_map[ch], ch)

        return None
