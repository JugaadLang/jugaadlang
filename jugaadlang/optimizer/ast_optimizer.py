from __future__ import annotations

import dataclasses
from typing import Any, List

from ..ast_nodes.nodes import (
    ASTNode,
    BinOp,
    BoolOp,
    Constant,
    Expr,
    If,
    Stmt,
    UnaryOp,
)


class JugaadASTOptimizer:
    """
    AST Optimizer for JugaadLang.
    Performs Constant Folding and Dead Code Elimination on the JugaadLang AST.
    """

    def optimize(self, node: ASTNode) -> ASTNode:
        """Main entry point to optimize an AST node."""
        return self.visit(node)

    def visit(self, node: Any) -> Any:
        """Recursively visits and optimizes AST nodes."""
        if isinstance(node, list):
            new_list = []
            for item in node:
                visited = self.visit(item)
                if visited is not None:
                    # If a single statement optimization returned a list of statements (e.g. If body)
                    if isinstance(visited, list):
                        new_list.extend(visited)
                    else:
                        new_list.append(visited)
            return new_list

        if not isinstance(node, ASTNode):
            return node

        # Visit all children first (bottom-up traversal)
        for field in dataclasses.fields(node):
            val = getattr(node, field.name)
            setattr(node, field.name, self.visit(val))

        # Now optimize this specific node if a method exists
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, None)
        if visitor:
            return visitor(node)
        
        return node

    def visit_BinOp(self, node: BinOp) -> Expr:
        """Constant folding for binary operations."""
        if isinstance(node.left, Constant) and isinstance(node.right, Constant):
            lval = node.left.value
            rval = node.right.value
            try:
                if node.op == '+': res = lval + rval
                elif node.op == '-': res = lval - rval
                elif node.op == '*': res = lval * rval
                elif node.op == '/': res = lval / rval
                elif node.op == '//': res = lval // rval
                elif node.op == '%': res = lval % rval
                elif node.op == '**': res = lval ** rval
                elif node.op == '<<': res = lval << rval
                elif node.op == '>>': res = lval >> rval
                elif node.op == '|': res = lval | rval
                elif node.op == '&': res = lval & rval
                elif node.op == '^': res = lval ^ rval
                else:
                    return node
                return Constant(value=res, line=node.line, col=node.col)
            except Exception:
                # E.g. division by zero; leave it for runtime error
                pass
        return node

    def visit_BoolOp(self, node: BoolOp) -> Expr:
        """Constant folding for boolean operations."""
        if all(isinstance(v, Constant) for v in node.values):
            try:
                if node.op == 'aur':
                    res = node.values[0].value
                    for v in node.values[1:]:
                        res = res and v.value
                elif node.op == 'ya':
                    res = node.values[0].value
                    for v in node.values[1:]:
                        res = res or v.value
                else:
                    return node
                return Constant(value=res, line=node.line, col=node.col)
            except Exception:
                pass
        return node

    def visit_UnaryOp(self, node: UnaryOp) -> Expr:
        """Constant folding for unary operations."""
        if isinstance(node.operand, Constant):
            val = node.operand.value
            try:
                if node.op == 'nahi': res = not val
                elif node.op == '+': res = +val
                elif node.op == '-': res = -val
                elif node.op == '~': res = ~val
                else:
                    return node
                return Constant(value=res, line=node.line, col=node.col)
            except Exception:
                pass
        return node

    def visit_If(self, node: If) -> Any:
        """Dead code elimination for If statements."""
        if isinstance(node.test, Constant):
            # If the condition resolves to True, return just the body.
            if bool(node.test.value):
                return node.body
            else:
                # If False, return the orelse branch (which may be empty).
                return node.orelse if node.orelse else []
        return node
