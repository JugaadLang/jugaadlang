"""
JugaadLang Transformer — Converts JugaadLang AST to Python standard library AST.
"""

from __future__ import annotations
import ast
from typing import Any

from ..ast_nodes.nodes import (
    Module,
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
    Yield,
    YieldFrom,
    Compare,
    Call,
    FormattedValue,
    JoinedStr,
    Constant,
    Attribute,
    Subscript,
    Starred,
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
    MatchValue,
    MatchSingleton,
    MatchAs,
    MatchOr,
    MatchSequence,
    MatchMapping,
    MatchClass,
)

# ── Operator Mappings ────────────────────────────────────────────────────────

BIN_OPS = {
    "+": ast.Add,
    "-": ast.Sub,
    "*": ast.Mult,
    "/": ast.Div,
    "//": ast.FloorDiv,
    "%": ast.Mod,
    "**": ast.Pow,
    "<<": ast.LShift,
    ">>": ast.RShift,
    "|": ast.BitOr,
    "^": ast.BitXor,
    "&": ast.BitAnd,
    "@": ast.MatMult,
}

UNARY_OPS = {
    "+": ast.UAdd,
    "-": ast.USub,
    "~": ast.Invert,
    "nahi": ast.Not,
}

COMP_OPS = {
    "==": ast.Eq,
    "!=": ast.NotEq,
    "<": ast.Lt,
    "<=": ast.LtE,
    ">": ast.Gt,
    ">=": ast.GtE,
    "mein": ast.In,
    "mein_nahi": ast.NotIn,
    "hai": ast.Is,
    "nahi_hai": ast.IsNot,
}

BOOL_OPS = {
    "aur": ast.And,
    "ya": ast.Or,
}


