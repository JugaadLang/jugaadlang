"""
JugaadLang Parser — Parses token stream into JugaadLang AST.
Uses recursive descent with precedence climb.
"""

from __future__ import annotations

from ..lexer.tokens import Token, TokenType
from ..ast_nodes.nodes import (
    Module,
    Stmt,
    Expr,
    FunctionDef,
    ClassDef,
    Return,
    Delete,
    Assign,
    AugAssign,
    AnnAssign,
    For,
    While,
    If,
    With,
    Raise,
    Try,
    Assert,
    Import,
    ImportFrom,
    Global,
    Nonlocal,
    ExprStmt,
    Pass,
    Break,
    Continue,
    PoochhoStmt,
    BoolOp,
    BinOp,
    UnaryOp,
    Lambda,
    IfExp,
    Dict,
    Set,
    ListComp,
    SetComp,
    DictComp,
    GeneratorExp,
    Await,
    Compare,
    Call,
    FormattedValue,
    JoinedStr,
    Constant,
    Attribute,
    Subscript,
    Name,
    List,
    Tuple,
    Slice,
    comprehension,
    arg,
    arguments,
    keyword,
    alias,
    withitem,
    ExceptHandler,
    Match,
    match_case,
    Pattern,
    MatchValue,
    MatchSingleton,
    MatchAs,
    MatchOr,
    MatchSequence,
    MatchMapping,
    MatchClass,
)


class ParseError(Exception):
    """Raised when parser encounters syntactically invalid source."""

    def __init__(self, message: str, line: int, col: int, source_line: str = ""):
        super().__init__(message)
        self.line = line
        self.col = col
        self.source_line = source_line


