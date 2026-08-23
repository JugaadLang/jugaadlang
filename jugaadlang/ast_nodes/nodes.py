"""
JugaadLang AST (Abstract Syntax Tree) Nodes.
Each node includes line and column information for accurate error reporting.
"""

from __future__ import annotations

from dataclasses import KW_ONLY, dataclass, field
from typing import Any, Optional


@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    _: KW_ONLY
    line: int = 1
    col: int = 1


@dataclass
class Stmt(ASTNode):
    """Base class for all statements."""

    pass


@dataclass
class Expr(ASTNode):
    """Base class for all expressions."""

    pass


# ── Program Structure ────────────────────────────────────────────────────────


@dataclass
class Module(ASTNode):
    """The root node of a JugaadLang program."""

    body: list[Stmt] = field(default_factory=list)


# ── Statements ───────────────────────────────────────────────────────────────


@dataclass
class FunctionDef(Stmt):
    """Function definition (banao name(args): ...)."""

    name: str
    args: arguments
    body: list[Stmt]
    decorator_list: list[Expr] = field(default_factory=list)
    returns: Optional[Expr] = None
    is_async: bool = False


@dataclass
class ClassDef(Stmt):
    """Class definition (ustad Name: ...)."""

    name: str
    bases: list[Expr]
    body: list[Stmt]
    decorator_list: list[Expr] = field(default_factory=list)


@dataclass
class Return(Stmt):
    """Return statement (wapas value)."""

    value: Optional[Expr] = None


@dataclass
class Delete(Stmt):
    """Delete statement (del target)."""

    targets: list[Expr] = field(default_factory=list)


@dataclass
class Assign(Stmt):
    """Assignment statement (x = 10)."""

    targets: list[Expr]
    value: Expr


@dataclass
class AugAssign(Stmt):
    """Augmented assignment (x += 10)."""

    target: Expr
    op: str  # '+', '-', '*', etc.
    value: Expr


@dataclass
class AnnAssign(Stmt):
    """Annotated assignment (x: int = 10)."""

    target: Expr
    annotation: Expr
    value: Optional[Expr] = None
    simple: int = 1


@dataclass
class For(Stmt):
    """For loop (ghumo item mein items: ...)."""

    target: Expr
    iter: Expr
    body: list[Stmt]
    orelse: list[Stmt] = field(default_factory=list)
    is_async: bool = False


@dataclass
class While(Stmt):
    """While loop (jabtak condition: ...)."""

    test: Expr
    body: list[Stmt]
    orelse: list[Stmt] = field(default_factory=list)


@dataclass
class If(Stmt):
    """If-elif-else conditional (agar cond: ... shayad cond: ... warna: ...)."""

    test: Expr
    body: list[Stmt]
    orelse: list[Stmt] = field(default_factory=list)


@dataclass
class With(Stmt):
    """With context manager (with ctx as var: ...)."""

    items: list[withitem]
    body: list[Stmt]
    is_async: bool = False


@dataclass
class Raise(Stmt):
    """Raise/throw exception (udao exc)."""

    exc: Optional[Expr] = None
    cause: Optional[Expr] = None


@dataclass
class Try(Stmt):
    """Try-except-finally block (koshish: ... gadbad: ... aakhir_me: ...)."""

    body: list[Stmt]
    handlers: list[ExceptHandler] = field(default_factory=list)
    orelse: list[Stmt] = field(default_factory=list)
    finalbody: list[Stmt] = field(default_factory=list)


@dataclass
class Assert(Stmt):
    """Assert statement (assert condition, message)."""

    test: Expr
    msg: Optional[Expr] = None


@dataclass
class Import(Stmt):
    """Import statement (lao module)."""

    names: list[alias]


@dataclass
class ImportFrom(Stmt):
    """From-import statement (se module lao name)."""

    module: Optional[str]
    names: list[alias]
    level: int = 0


@dataclass
class Global(Stmt):
    """Global declaration (sabka var)."""

    names: list[str]


@dataclass
class Nonlocal(Stmt):
    """Nonlocal declaration (nonlocal var)."""

    names: list[str]