class JugaadToPythonTransformer:
    """
    Traverses the JugaadLang AST and translates each node into a corresponding Python AST node.
    """

    def __init__(self, filename: str = "<stdin>") -> None:
        self.filename = filename

    def transform(self, node: Module) -> ast.Module:
        """Transform a JugaadLang Module to a Python ast.Module."""
        py_module = self.visit(node)
        ast.fix_missing_locations(py_module)
        return py_module

    def visit(self, node: Any, ctx: Any = None) -> Any:
        """Dispatches node visiting recursively."""
        if node is None:
            return None

        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        res = visitor(node, ctx)

        # Propagate line and column info to Python AST nodes for accurate error stack traces
        if isinstance(res, ast.AST) and hasattr(node, "line") and hasattr(node, "col"):
            res.lineno = node.line
            res.col_offset = node.col
            # Also set end lines if available or copy from start
            res.end_lineno = node.line
            res.end_col_offset = node.col

        return res

    def generic_visit(self, node: Any, ctx: Any = None) -> Any:
        raise NotImplementedError(
            f"Transformer visitor visit_{type(node).__name__} is not implemented"
        )

    # ── Visitor Methods ───────────────────────────────────────────────

    def visit_Module(self, node: Module, ctx: Any = None) -> ast.Module:
        body = [self.visit(stmt) for stmt in node.body]
        return ast.Module(body=body, type_ignores=[])

    def visit_FunctionDef(self, node: FunctionDef, ctx: Any = None) -> ast.AST:
        # 'shuru' method maps to '__init__' in OOP
        name = "__init__" if node.name == "shuru" else node.name
        args = self.visit(node.args)
        body = [self.visit(stmt) for stmt in node.body]
        decorators = [self.visit(dec) for dec in node.decorator_list]
        returns = self.visit(node.returns) if node.returns else None

        if node.is_async:
            return ast.AsyncFunctionDef(
                name=name, args=args, body=body, decorator_list=decorators, returns=returns
            )
        else:
            return ast.FunctionDef(
                name=name, args=args, body=body, decorator_list=decorators, returns=returns
            )

    def visit_arguments(self, node: arguments, ctx: Any = None) -> ast.arguments:
        py_args = [self.visit(arg_item) for arg_item in node.args]
        py_defaults = [self.visit(def_val) for def_val in node.defaults]
        py_vararg = self.visit(node.vararg) if node.vararg else None
        py_kwarg = self.visit(node.kwarg) if node.kwarg else None

        return ast.arguments(
            posonlyargs=[],
            args=py_args,
            vararg=py_vararg,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=py_kwarg,
            defaults=py_defaults,
        )

    def visit_arg(self, node: arg, ctx: Any = None) -> ast.arg:
        # If parameter name is 'khud', map it to 'self'
        name = "self" if node.arg == "khud" else node.arg
        annotation = self.visit(node.annotation) if node.annotation else None
        return ast.arg(arg=name, annotation=annotation)

    def visit_ClassDef(self, node: ClassDef, ctx: Any = None) -> ast.ClassDef:
        bases = [self.visit(base) for base in node.bases]
        body = [self.visit(stmt) for stmt in node.body]
        decorators = [self.visit(dec) for dec in node.decorator_list]
        return ast.ClassDef(
            name=node.name, bases=bases, keywords=[], body=body, decorator_list=decorators
        )

    def visit_Return(self, node: Return, ctx: Any = None) -> ast.Return:
        value = self.visit(node.value) if node.value else None
        return ast.Return(value=value)

    def visit_Delete(self, node: Delete, ctx: Any = None) -> ast.Delete:
        targets = [self.visit(t, ast.Del()) for t in node.targets]
        return ast.Delete(targets=targets)

    def visit_Assign(self, node: Assign, ctx: Any = None) -> ast.Assign:
        targets = [self.visit(t, ast.Store()) for t in node.targets]
        value = self.visit(node.value)
        return ast.Assign(targets=targets, value=value)

    def visit_AugAssign(self, node: AugAssign, ctx: Any = None) -> ast.AugAssign:
        target = self.visit(node.target, ast.Store())
        op = BIN_OPS[node.op]()
        value = self.visit(node.value)
        return ast.AugAssign(target=target, op=op, value=value)

    def visit_AnnAssign(self, node: AnnAssign, ctx: Any = None) -> ast.AnnAssign:
        target = self.visit(node.target, ast.Store())
        annotation = self.visit(node.annotation)
        value = self.visit(node.value) if node.value else None
        return ast.AnnAssign(target=target, annotation=annotation, value=value, simple=node.simple)

    def visit_For(self, node: For, ctx: Any = None) -> ast.AST:
        target = self.visit(node.target, ast.Store())
        iter_expr = self.visit(node.iter)
        body = [self.visit(stmt) for stmt in node.body]
        orelse = [self.visit(stmt) for stmt in node.orelse]

        if node.is_async:
            return ast.AsyncFor(target=target, iter=iter_expr, body=body, orelse=orelse)
        else:
            return ast.For(target=target, iter=iter_expr, body=body, orelse=orelse)

    def visit_While(self, node: While, ctx: Any = None) -> ast.While:
        test = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        orelse = [self.visit(stmt) for stmt in node.orelse]
        return ast.While(test=test, body=body, orelse=orelse)

    def visit_If(self, node: If, ctx: Any = None) -> ast.If:
        test = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        orelse = [self.visit(stmt) for stmt in node.orelse]
        return ast.If(test=test, body=body, orelse=orelse)

    def visit_With(self, node: With, ctx: Any = None) -> ast.AST:
        items = [self.visit(item) for item in node.items]
        body = [self.visit(stmt) for stmt in node.body]
        if node.is_async:
            return ast.AsyncWith(items=items, body=body)
        else:
            return ast.With(items=items, body=body)

    def visit_withitem(self, node: withitem, ctx: Any = None) -> ast.withitem:
        context_expr = self.visit(node.context_expr)
        optional_vars = self.visit(node.optional_vars, ast.Store()) if node.optional_vars else None
        return ast.withitem(context_expr=context_expr, optional_vars=optional_vars)

    def visit_Raise(self, node: Raise, ctx: Any = None) -> ast.Raise:
        exc = self.visit(node.exc) if node.exc else None
        cause = self.visit(node.cause) if node.cause else None
        return ast.Raise(exc=exc, cause=cause)

    def visit_Try(self, node: Try, ctx: Any = None) -> ast.Try:
        body = [self.visit(stmt) for stmt in node.body]
        handlers = [self.visit(h) for h in node.handlers]
        orelse = [self.visit(stmt) for stmt in node.orelse]
        finalbody = [self.visit(stmt) for stmt in node.finalbody]
        return ast.Try(body=body, handlers=handlers, orelse=orelse, finalbody=finalbody)

    def visit_ExceptHandler(self, node: ExceptHandler, ctx: Any = None) -> ast.ExceptHandler:
        exc_type = self.visit(node.type) if node.type else None
        body = [self.visit(stmt) for stmt in node.body]
        return ast.ExceptHandler(type=exc_type, name=node.name, body=body)

    def visit_Assert(self, node: Assert, ctx: Any = None) -> ast.Assert:
        test = self.visit(node.test)
        msg = self.visit(node.msg) if node.msg else None
        return ast.Assert(test=test, msg=msg)

    def visit_Import(self, node: Import, ctx: Any = None) -> ast.Import:
        names = [self.visit(alias_item) for alias_item in node.names]
        return ast.Import(names=names)

    def visit_ImportFrom(self, node: ImportFrom, ctx: Any = None) -> ast.ImportFrom:
        names = [self.visit(alias_item) for alias_item in node.names]
        return ast.ImportFrom(module=node.module, names=names, level=node.level)

    def visit_alias(self, node: alias, ctx: Any = None) -> ast.alias:
        return ast.alias(name=node.name, asname=node.asname)

    def visit_Global(self, node: Global, ctx: Any = None) -> ast.Global:
        return ast.Global(names=node.names)

    def visit_Nonlocal(self, node: Nonlocal, ctx: Any = None) -> ast.Nonlocal:
        return ast.Nonlocal(names=node.names)

    def visit_ExprStmt(self, node: ExprStmt, ctx: Any = None) -> ast.Expr:
        value = self.visit(node.value)
        return ast.Expr(value=value)

    def visit_Pass(self, node: Pass, ctx: Any = None) -> ast.Pass:
        return ast.Pass()

    def visit_Break(self, node: Break, ctx: Any = None) -> ast.Break:
        return ast.Break()

    def visit_Continue(self, node: Continue, ctx: Any = None) -> ast.Continue:
        return ast.Continue()

    def visit_PoochhoStmt(self, node: PoochhoStmt, ctx: Any = None) -> ast.Assign:
        target = self.visit(node.target, ast.Store())
        input_call = ast.Call(func=ast.Name(id="input", ctx=ast.Load()), args=[], keywords=[])
        return ast.Assign(targets=[target], value=input_call)

    def visit_BoolOp(self, node: BoolOp, ctx: Any = None) -> ast.BoolOp:
        op = BOOL_OPS[node.op]()
        values = [self.visit(val) for val in node.values]
        return ast.BoolOp(op=op, values=values)

    def visit_BinOp(self, node: BinOp, ctx: Any = None) -> ast.BinOp:
        left = self.visit(node.left)
        op = BIN_OPS[node.op]()
        right = self.visit(node.right)
        return ast.BinOp(left=left, op=op, right=right)

    def visit_UnaryOp(self, node: UnaryOp, ctx: Any = None) -> ast.UnaryOp:
        op = UNARY_OPS[node.op]()
        operand = self.visit(node.operand)
        return ast.UnaryOp(op=op, operand=operand)

    def visit_Lambda(self, node: Lambda, ctx: Any = None) -> ast.Lambda:
        args = self.visit(node.args)
        body = self.visit(node.body)
        return ast.Lambda(args=args, body=body)

    def visit_IfExp(self, node: IfExp, ctx: Any = None) -> ast.IfExp:
        body = self.visit(node.body)
        test = self.visit(node.test)
        orelse = self.visit(node.orelse)
        return ast.IfExp(body=body, test=test, orelse=orelse)

    def visit_Dict(self, node: Dict, ctx: Any = None) -> ast.Dict:
        keys = [self.visit(k) if k else None for k in node.keys]
        values = [self.visit(v) for v in node.values]
        return ast.Dict(keys=keys, values=values)

    def visit_Set(self, node: Set, ctx: Any = None) -> ast.Set:
        elts = [self.visit(e) for e in node.elts]
        return ast.Set(elts=elts)

    def visit_ListComp(self, node: ListComp, ctx: Any = None) -> ast.ListComp:
        elt = self.visit(node.elt)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.ListComp(elt=elt, generators=generators)

    def visit_SetComp(self, node: SetComp, ctx: Any = None) -> ast.SetComp:
        elt = self.visit(node.elt)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.SetComp(elt=elt, generators=generators)

    def visit_DictComp(self, node: DictComp, ctx: Any = None) -> ast.DictComp:
        key = self.visit(node.key)
        value = self.visit(node.value)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.DictComp(key=key, value=value, generators=generators)

    def visit_GeneratorExp(self, node: GeneratorExp, ctx: Any = None) -> ast.GeneratorExp:
        elt = self.visit(node.elt)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.GeneratorExp(elt=elt, generators=generators)

    def visit_comprehension(self, node: comprehension, ctx: Any = None) -> ast.comprehension:
        target = self.visit(node.target, ast.Store())
        iter_expr = self.visit(node.iter)
        ifs = [self.visit(cond) for cond in node.ifs]
        return ast.comprehension(target=target, iter=iter_expr, ifs=ifs, is_async=node.is_async)

    def visit_Await(self, node: Await, ctx: Any = None) -> ast.Await:
        value = self.visit(node.value)
        return ast.Await(value=value)

    def visit_Yield(self, node: Yield, ctx: Any = None) -> ast.Yield:
        value = self.visit(node.value) if node.value else None
        return ast.Yield(value=value)

    def visit_YieldFrom(self, node: YieldFrom, ctx: Any = None) -> ast.YieldFrom:
        value = self.visit(node.value)
        return ast.YieldFrom(value=value)

    def visit_Compare(self, node: Compare, ctx: Any = None) -> ast.Compare:
        left = self.visit(node.left)
        ops: list[ast.cmpop] = [COMP_OPS[op]() for op in node.ops]
        comparators = [self.visit(c) for c in node.comparators]
        return ast.Compare(left=left, ops=ops, comparators=comparators)

    def visit_Call(self, node: Call, ctx: Any = None) -> ast.Call:
        func = self.visit(node.func)
        args = [self.visit(arg_item) for arg_item in node.args]
        keywords = [self.visit(kw) for kw in node.keywords]
        return ast.Call(func=func, args=args, keywords=keywords)

    def visit_keyword(self, node: keyword, ctx: Any = None) -> ast.keyword:
        value = self.visit(node.value)
        return ast.keyword(arg=node.arg, value=value)

    def visit_FormattedValue(self, node: FormattedValue, ctx: Any = None) -> ast.FormattedValue:
        value = self.visit(node.value)
        format_spec = self.visit(node.format_spec) if node.format_spec else None
        return ast.FormattedValue(value=value, conversion=node.conversion, format_spec=format_spec)

    def visit_JoinedStr(self, node: JoinedStr, ctx: Any = None) -> ast.JoinedStr:
        values = [self.visit(val) for val in node.values]
        return ast.JoinedStr(values=values)

    def visit_Constant(self, node: Constant, ctx: Any = None) -> ast.Constant:
        return ast.Constant(value=node.value)

    def visit_Attribute(self, node: Attribute, ctx: Any = None) -> ast.Attribute:
        py_ctx = ctx if ctx is not None else ast.Load()
        value = self.visit(node.value)
        return ast.Attribute(value=value, attr=node.attr, ctx=py_ctx)

    def visit_Subscript(self, node: Subscript, ctx: Any = None) -> ast.Subscript:
        py_ctx = ctx if ctx is not None else ast.Load()
        value = self.visit(node.value)
        slice_expr = self.visit(node.slice)
        return ast.Subscript(value=value, slice=slice_expr, ctx=py_ctx)

    def visit_Slice(self, node: Slice, ctx: Any = None) -> ast.Slice:
        lower = self.visit(node.lower) if node.lower else None
        upper = self.visit(node.upper) if node.upper else None
        step = self.visit(node.step) if node.step else None
        return ast.Slice(lower=lower, upper=upper, step=step)

    def visit_Starred(self, node: Starred, ctx: Any = None) -> ast.Starred:
        py_ctx = ctx if ctx is not None else ast.Load()
        value = self.visit(node.value)
        return ast.Starred(value=value, ctx=py_ctx)

    def visit_Name(self, node: Name, ctx: Any = None) -> ast.Name:
        py_ctx = ctx if ctx is not None else ast.Load()
        # Translate Roman Hindi keywords that represent built-in functions
        id_map = {
            "bolo": "print",
            "poochho": "input",
            "khud": "self",
            "maan": "abs",
            "sab": "all",
            "koi_bhi": "any",
            "binary": "bin",
            "satyata": "bool",
            "bulaane_yogya": "callable",
            "akshar": "chr",
            "gun_hatao": "delattr",
            "kosh": "dict",
            "bhag_shesh": "divmod",
            "ginti": "enumerate",
            "chhano": "filter",
            "gun_lao": "getattr",
            "gun_hai": "hasattr",
            "pehchan": "id",
            "purnank": "int",
            "prakar_hai": "isinstance",
            "subclass_hai": "issubclass",
            "lambaee": "len",
            "suchi": "list",
            "adhiktam": "max",
            "nyuntam": "min",
            "agla": "next",
            "vastu": "object",
            "ghat": "pow",
            "ulta": "reversed",
            "gun_badlo": "setattr",
            "tukda": "slice",
            "kramwar": "sorted",
            "shabd": "str",
            "yog": "sum",
            "prakar": "type",
        }
        name_id = id_map.get(node.id, node.id)
        return ast.Name(id=name_id, ctx=py_ctx)

    def visit_List(self, node: List, ctx: Any = None) -> ast.List:
        py_ctx = ctx if ctx is not None else ast.Load()
        elts = [self.visit(e, py_ctx) for e in node.elts]
        return ast.List(elts=elts, ctx=py_ctx)

    def visit_Tuple(self, node: Tuple, ctx: Any = None) -> ast.Tuple:
        py_ctx = ctx if ctx is not None else ast.Load()
        elts = [self.visit(e, py_ctx) for e in node.elts]
        return ast.Tuple(elts=elts, ctx=py_ctx)

    def visit_Match(self, node: Match, ctx: Any = None) -> ast.Match:
        subject = self.visit(node.subject)
        cases = [self.visit(case) for case in node.cases]
        return ast.Match(subject=subject, cases=cases)

    def visit_match_case(self, node: match_case, ctx: Any = None) -> ast.match_case:
        pattern = self.visit(node.pattern)
        guard = self.visit(node.guard) if node.guard else None
        body = [self.visit(stmt) for stmt in node.body]
        return ast.match_case(pattern=pattern, guard=guard, body=body)

    def visit_MatchValue(self, node: MatchValue, ctx: Any = None) -> ast.MatchValue:
        value = self.visit(node.value)
        return ast.MatchValue(value=value)

    def visit_MatchSingleton(self, node: MatchSingleton, ctx: Any = None) -> ast.MatchSingleton:
        return ast.MatchSingleton(value=node.value)

    def visit_MatchAs(self, node: MatchAs, ctx: Any = None) -> ast.MatchAs:
        pattern = self.visit(node.pattern) if node.pattern else None
        return ast.MatchAs(pattern=pattern, name=node.name)

    def visit_MatchOr(self, node: MatchOr, ctx: Any = None) -> ast.MatchOr:
        patterns = [self.visit(p) for p in node.patterns]
        return ast.MatchOr(patterns=patterns)

    def visit_MatchSequence(self, node: MatchSequence, ctx: Any = None) -> ast.MatchSequence:
        patterns = [self.visit(p) for p in node.patterns]
        return ast.MatchSequence(patterns=patterns)

    def visit_MatchMapping(self, node: MatchMapping, ctx: Any = None) -> ast.MatchMapping:
        keys = [self.visit(k) for k in node.keys]
        patterns = [self.visit(p) for p in node.patterns]
        return ast.MatchMapping(keys=keys, patterns=patterns, rest=node.rest)

    def visit_MatchClass(self, node: MatchClass, ctx: Any = None) -> ast.MatchClass:
        cls = self.visit(node.cls)
        patterns = [self.visit(p) for p in node.patterns]
        kwd_patterns = [self.visit(p) for p in node.kwd_patterns]
        return ast.MatchClass(
            cls=cls, patterns=patterns, kwd_attrs=node.kwd_attrs, kwd_patterns=kwd_patterns
        )