class Parser:
    """
    Parses a list of tokens into a JugaadLang AST.
    """

    def __init__(self, tokens: list[Token], filename: str = "<stdin>", source: str = "") -> None:
        self._tokens = tokens
        self._filename = filename
        self._source_lines = source.splitlines() if source else []
        self._current = 0

    # ── Public API ────────────────────────────────────────────────────

    def parse(self) -> Module:
        """Parse the entire token stream into a Module AST node."""
        from ..events.bus import event_bus
        event_bus.emit("PARSING_STARTED", {"filename": self._filename, "token_count": len(self._tokens)})
        body = []
        try:
            while not self._check(TokenType.EOF):
                # Skip any leading empty lines
                while self._match(TokenType.NEWLINE):
                    pass
                if self._check(TokenType.EOF):
                    break
                body.append(self.parse_statement())
            self._expect(TokenType.EOF, "Expected end of file")
        except ParseError:
            raise
        except Exception as e:
            # Wrap standard exceptions to prevent compiler crash
            curr = self._current_token()
            raise ParseError(f"Parser error occurred: {str(e)}", curr.line, curr.col)

        event_bus.emit("PARSING_COMPLETED", {"filename": self._filename, "node_count": len(body)})
        return Module(body=body, line=1, col=1)

    # ── Token Navigation Helpers ──────────────────────────────────────

    def _current_token(self) -> Token:
        if self._current < len(self._tokens):
            return self._tokens[self._current]
        return self._tokens[-1]

    def _previous_token(self) -> Token:
        if self._current > 0:
            return self._tokens[self._current - 1]
        return self._tokens[0]

    def _peek(self, offset: int = 1) -> Token:
        idx = self._current + offset
        if idx < len(self._tokens):
            return self._tokens[idx]
        return self._tokens[-1]

    def _check(self, *types: TokenType) -> bool:
        return self._current_token().type in types

    def _match(self, *types: TokenType) -> bool:
        if self._check(*types):
            self._advance()
            return True
        return False

    def _advance(self) -> Token:
        tok = self._current_token()
        if not self._check(TokenType.EOF):
            self._current += 1
        return tok

    def _expect(self, ttype: TokenType, msg: str) -> Token:
        if self._check(ttype):
            return self._advance()
        raise self._error(msg)

    def _source_line_at(self, line: int) -> str:
        idx = line - 1
        if 0 <= idx < len(self._source_lines):
            return self._source_lines[idx]
        return ""

    def _error(self, msg: str) -> ParseError:
        tok = self._current_token()
        return ParseError(msg, tok.line, tok.col, self._source_line_at(tok.line))

    def _expect_newline_or_eof(self) -> None:
        if self._match(TokenType.NEWLINE):
            return
        elif self._check(TokenType.EOF, TokenType.DEDENT):
            return
        elif self._match(TokenType.SEMICOLON):
            return
        else:
            raise self._error(
                f"Expected newline or semicolon, but got: {self._current_token().value!r}"
            )

    # ── Statement Parsing ─────────────────────────────────────────────

    def parse_statement(self) -> Stmt:
        # Skip leading newlines
        while self._match(TokenType.NEWLINE):
            pass

        # Handle decorators
        if self._check(TokenType.AT):
            return self.parse_decorated_stmt()

        # Dispatch based on statement keywords
        if self._check(TokenType.BANAO):
            return self.parse_function_def(is_async=False)
        elif self._check(TokenType.TEZ):
            self._advance()
            if self._check(TokenType.BANAO):
                return self.parse_function_def(is_async=True)
            elif self._check(TokenType.GHUMO):
                return self.parse_for(is_async=True)
            else:
                raise self._error("Expected 'banao' or 'ghumo' after 'tez'")
        elif self._check(TokenType.USTAD):
            return self.parse_class_def()
        elif self._check(TokenType.WAPAS):
            return self.parse_return()
        elif self._check(TokenType.DEL):
            return self.parse_delete()
        elif self._check(TokenType.GHUMO):
            return self.parse_for(is_async=False)
        elif self._check(TokenType.JABTAK):
            return self.parse_while()
        elif self._check(TokenType.AGAR):
            return self.parse_if()
        elif self._check(TokenType.AGAR_MATCH):
            return self.parse_match()
        elif self._check(TokenType.KOSHISH):
            return self.parse_try()
        elif self._check(TokenType.UDAO):
            return self.parse_raise()
        elif self._check(TokenType.LAO):
            return self.parse_import()
        elif self._check(TokenType.SE):
            return self.parse_import_from()
        elif self._check(TokenType.SABKA):
            return self.parse_global()
        elif self._check(TokenType.NONLOCAL):
            return self.parse_nonlocal()
        elif self._check(TokenType.THEEK_HAI):
            tok = self._advance()
            self._expect_newline_or_eof()
            return Pass(line=tok.line, col=tok.col)
        elif self._check(TokenType.RUKJA):
            tok = self._advance()
            self._expect_newline_or_eof()
            return Break(line=tok.line, col=tok.col)
        elif self._check(TokenType.CHALTE_RAHO):
            tok = self._advance()
            self._expect_newline_or_eof()
            return Continue(line=tok.line, col=tok.col)
        elif self._check(TokenType.ASSERT):
            return self.parse_assert()
        elif self._check(TokenType.WITH):
            return self.parse_with()
        elif self._check(TokenType.POOCHHO):
            # poochho name (special form: name = poochho())
            # We differentiate this from poochho(expr) inside an expression statement.
            if self._peek().type == TokenType.IDENTIFIER:
                tok = self._advance()  # consume POOCHHO
                id_tok = self._advance()  # consume IDENTIFIER
                self._expect_newline_or_eof()
                name_node = Name(id=id_tok.value, line=id_tok.line, col=id_tok.col)
                return PoochhoStmt(target=name_node, line=tok.line, col=tok.col)

        # Fallback to expression statement or assignment
        return self.parse_expr_statement_or_assignment()

    def parse_decorated_stmt(self) -> Stmt:
        decorators = []
        while self._match(TokenType.AT):
            # Parse decorator name/call (e.g. @app.route("/") or @classmethod)
            dec = self.parse_primary()
            decorators.append(dec)
            self._expect_newline_or_eof()
            while self._match(TokenType.NEWLINE):
                pass

        if self._check(TokenType.BANAO):
            func = self.parse_function_def(is_async=False)
            func.decorator_list = decorators
            return func
        elif self._check(TokenType.TEZ):
            self._advance()
            self._expect(TokenType.BANAO, "Expected 'banao' after 'tez'")
            func = self.parse_function_def(is_async=True)
            func.decorator_list = decorators
            return func
        elif self._check(TokenType.USTAD):
            cls = self.parse_class_def()
            cls.decorator_list = decorators
            return cls
        else:
            raise self._error("Decorated statement must be a function or class definition")

    def parse_block(self) -> list[Stmt]:
        self._expect(TokenType.COLON, "Expected ':' before block start")
        if self._match(TokenType.NEWLINE):
            self._expect(TokenType.INDENT, "Expected indented block")
            body = []
            while not self._check(TokenType.DEDENT, TokenType.EOF):
                # Skip any blank lines inside block
                while self._match(TokenType.NEWLINE):
                    pass
                if self._check(TokenType.DEDENT, TokenType.EOF):
                    break
                body.append(self.parse_statement())
            self._expect(TokenType.DEDENT, "Expected DEDENT at block end")
            return body
        else:
            # Inline statement block, e.g. "agar x == 1: y = 2"
            stmt = self.parse_statement()
            return [stmt]

    def parse_function_def(self, is_async: bool) -> FunctionDef:
        tok = self._expect(TokenType.BANAO, "Expected 'banao' for function definition")
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected function name")

        self._expect(TokenType.LPAREN, "Expected '(' after function name")
        args = self.parse_function_arguments()
        self._expect(TokenType.RPAREN, "Expected ')' after parameters")

        returns = None
        if self._match(TokenType.ARROW):
            returns = self.parse_expression()

        body = self.parse_block()
        return FunctionDef(
            name=name_tok.value,
            args=args,
            body=body,
            decorator_list=[],
            returns=returns,
            is_async=is_async,
            line=tok.line,
            col=tok.col,
        )

    def parse_function_arguments(self) -> arguments:
        tok = self._current_token()
        args = []
        defaults = []
        vararg = None
        kwarg = None

        while not self._check(TokenType.RPAREN, TokenType.EOF):
            if self._match(TokenType.STAR):
                # *args
                arg_tok = self._expect(TokenType.IDENTIFIER, "Expected identifier after '*'")
                annotation = None
                if self._match(TokenType.COLON):
                    annotation = self.parse_expression()
                vararg = arg(
                    arg=arg_tok.value, annotation=annotation, line=arg_tok.line, col=arg_tok.col
                )
            elif self._match(TokenType.DOUBLESTAR):
                # **kwargs
                arg_tok = self._expect(TokenType.IDENTIFIER, "Expected identifier after '**'")
                annotation = None
                if self._match(TokenType.COLON):
                    annotation = self.parse_expression()
                kwarg = arg(
                    arg=arg_tok.value, annotation=annotation, line=arg_tok.line, col=arg_tok.col
                )
            else:
                # Regular parameter (or 'khud')
                p_name = ""
                p_line, p_col = 0, 0
                if self._match(TokenType.KHUD):
                    p_name = "self"
                    p_line, p_col = self._previous_token().line, self._previous_token().col
                else:
                    arg_tok = self._expect(TokenType.IDENTIFIER, "Expected parameter name")
                    p_name = arg_tok.value
                    p_line, p_col = arg_tok.line, arg_tok.col

                annotation = None
                if self._match(TokenType.COLON):
                    annotation = self.parse_expression()

                default_val = None
                if self._match(TokenType.ASSIGN):
                    default_val = self.parse_expression()

                args.append(arg(arg=p_name, annotation=annotation, line=p_line, col=p_col))
                if default_val:
                    defaults.append(default_val)

            if not self._match(TokenType.COMMA):
                break

        return arguments(
            args=args, defaults=defaults, vararg=vararg, kwarg=kwarg, line=tok.line, col=tok.col
        )

    def parse_class_def(self) -> ClassDef:
        tok = self._expect(TokenType.USTAD, "Expected 'ustad' to define a class")
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected class name")

        bases = []
        if self._match(TokenType.LPAREN):
            while not self._check(TokenType.RPAREN, TokenType.EOF):
                bases.append(self.parse_expression())
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RPAREN, "Expected ')' after base classes")

        body = self.parse_block()
        return ClassDef(name=name_tok.value, bases=bases, body=body, line=tok.line, col=tok.col)

    def parse_return(self) -> Return:
        tok = self._expect(TokenType.WAPAS, "Expected 'wapas'")
        value = None
        if not self._check(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT):
            value = self.parse_expression()
        self._expect_newline_or_eof()
        return Return(value=value, line=tok.line, col=tok.col)

    def parse_delete(self) -> Delete:
        tok = self._expect(TokenType.DEL, "Expected 'del'")
        targets = []
        while True:
            targets.append(self.parse_expression())
            if not self._match(TokenType.COMMA):
                break
        self._expect_newline_or_eof()
        return Delete(targets=targets, line=tok.line, col=tok.col)

    def parse_for(self, is_async: bool) -> For:
        tok = self._expect(TokenType.GHUMO, "Expected 'ghumo'")
        target = self.parse_primary()
        if self._match(TokenType.COMMA):
            elts = [target]
            while True:
                elts.append(self.parse_primary())
                if not self._match(TokenType.COMMA):
                    break
            target = Tuple(elts=elts, line=target.line, col=target.col)

        self._expect(TokenType.MEIN, "Expected 'mein' after loop target variables")
        iter_expr = self.parse_expression()
        body = self.parse_block()

        orelse = []
        if self._match(TokenType.WARNA):
            orelse = self.parse_block()

        return For(
            target=target,
            iter=iter_expr,
            body=body,
            orelse=orelse,
            is_async=is_async,
            line=tok.line,
            col=tok.col,
        )

    def parse_while(self) -> While:
        tok = self._expect(TokenType.JABTAK, "Expected 'jabtak'")
        test = self.parse_expression()
        body = self.parse_block()
        orelse = []
        if self._match(TokenType.WARNA):
            orelse = self.parse_block()
        return While(test=test, body=body, orelse=orelse, line=tok.line, col=tok.col)

    def parse_if(self) -> If:
        tok = self._expect(TokenType.AGAR, "Expected 'agar'")
        test = self.parse_expression()
        body = self.parse_block()

        orelse: list[Stmt] = []
        if self._match(TokenType.SHAYAD):
            orelse = [self.parse_elif()]
        elif self._match(TokenType.WARNA):
            orelse = self.parse_block()

        return If(test=test, body=body, orelse=orelse, line=tok.line, col=tok.col)

    def parse_elif(self) -> If:
        tok = self._previous_token()
        test = self.parse_expression()
        body = self.parse_block()

        orelse: list[Stmt] = []
        if self._match(TokenType.SHAYAD):
            orelse = [self.parse_elif()]
        elif self._match(TokenType.WARNA):
            orelse = self.parse_block()

        return If(test=test, body=body, orelse=orelse, line=tok.line, col=tok.col)

    def parse_match(self) -> Match:
        tok = self._expect(TokenType.AGAR_MATCH, "Expected 'agar_match'")
        subject = self.parse_expression()
        self._expect(TokenType.COLON, "Expected ':' after agar_match subject")

        cases = []
        if self._match(TokenType.NEWLINE):
            self._expect(TokenType.INDENT, "Expected indented block after 'agar_match'")
            while not self._check(TokenType.DEDENT, TokenType.EOF):
                # Skip any blank lines inside block
                while self._match(TokenType.NEWLINE):
                    pass
                if self._check(TokenType.DEDENT, TokenType.EOF):
                    break
                cases.append(self.parse_match_case())
            self._expect(TokenType.DEDENT, "Expected DEDENT at the end of 'agar_match' block")
        else:
            cases.append(self.parse_match_case())

        return Match(subject=subject, cases=cases, line=tok.line, col=tok.col)

    def parse_match_case(self) -> match_case:
        tok = self._expect(TokenType.KAAND, "Expected 'kaand'")
        pattern = self.parse_pattern()

        guard = None
        if self._match(TokenType.AGAR):
            guard = self.parse_expression()

        body = self.parse_block()
        return match_case(pattern=pattern, guard=guard, body=body, line=tok.line, col=tok.col)

    def parse_pattern(self) -> Pattern:
        pattern = self.parse_pattern_or()
        if self._match(TokenType.AS):
            name_tok = self._expect(TokenType.IDENTIFIER, "Expected name after 'as'")
            pattern = MatchAs(
                pattern=pattern, name=name_tok.value, line=pattern.line, col=pattern.col
            )
        return pattern

    def parse_pattern_or(self) -> Pattern:
        patterns = [self.parse_pattern_primary()]
        while self._match(TokenType.PIPE):
            patterns.append(self.parse_pattern_primary())
        if len(patterns) > 1:
            return MatchOr(patterns=patterns, line=patterns[0].line, col=patterns[0].col)
        return patterns[0]

    def parse_pattern_primary(self) -> Pattern:
        if self._check(TokenType.SAHI):
            tok = self._advance()
            return MatchSingleton(value=True, line=tok.line, col=tok.col)
        elif self._check(TokenType.GALAT):
            tok = self._advance()
            return MatchSingleton(value=False, line=tok.line, col=tok.col)
        elif self._check(TokenType.KUCH_NAHI):
            tok = self._advance()
            return MatchSingleton(value=None, line=tok.line, col=tok.col)
        elif self._match(TokenType.INT):
            tok = self._previous_token()
            v_str = tok.value
            if v_str.startswith(("0x", "0X")):
                val = int(v_str, 16)
            elif v_str.startswith(("0b", "0B")):
                val = int(v_str, 2)
            elif v_str.startswith(("0o", "0O")):
                val = int(v_str, 8)
            else:
                val = int(v_str)
            val_expr = Constant(value=val, line=tok.line, col=tok.col)
            return MatchValue(value=val_expr, line=tok.line, col=tok.col)
        elif self._match(TokenType.FLOAT):
            tok = self._previous_token()
            val = float(tok.value)
            val_expr = Constant(value=val, line=tok.line, col=tok.col)
            return MatchValue(value=val_expr, line=tok.line, col=tok.col)
        elif self._match(TokenType.STRING):
            tok = self._previous_token()
            val = tok.value
            val_expr = Constant(value=val, line=tok.line, col=tok.col)
            return MatchValue(value=val_expr, line=tok.line, col=tok.col)
        elif self._check(TokenType.MINUS):
            minus_tok = self._advance()
            if self._match(TokenType.INT):
                tok = self._previous_token()
                v_str = tok.value
                if v_str.startswith(("0x", "0X")):
                    val = int(v_str, 16)
                elif v_str.startswith(("0b", "0B")):
                    val = int(v_str, 2)
                elif v_str.startswith(("0o", "0O")):
                    val = int(v_str, 8)
                else:
                    val = int(v_str)
                val = -val
                val_expr = Constant(value=val, line=minus_tok.line, col=minus_tok.col)
                return MatchValue(value=val_expr, line=minus_tok.line, col=minus_tok.col)
            elif self._match(TokenType.FLOAT):
                tok = self._previous_token()
                val = -float(tok.value)
                val_expr = Constant(value=val, line=minus_tok.line, col=minus_tok.col)
                return MatchValue(value=val_expr, line=minus_tok.line, col=minus_tok.col)
            else:
                raise self._error("Expected integer or float after '-' in pattern")
        elif self._check(TokenType.IDENTIFIER):
            tok = self._current_token()
            if tok.value == "_":
                self._advance()
                return MatchAs(pattern=None, name=None, line=tok.line, col=tok.col)

            dotted = self.parse_dotted_name()
            if self._match(TokenType.LPAREN):
                patterns = []
                kwd_attrs = []
                kwd_patterns = []
                while not self._check(TokenType.RPAREN):
                    if self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.ASSIGN:
                        kwd_name = self._advance().value
                        self._advance()
                        kwd_pat = self.parse_pattern()
                        kwd_attrs.append(kwd_name)
                        kwd_patterns.append(kwd_pat)
                    else:
                        pat = self.parse_pattern()
                        patterns.append(pat)
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN, "Expected ')' after class pattern arguments")
                return MatchClass(
                    cls=dotted,
                    patterns=patterns,
                    kwd_attrs=kwd_attrs,
                    kwd_patterns=kwd_patterns,
                    line=dotted.line,
                    col=dotted.col,
                )
            elif isinstance(dotted, Attribute):
                return MatchValue(value=dotted, line=dotted.line, col=dotted.col)
            elif isinstance(dotted, Name):
                return MatchAs(pattern=None, name=dotted.id, line=dotted.line, col=dotted.col)
            else:
                raise self._error(
                    f"Unexpected dotted name type in pattern: {type(dotted).__name__}"
                )
        elif self._match(TokenType.LBRACKET):
            line, col = self._previous_token().line, self._previous_token().col
            patterns = []
            while not self._check(TokenType.RBRACKET):
                patterns.append(self.parse_pattern())
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RBRACKET, "Expected ']' at end of sequence pattern")
            return MatchSequence(patterns=patterns, line=line, col=col)
        elif self._match(TokenType.LPAREN):
            line, col = self._previous_token().line, self._previous_token().col
            patterns = []
            is_tuple = False
            while not self._check(TokenType.RPAREN):
                patterns.append(self.parse_pattern())
                if self._match(TokenType.COMMA):
                    is_tuple = True
                else:
                    break
            self._expect(TokenType.RPAREN, "Expected ')' at end of tuple pattern")
            if len(patterns) == 0 or is_tuple or len(patterns) > 1:
                return MatchSequence(patterns=patterns, line=line, col=col)
            else:
                return patterns[0]
        elif self._match(TokenType.LBRACE):
            line, col = self._previous_token().line, self._previous_token().col
            keys = []
            patterns = []
            rest = None
            while not self._check(TokenType.RBRACE):
                if self._match(TokenType.DOUBLESTAR):
                    rest_tok = self._expect(
                        TokenType.IDENTIFIER, "Expected identifier after '**' in dict pattern"
                    )
                    rest = rest_tok.value
                    break
                else:
                    key_expr = self.parse_expression()
                    self._expect(TokenType.COLON, "Expected ':' after key in dict pattern")
                    pat = self.parse_pattern()
                    keys.append(key_expr)
                    patterns.append(pat)
                    if not self._match(TokenType.COMMA):
                        break
            self._expect(TokenType.RBRACE, "Expected '}' at end of mapping pattern")
            return MatchMapping(keys=keys, patterns=patterns, rest=rest, line=line, col=col)
        else:
            raise self._error(f"Unexpected token in pattern: {self._current_token().value!r}")

    def parse_dotted_name(self) -> Expr:
        tok = self._expect(TokenType.IDENTIFIER, "Expected identifier")
        node = Name(id=tok.value, line=tok.line, col=tok.col)
        while self._match(TokenType.DOT):
            attr_tok = self._expect(TokenType.IDENTIFIER, "Expected attribute name")
            node = Attribute(value=node, attr=attr_tok.value, line=attr_tok.line, col=attr_tok.col)
        return node

    def parse_try(self) -> Try:
        tok = self._expect(TokenType.KOSHISH, "Expected 'koshish'")
        body = self.parse_block()

        handlers = []
        while self._match(TokenType.GADBAD):
            handler_tok = self._previous_token()
            exc_type = None
            exc_name = None
            if not self._check(TokenType.COLON):
                exc_type = self.parse_expression()
                if self._match(TokenType.AS):
                    name_tok = self._expect(TokenType.IDENTIFIER, "Expected name after 'as'")
                    exc_name = name_tok.value
            exc_body = self.parse_block()
            handlers.append(
                ExceptHandler(
                    type=exc_type,
                    name=exc_name,
                    body=exc_body,
                    line=handler_tok.line,
                    col=handler_tok.col,
                )
            )

        orelse = []
        if self._match(TokenType.WARNA):
            orelse = self.parse_block()

        finalbody = []
        if self._match(TokenType.AAKHIR_ME):
            finalbody = self.parse_block()

        return Try(
            body=body,
            handlers=handlers,
            orelse=orelse,
            finalbody=finalbody,
            line=tok.line,
            col=tok.col,
        )

    def parse_raise(self) -> Raise:
        tok = self._expect(TokenType.UDAO, "Expected 'udao'")
        exc = None
        cause = None
        if not self._check(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT):
            exc = self.parse_expression()
            if self._match(TokenType.SE):
                cause = self.parse_expression()
        self._expect_newline_or_eof()
        return Raise(exc=exc, cause=cause, line=tok.line, col=tok.col)

    def parse_global(self) -> Global:
        tok = self._expect(TokenType.SABKA, "Expected 'sabka'")
        names = []
        while True:
            id_tok = self._expect(TokenType.IDENTIFIER, "Expected identifier")
            names.append(id_tok.value)
            if not self._match(TokenType.COMMA):
                break
        self._expect_newline_or_eof()
        return Global(names=names, line=tok.line, col=tok.col)

    def parse_nonlocal(self) -> Nonlocal:
        tok = self._expect(TokenType.NONLOCAL, "Expected 'nonlocal'")
        names = []
        while True:
            id_tok = self._expect(TokenType.IDENTIFIER, "Expected identifier")
            names.append(id_tok.value)
            if not self._match(TokenType.COMMA):
                break
        self._expect_newline_or_eof()
        return Nonlocal(names=names, line=tok.line, col=tok.col)

    def parse_import(self) -> Import:
        tok = self._expect(TokenType.LAO, "Expected 'lao'")
        names = []
        while True:
            parts = [self._expect(TokenType.IDENTIFIER, "Expected module name").value]
            while self._match(TokenType.DOT):
                parts.append(self._expect(TokenType.IDENTIFIER, "Expected submodule name").value)
            m_name = ".".join(parts)

            asname = None
            if self._match(TokenType.AS):
                asname = self._expect(TokenType.IDENTIFIER, "Expected alias").value
            names.append(alias(name=m_name, asname=asname, line=tok.line, col=tok.col))
            if not self._match(TokenType.COMMA):
                break
        self._expect_newline_or_eof()
        return Import(names=names, line=tok.line, col=tok.col)

    def parse_import_from(self) -> ImportFrom:
        tok = self._expect(TokenType.SE, "Expected 'se'")

        level = 0
        while self._match(TokenType.DOT):
            level += 1

        m_name = None
        if self._check(TokenType.IDENTIFIER):
            parts = [self._advance().value]
            while self._match(TokenType.DOT):
                parts.append(self._expect(TokenType.IDENTIFIER, "Expected submodule name").value)
            m_name = ".".join(parts)

        self._expect(TokenType.LAO, "Expected 'lao' after from-module")

        names = []
        if self._match(TokenType.STAR):
            names.append(alias(name="*", asname=None, line=tok.line, col=tok.col))
        else:
            has_parens = self._match(TokenType.LPAREN)
            while True:
                name_tok = self._expect(TokenType.IDENTIFIER, "Expected import name")
                asname = None
                if self._match(TokenType.AS):
                    asname = self._expect(TokenType.IDENTIFIER, "Expected alias").value
                names.append(
                    alias(name=name_tok.value, asname=asname, line=name_tok.line, col=name_tok.col)
                )
                if not self._match(TokenType.COMMA):
                    break
            if has_parens:
                self._expect(TokenType.RPAREN, "Expected ')' after import list")

        self._expect_newline_or_eof()
        return ImportFrom(module=m_name, names=names, level=level, line=tok.line, col=tok.col)

    def parse_assert(self) -> Assert:
        tok = self._expect(TokenType.ASSERT, "Expected 'assert'")
        test = self.parse_expression()
        msg = None
        if self._match(TokenType.COMMA):
            msg = self.parse_expression()
        self._expect_newline_or_eof()
        return Assert(test=test, msg=msg, line=tok.line, col=tok.col)

    def parse_with(self) -> With:
        tok = self._expect(TokenType.WITH, "Expected 'with' or 'ke_saath'")
        items = []
        while True:
            context_expr = self.parse_expression()
            optional_vars = None
            if self._match(TokenType.AS):
                optional_vars = self.parse_expression()
            items.append(withitem(context_expr=context_expr, optional_vars=optional_vars))
            if not self._match(TokenType.COMMA):
                break
        body = self.parse_block()
        return With(items=items, body=body, line=tok.line, col=tok.col)

    def parse_expr_statement_or_assignment(self) -> Stmt:
        expr = self.parse_expression()

        # Check for assignment
        if self._match(TokenType.ASSIGN):
            targets = [expr]
            value = self.parse_expression()
            while self._match(TokenType.ASSIGN):
                targets.append(value)
                value = self.parse_expression()
            self._expect_newline_or_eof()
            return Assign(targets=targets, value=value, line=expr.line, col=expr.col)

        # Check for augmented assignment (+=, -=, etc.)
        aug_assign_tokens = {
            TokenType.PLUS_ASSIGN: "+",
            TokenType.MINUS_ASSIGN: "-",
            TokenType.STAR_ASSIGN: "*",
            TokenType.SLASH_ASSIGN: "/",
            TokenType.DOUBLESLASH_ASSIGN: "//",
            TokenType.PERCENT_ASSIGN: "%",
            TokenType.DOUBLESTAR_ASSIGN: "**",
            TokenType.AMP_ASSIGN: "&",
            TokenType.PIPE_ASSIGN: "|",
            TokenType.CARET_ASSIGN: "^",
            TokenType.LSHIFT_ASSIGN: "<<",
            TokenType.RSHIFT_ASSIGN: ">>",
            TokenType.AT_ASSIGN: "@",
        }

        if self._current_token().type in aug_assign_tokens:
            tok = self._advance()
            op = aug_assign_tokens[tok.type]
            value = self.parse_expression()
            self._expect_newline_or_eof()
            return AugAssign(target=expr, op=op, value=value, line=expr.line, col=expr.col)

        # Check for annotated assignment, e.g. x: int = 10
        if self._match(TokenType.COLON):
            annotation = self.parse_expression()
            value = None
            if self._match(TokenType.ASSIGN):
                value = self.parse_expression()
            self._expect_newline_or_eof()
            return AnnAssign(
                target=expr, annotation=annotation, value=value, line=expr.line, col=expr.col
            )

        # Standard expression statement
        self._expect_newline_or_eof()
        return ExprStmt(value=expr, line=expr.line, col=expr.col)

    # ── Expression Parsing (Precedence Climb / Pratt) ─────────────────

    def parse_expression(self) -> Expr:
        # 1. Lambda functions (chota_funkshan)
        if self._check(TokenType.CHOTA_FUNKSHAN):
            return self.parse_lambda()

        # 2. BULAWO prefix sugar: bulawo func(args)
        if self._match(TokenType.BULAWO):
            self._previous_token()
            expr = self.parse_primary()
            if not isinstance(expr, Call):
                raise self._error("'bulawo' keyword ke baad function call hona chahiye")
            return expr

        expr = self.parse_logical_or()

        # 3. Ternary operator (x if cond else y) -> expr agar cond warna orelse
        if self._match(TokenType.AGAR):
            cond = self.parse_logical_or()
            self._expect(TokenType.WARNA, "Expected 'warna' in ternary expression")
            orelse = self.parse_expression()
            return IfExp(body=expr, test=cond, orelse=orelse, line=expr.line, col=expr.col)

        return expr

    def parse_lambda(self) -> Lambda:
        tok = self._expect(TokenType.CHOTA_FUNKSHAN, "Expected 'chota_funkshan'")
        args_list = []
        while not self._check(TokenType.COLON, TokenType.EOF):
            id_tok = self._expect(TokenType.IDENTIFIER, "Expected parameter in lambda")
            args_list.append(arg(arg=id_tok.value, line=id_tok.line, col=id_tok.col))
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.COLON, "Expected ':' after lambda parameters")
        body = self.parse_expression()
        return Lambda(
            args=arguments(args=args_list, line=tok.line, col=tok.col),
            body=body,
            line=tok.line,
            col=tok.col,
        )

    def parse_logical_or(self) -> Expr:
        expr = self.parse_logical_and()
        while self._match(TokenType.YA):
            right = self.parse_logical_and()
            expr = BoolOp(op="ya", values=[expr, right], line=expr.line, col=expr.col)
        return expr

    def parse_logical_and(self) -> Expr:
        expr = self.parse_logical_not()
        while self._match(TokenType.AUR):
            right = self.parse_logical_not()
            expr = BoolOp(op="aur", values=[expr, right], line=expr.line, col=expr.col)
        return expr

    def parse_logical_not(self) -> Expr:
        if self._match(TokenType.NAHI):
            tok = self._previous_token()
            operand = self.parse_logical_not()
            return UnaryOp(op="nahi", operand=operand, line=tok.line, col=tok.col)
        return self.parse_comparison()

    def parse_comparison(self) -> Expr:
        expr = self.parse_bitwise_or()
        ops = []
        comparators = []

        comp_tokens = {
            TokenType.EQ: "==",
            TokenType.NEQ: "!=",
            TokenType.LT: "<",
            TokenType.LTE: "<=",
            TokenType.GT: ">",
            TokenType.GTE: ">=",
            TokenType.MEIN: "mein",
            TokenType.MEIN_NAHI: "mein_nahi",
            TokenType.HAI: "hai",
            TokenType.NAHI_HAI: "nahi_hai",
        }

        while self._current_token().type in comp_tokens:
            tok = self._advance()
            ops.append(comp_tokens[tok.type])
            comparators.append(self.parse_bitwise_or())

        if ops:
            return Compare(
                left=expr, ops=ops, comparators=comparators, line=expr.line, col=expr.col
            )
        return expr

    def parse_bitwise_or(self) -> Expr:
        expr = self.parse_bitwise_xor()
        while self._match(TokenType.PIPE):
            right = self.parse_bitwise_xor()
            expr = BinOp(left=expr, op="|", right=right, line=expr.line, col=expr.col)
        return expr

    def parse_bitwise_xor(self) -> Expr:
        expr = self.parse_bitwise_and()
        while self._match(TokenType.CARET):
            right = self.parse_bitwise_and()
            expr = BinOp(left=expr, op="^", right=right, line=expr.line, col=expr.col)
        return expr

    def parse_bitwise_and(self) -> Expr:
        expr = self.parse_shift()
        while self._match(TokenType.AMP):
            right = self.parse_shift()
            expr = BinOp(left=expr, op="&", right=right, line=expr.line, col=expr.col)
        return expr

    def parse_shift(self) -> Expr:
        expr = self.parse_term()
        while self._match(TokenType.LSHIFT, TokenType.RSHIFT):
            op = "<<" if self._previous_token().type == TokenType.LSHIFT else ">>"
            right = self.parse_term()
            expr = BinOp(left=expr, op=op, right=right, line=expr.line, col=expr.col)
        return expr

    def parse_term(self) -> Expr:
        expr = self.parse_factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = "+" if self._previous_token().type == TokenType.PLUS else "-"
            right = self.parse_factor()
            expr = BinOp(left=expr, op=op, right=right, line=expr.line, col=expr.col)
        return expr

    def parse_factor(self) -> Expr:
        expr = self.parse_unary()
        factor_ops = {
            TokenType.STAR: "*",
            TokenType.SLASH: "/",
            TokenType.DOUBLESLASH: "//",
            TokenType.PERCENT: "%",
            TokenType.AT: "@",
        }
        while self._current_token().type in factor_ops:
            tok = self._advance()
            op = factor_ops[tok.type]
            right = self.parse_unary()
            expr = BinOp(left=expr, op=op, right=right, line=expr.line, col=expr.col)
        return expr

    def parse_unary(self) -> Expr:
        unary_ops = {
            TokenType.PLUS: "+",
            TokenType.MINUS: "-",
            TokenType.TILDE: "~",
        }
        if self._current_token().type in unary_ops:
            tok = self._advance()
            op = unary_ops[tok.type]
            operand = self.parse_unary()
            return UnaryOp(op=op, operand=operand, line=tok.line, col=tok.col)
        elif self._match(TokenType.INTEZAAR):
            tok = self._previous_token()
            value = self.parse_unary()
            return Await(value=value, line=tok.line, col=tok.col)

        return self.parse_power()

    def parse_power(self) -> Expr:
        expr = self.parse_primary()
        if self._match(TokenType.DOUBLESTAR):
            right = self.parse_unary()
            expr = BinOp(left=expr, op="**", right=right, line=expr.line, col=expr.col)
        return expr

    def parse_primary(self) -> Expr:
        expr = self.parse_atom()

        while True:
            if self._match(TokenType.LPAREN):
                # Call
                args = []
                keywords = []
                while not self._check(TokenType.RPAREN, TokenType.EOF):
                    if self._check(TokenType.IDENTIFIER) and self._peek().type == TokenType.ASSIGN:
                        id_tok = self._advance()
                        self._advance()  # '='
                        val = self.parse_expression()
                        keywords.append(
                            keyword(arg=id_tok.value, value=val, line=id_tok.line, col=id_tok.col)
                        )
                    else:
                        args.append(self.parse_expression())
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN, "Expected ')' after call arguments")
                expr = Call(func=expr, args=args, keywords=keywords, line=expr.line, col=expr.col)
            elif self._match(TokenType.DOT):
                id_tok = self._expect(TokenType.IDENTIFIER, "Expected attribute name")
                expr = Attribute(value=expr, attr=id_tok.value, line=expr.line, col=expr.col)
            elif self._match(TokenType.LBRACKET):
                # Subscript / Slice
                slice_expr = self.parse_slice()
                self._expect(TokenType.RBRACKET, "Expected ']' at end of subscript")
                expr = Subscript(value=expr, slice=slice_expr, line=expr.line, col=expr.col)
            else:
                break

        return expr

    def parse_slice(self) -> Expr:
        tok = self._current_token()
        first = None
        if not self._check(TokenType.COLON, TokenType.RBRACKET):
            first = self.parse_expression()

        if self._match(TokenType.COLON):
            upper = None
            if not self._check(TokenType.COLON, TokenType.RBRACKET):
                upper = self.parse_expression()
            step = None
            if self._match(TokenType.COLON):
                if not self._check(TokenType.RBRACKET):
                    step = self.parse_expression()
            return Slice(lower=first, upper=upper, step=step, line=tok.line, col=tok.col)
        else:
            if first is None:
                raise self._error("Subscript slice empty nahi ho sakti")
            return first

    def parse_atom(self) -> Expr:
        tok = self._current_token()

        if self._match(TokenType.INT):
            v_str = self._previous_token().value
            if v_str.startswith(("0x", "0X")):
                val = int(v_str, 16)
            elif v_str.startswith(("0b", "0B")):
                val = int(v_str, 2)
            elif v_str.startswith(("0o", "0O")):
                val = int(v_str, 8)
            else:
                val = int(v_str)
            return Constant(value=val, line=tok.line, col=tok.col)

        elif self._match(TokenType.FLOAT):
            return Constant(value=float(self._previous_token().value), line=tok.line, col=tok.col)

        elif self._match(TokenType.STRING):
            return Constant(value=self._previous_token().value, line=tok.line, col=tok.col)

        elif self._check(TokenType.FSTRING):
            f_tok = self._advance()
            return self.parse_fstring(f_tok)

        elif self._match(TokenType.SAHI):
            return Constant(value=True, line=tok.line, col=tok.col)

        elif self._match(TokenType.GALAT):
            return Constant(value=False, line=tok.line, col=tok.col)

        elif self._match(TokenType.KUCH_NAHI):
            return Constant(value=None, line=tok.line, col=tok.col)

        elif self._match(TokenType.KHUD):
            return Name(id="self", line=tok.line, col=tok.col)

        elif self._match(TokenType.IDENTIFIER):
            return Name(id=self._previous_token().value, line=tok.line, col=tok.col)

        # Allow keywords as expression variables/built-ins
        elif self._match(TokenType.BOLO):
            return Name(id="bolo", line=tok.line, col=tok.col)
        elif self._match(TokenType.POOCHHO):
            return Name(id="poochho", line=tok.line, col=tok.col)

        elif self._match(TokenType.LBRACKET):
            return self.parse_list_or_comp()

        elif self._match(TokenType.LBRACE):
            return self.parse_dict_or_set_or_comp()

        elif self._match(TokenType.LPAREN):
            # Tuple, grouped expression, or generator expression
            if self._match(TokenType.RPAREN):
                return Tuple(elts=[], line=tok.line, col=tok.col)

            first = self.parse_expression()
            if self._check(TokenType.GHUMO):
                generators = self.parse_comprehensions()
                self._expect(TokenType.RPAREN, "Expected ')' at end of generator expression")
                return GeneratorExp(elt=first, generators=generators, line=tok.line, col=tok.col)

            if self._match(TokenType.COMMA):
                elts = [first]
                while not self._check(TokenType.RPAREN, TokenType.EOF):
                    elts.append(self.parse_expression())
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN, "Expected ')' at end of tuple")
                return Tuple(elts=elts, line=tok.line, col=tok.col)

            self._expect(TokenType.RPAREN, "Expected ')' after grouped expression")
            return first

        elif self._match(TokenType.ELLIPSIS):
            return Constant(value=..., line=tok.line, col=tok.col)

        raise self._error(
            f"Ye expression kya hai bhai? Unexpected token: {tok.value or tok.type.name}"
        )

    def parse_fstring(self, token: Token) -> Expr:
        parts = []
        val = token.value
        pos = 0
        while pos < len(val):
            if val[pos] == "{" and (pos == 0 or val[pos - 1] != "\\"):
                # Start of expression
                pos += 1
                start = pos
                depth = 1
                while pos < len(val):
                    if val[pos] == "{":
                        depth += 1
                    elif val[pos] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    pos += 1
                if pos >= len(val):
                    raise ParseError(
                        "f-string expression brace band nahi hua", token.line, token.col
                    )
                expr_str = val[start:pos]
                pos += 1  # skip '}'

                # Lex and Parse the expression inside {}
                from ..lexer.lexer import Lexer

                sub_lexer = Lexer(expr_str, filename=self._filename)
                sub_lexer._line = token.line
                sub_lexer._col = token.col + start
                sub_tokens = sub_lexer.tokenize()
                if sub_tokens and sub_tokens[-1].type == TokenType.EOF:
                    sub_tokens.pop()

                if not sub_tokens:
                    raise ParseError("f-string expression khali hai", token.line, token.col)

                sub_parser = Parser(
                    sub_tokens, filename=self._filename, source=self._source_line_at(token.line)
                )
                expr = sub_parser.parse_expression()
                parts.append(FormattedValue(value=expr, line=token.line, col=token.col + start))
            else:
                # String constant part
                start = pos
                while pos < len(val) and not (
                    val[pos] == "{" and (pos == 0 or val[pos - 1] != "\\")
                ):
                    pos += 1
                segment = val[start:pos]
                segment = segment.replace("\\{", "{").replace("\\}", "}")
                parts.append(Constant(value=segment, line=token.line, col=token.col + start))

        return JoinedStr(values=parts, line=token.line, col=token.col)

    def parse_list_or_comp(self) -> Expr:
        tok = self._previous_token()
        if self._match(TokenType.RBRACKET):
            return List(elts=[], line=tok.line, col=tok.col)

        first = self.parse_expression()
        if self._check(TokenType.GHUMO):
            generators = self.parse_comprehensions()
            self._expect(TokenType.RBRACKET, "Expected ']' at end of list comprehension")
            return ListComp(elt=first, generators=generators, line=tok.line, col=tok.col)

        elts = [first]
        while self._match(TokenType.COMMA):
            if self._check(TokenType.RBRACKET):
                break
            elts.append(self.parse_expression())
        self._expect(TokenType.RBRACKET, "Expected ']' at end of list")
        return List(elts=elts, line=tok.line, col=tok.col)

    def parse_dict_or_set_or_comp(self) -> Expr:
        tok = self._previous_token()
        if self._match(TokenType.RBRACE):
            return Dict(keys=[], values=[], line=tok.line, col=tok.col)

        first = self.parse_expression()
        if self._match(TokenType.COLON):
            # Dict or DictComp
            val = self.parse_expression()
            if self._check(TokenType.GHUMO):
                generators = self.parse_comprehensions()
                self._expect(TokenType.RBRACE, "Expected '}' at end of dict comprehension")
                return DictComp(
                    key=first, value=val, generators=generators, line=tok.line, col=tok.col
                )

            keys: list[Expr | None] = [first]
            values = [val]
            while self._match(TokenType.COMMA):
                if self._check(TokenType.RBRACE):
                    break
                k = self.parse_expression()
                self._expect(TokenType.COLON, "Expected ':' after key in dictionary")
                v = self.parse_expression()
                keys.append(k)
                values.append(v)
            self._expect(TokenType.RBRACE, "Expected '}' at end of dictionary")
            return Dict(keys=keys, values=values, line=tok.line, col=tok.col)
        else:
            # Set or SetComp
            if self._check(TokenType.GHUMO):
                generators = self.parse_comprehensions()
                self._expect(TokenType.RBRACE, "Expected '}' at end of set comprehension")
                return SetComp(elt=first, generators=generators, line=tok.line, col=tok.col)

            elts = [first]
            while self._match(TokenType.COMMA):
                if self._check(TokenType.RBRACE):
                    break
                elts.append(self.parse_expression())
            self._expect(TokenType.RBRACE, "Expected '}' at end of set")
            return Set(elts=elts, line=tok.line, col=tok.col)

    def parse_comprehensions(self) -> list[comprehension]:
        generators = []
        while self._match(TokenType.GHUMO):
            is_async = False
            # check for async comprehension via "tez"
            if self._check(TokenType.TEZ):
                self._advance()
                self._expect(TokenType.GHUMO, "Expected 'ghumo' after 'tez' in comprehension")
                is_async = True

            target = self.parse_primary()
            if self._match(TokenType.COMMA):
                elts = [target]
                while True:
                    elts.append(self.parse_primary())
                    if not self._match(TokenType.COMMA):
                        break
                target = Tuple(elts=elts, line=target.line, col=target.col)

            self._expect(TokenType.MEIN, "Expected 'mein' in comprehension")
            iter_expr = self.parse_expression()
            ifs = []
            while self._match(TokenType.AGAR):
                ifs.append(self.parse_expression())
            generators.append(
                comprehension(target=target, iter=iter_expr, ifs=ifs, is_async=is_async)
            )
        return generators