@dataclass
class ExprStmt(Stmt):
    """Expression statement (just calling a function or a value on its own line)."""

    value: Expr


@dataclass
class Pass(Stmt):
    """Pass / empty statement (theek_hai)."""

    pass


@dataclass
class Break(Stmt):
    """Break statement (rukja)."""

    pass


@dataclass
class Continue(Stmt):
    """Continue statement (chalte_raho)."""

    pass


@dataclass
class PoochhoStmt(Stmt):
    """Special shorthand statement: 'poochho name' equivalent to 'name = input()'."""

    target: Name


# ── Expressions ──────────────────────────────────────────────────────────────


@dataclass
class BoolOp(Expr):
    """Boolean operation (and, or)."""

    op: str  # 'aur', 'ya'
    values: list[Expr] = field(default_factory=list)


@dataclass
class BinOp(Expr):
    """Binary operation (+, -, *, etc.)."""

    left: Expr
    op: str
    right: Expr


@dataclass
class UnaryOp(Expr):
    """Unary operation (not, unary plus/minus/tilde)."""

    op: str
    operand: Expr


@dataclass
class Lambda(Expr):
    """Lambda function (chota_funkshan x: x + 1)."""

    args: arguments
    body: Expr


@dataclass
class IfExp(Expr):
    """Ternary expression (x if cond else y)."""

    body: Expr
    test: Expr
    orelse: Expr


@dataclass
class Dict(Expr):
    """Dictionary literal ({k: v})."""

    keys: list[Optional[Expr]] = field(default_factory=list)
    values: list[Expr] = field(default_factory=list)


@dataclass
class Set(Expr):
    """Set literal ({x, y})."""

    elts: list[Expr] = field(default_factory=list)


@dataclass
class ListComp(Expr):
    """List comprehension ([x ghumo x mein items])."""

    elt: Expr
    generators: list[comprehension] = field(default_factory=list)


@dataclass
class SetComp(Expr):
    """Set comprehension ({x ghumo x mein items})."""

    elt: Expr
    generators: list[comprehension] = field(default_factory=list)


@dataclass
class DictComp(Expr):
    """Dict comprehension ({k: v ghumo k, v mein items})."""

    key: Expr
    value: Expr
    generators: list[comprehension] = field(default_factory=list)


@dataclass
class GeneratorExp(Expr):
    """Generator expression ((x ghumo x mein items))."""

    elt: Expr
    generators: list[comprehension] = field(default_factory=list)


@dataclass
class Await(Expr):
    """Await expression (intezaar value)."""

    value: Expr


@dataclass
class Yield(Expr):
    """Yield expression (baanto value)."""

    value: Optional[Expr] = None


@dataclass
class YieldFrom(Expr):
    """Yield from expression (baanto se value)."""

    value: Expr


@dataclass
class Compare(Expr):
    """Comparison (x == y, a < b < c)."""

    left: Expr
    ops: list[str]
    comparators: list[Expr]


@dataclass
class Call(Expr):
    """Function call (func(args))."""

    func: Expr
    args: list[Expr] = field(default_factory=list)
    keywords: list[keyword] = field(default_factory=list)


@dataclass
class FormattedValue(Expr):
    """Formatted value inside f-string (e.g. {x} inside f"x is {x}")."""

    value: Expr
    conversion: int = -1
    format_spec: Optional[JoinedStr] = None


@dataclass
class JoinedStr(Expr):
    """F-string literal containing string constants and formatted values."""

    values: list[Expr] = field(default_factory=list)


@dataclass
class Constant(Expr):
    """Literal constant (string, int, float, boolean, None)."""

    value: Any


@dataclass
class Attribute(Expr):
    """Attribute access (obj.attr)."""

    value: Expr
    attr: str


@dataclass
class Subscript(Expr):
    """Subscript/indexing (obj[key])."""

    value: Expr
    slice: Expr


@dataclass
class Starred(Expr):
    """Starred expression (*args)."""

    value: Expr


@dataclass
class Name(Expr):
    """Identifier/variable name (e.g. x)."""

    id: str


@dataclass
class List(Expr):
    """List literal ([x, y])."""

    elts: list[Expr] = field(default_factory=list)


@dataclass
class Tuple(Expr):
    """Tuple literal ((x, y))."""

    elts: list[Expr] = field(default_factory=list)


@dataclass
class Slice(Expr):
    """Slice object (start:stop:step)."""

    lower: Optional[Expr] = None
    upper: Optional[Expr] = None
    step: Optional[Expr] = None


# ── Helper Nodes ─────────────────────────────────────────────────────────────


@dataclass
class comprehension(ASTNode):
    """Comprehension component: ghumo target mein iter agar cond."""

    target: Expr
    iter: Expr
    ifs: list[Expr] = field(default_factory=list)
    is_async: bool = False


@dataclass
class arg(ASTNode):
    """Single argument name with optional annotation."""

    arg: str
    annotation: Optional[Expr] = None


@dataclass
class arguments(ASTNode):
    """Function arguments specification."""

    args: list[arg] = field(default_factory=list)
    posonlyargs: list[arg] = field(default_factory=list)
    kwonlyargs: list[arg] = field(default_factory=list)
    kw_defaults: list[Optional[Expr]] = field(default_factory=list)
    defaults: list[Expr] = field(default_factory=list)
    vararg: Optional[arg] = None
    kwarg: Optional[arg] = None


@dataclass
class keyword(ASTNode):
    """Keyword argument in a function call (name=value)."""

    arg: Optional[str]
    value: Expr


@dataclass
class alias(ASTNode):
    """Alias for imports (name as asname)."""

    name: str
    asname: Optional[str] = None


@dataclass
class withitem(ASTNode):
    """Context manager item (ctx as var)."""

    context_expr: Expr
    optional_vars: Optional[Expr] = None


@dataclass
class ExceptHandler(ASTNode):
    """Except/error handling block (gadbad ErrorName as e: ...)."""

    type: Optional[Expr] = None
    name: Optional[str] = None
    body: list[Stmt] = field(default_factory=list)


# ── Pattern Matching AST Nodes ────────────────────────────────────────────────


@dataclass
class Match(Stmt):
    """Pattern matching root (agar_match subject: ...)."""

    subject: Expr
    cases: list[match_case] = field(default_factory=list)


@dataclass
class match_case(ASTNode):
    """Single pattern match case (kaand pattern [agar guard]: block)."""

    pattern: Pattern
    guard: Optional[Expr] = None
    body: list[Stmt] = field(default_factory=list)


@dataclass
class Pattern(ASTNode):
    """Base pattern class."""

    pass


@dataclass
class MatchValue(Pattern):
    """Value match pattern (e.g. constant values)."""

    value: Expr


@dataclass
class MatchSingleton(Pattern):
    """Singleton match pattern (e.g. sahi, galat, kuch_nahi)."""

    value: Any


@dataclass
class MatchAs(Pattern):
    """Bind pattern (e.g. case x:, or case _: for wildcard)."""

    pattern: Optional[Pattern] = None
    name: Optional[str] = None


@dataclass
class MatchOr(Pattern):
    """Or match pattern (e.g. pattern1 | pattern2)."""

    patterns: list[Pattern] = field(default_factory=list)


@dataclass
class MatchSequence(Pattern):
    """Sequence match pattern (e.g. [a, b], (c, d))."""

    patterns: list[Pattern] = field(default_factory=list)


@dataclass
class MatchMapping(Pattern):
    """Mapping match pattern (e.g. {'name': name})."""

    keys: list[Expr] = field(default_factory=list)
    patterns: list[Pattern] = field(default_factory=list)
    rest: Optional[str] = None


@dataclass
class MatchClass(Pattern):
    """Class/object destructuring pattern (e.g. Point(x, y))."""

    cls: Expr
    patterns: list[Pattern] = field(default_factory=list)
    kwd_attrs: list[str] = field(default_factory=list)
    kwd_patterns: list[Pattern] = field(default_factory=list)
