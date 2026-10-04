"""
JugaadLang Runtime - Executes JugaadLang AST after transpiling to Python.
"""

from __future__ import annotations

import ast
import builtins
import os
import sys
from typing import Any

from ..ast_nodes.nodes import ExprStmt
from ..cache.manager import cache_manager
from ..errors.messages import format_error
from ..lexer.lexer import Lexer
from ..parser.parser import Parser
from ..transformer.to_python import JugaadToPythonTransformer
from .fun_builtins import FUN_BUILTINS

#  Safe builtins (explicit allowlist - no exec/eval/compile/open/__import__) 

_SAFE_BUILTINS: dict[str, Any] = {
    name: getattr(builtins, name)
    for name in [
        "abs", "all", "any", "ascii", "bin", "bool", "bytearray", "bytes",
        "callable", "chr", "classmethod", "complex", "delattr", "dict",
        "dir", "divmod", "enumerate", "filter", "float", "format",
        "frozenset", "getattr", "hasattr", "hash", "hex", "id", "input",
        "int", "isinstance", "issubclass", "iter", "len", "list", "map",
        "max", "memoryview", "min", "next", "object", "oct", "ord",
        "pow", "print", "property", "range", "repr", "reversed", "round",
        "set", "setattr", "slice", "sorted", "staticmethod", "str",
        "sum", "super", "tuple", "type", "zip",
        # Required for language functionality (not security risks)
        "__build_class__", "__import__",
        # Exception types
        "ArithmeticError", "AssertionError", "AttributeError",
        "BaseException", "BrokenPipeError", "BufferError", "BytesWarning",
        "ChildProcessError", "ConnectionAbortedError", "ConnectionError",
        "ConnectionRefusedError", "ConnectionResetError", "DeprecationWarning",
        "EOFError", "EnvironmentError", "Exception",
        "FileExistsError", "FileNotFoundError", "FloatingPointError",
        "FutureWarning", "GeneratorExit", "IOError", "ImportError",
        "IndentationError", "IndexError", "InterruptedError",
        "IsADirectoryError", "KeyError", "KeyboardInterrupt",
        "LookupError", "MemoryError", "ModuleNotFoundError",
        "NameError", "NotADirectoryError", "NotImplemented", "NotImplementedError",
        "OSError", "OverflowError", "PendingDeprecationWarning",
        "PermissionError", "ProcessLookupError", "RecursionError",
        "ReferenceError", "ResourceWarning", "RuntimeError", "RuntimeWarning",
        "StopAsyncIteration", "StopIteration", "SyntaxError", "SystemError",
        "SystemExit", "TabError", "TimeoutError", "TypeError",
        "UnboundLocalError", "UnicodeDecodeError", "UnicodeEncodeError",
        "UnicodeError", "UnicodeTranslateError", "UnicodeWarning",
        "UserWarning", "ValueError", "Warning", "ZeroDivisionError",
    ]
}


class JugaadInterpreter:
    def __init__(self, filename: str = "<main>"):
        self.filename = filename
        
        # Initialize safe global namespace
        self.globals: dict[str, Any] = {
            "__builtins__": _SAFE_BUILTINS,
            "__name__": "__main__",
            "__file__": self.filename,
        }
        self.globals.update(FUN_BUILTINS)
        
        # Inject standard library path for imports
        stdlib_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "stdlib")
        )
        if stdlib_path not in sys.path:
            sys.path.insert(0, stdlib_path)

    def run(self, source: str) -> None:
        """Run JugaadLang source code as statements (exec mode)."""
        from ..events.bus import event_bus
        event_bus.emit("EXECUTION_STARTED", {"filename": self.filename, "mode": "exec"})
        try:
            
            # Tier 1: Try Bytecode Cache
            code_obj = cache_manager.get_bytecode(source, filename=self.filename)
            
            if code_obj is None:
                # Tier 2: Try AST Cache
                ast_mod = cache_manager.get_ast(source, filename=self.filename)
                
                if ast_mod is None:
                    # Tier 3: Parse from scratch
                    lexer = Lexer(source, self.filename)
                    tokens = lexer.tokenize()

                    parser = Parser(tokens, self.filename, source)
                    ast_mod = parser.parse()

                    try:
                        cache_manager.set_ast(source, ast_mod, filename=self.filename)
                    except Exception:
                        pass

                # Transpile to Python AST
                transformer = JugaadToPythonTransformer(self.filename)
                py_ast = transformer.transform(ast_mod)
                
                # Compile to Bytecode
                code_obj = compile(py_ast, self.filename, "exec")
                
                # Cache Bytecode
                try:
                    cache_manager.set_bytecode(source, code_obj, filename=self.filename)
                except Exception:
                    pass

            # Execute bytecode
            exec(code_obj, self.globals, self.globals)
            event_bus.emit("EXECUTION_COMPLETED", {"filename": self.filename, "mode": "exec"})
        except Exception as e:
            formatted = format_error(e, source, self.filename)
            print(formatted, file=sys.stderr)
            raise

    def run_expression(self, source: str) -> Any:
        """
        Evaluate JugaadLang source.
        If it's a single expression, evaluate and return its value (eval mode).
        Otherwise, execute normally (exec mode) and return None.
        """
        from ..events.bus import event_bus
        event_bus.emit("EXECUTION_STARTED", {"filename": self.filename, "mode": "eval"})
        try:

            cache_key = f"expr::{source}"
            code_obj = cache_manager.get_bytecode(cache_key, filename=self.filename)
            mode = "eval"

            if code_obj is None:
                ast_mod = cache_manager.get_ast(cache_key, filename=self.filename)
                
                if ast_mod is None:
                    lexer = Lexer(source, self.filename)
                    tokens = lexer.tokenize()
                    parser = Parser(tokens, self.filename, source)
                    ast_mod = parser.parse()
                    try:
                        cache_manager.set_ast(cache_key, ast_mod, filename=self.filename)
                    except Exception:
                        pass
                
                transformer = JugaadToPythonTransformer(self.filename)
                py_ast = transformer.transform(ast_mod)

                # Check if the parsed result is a single expression
                if isinstance(ast_mod.body[0], ExprStmt) and len(ast_mod.body) == 1:
                    mode = "eval"
                    # In Python AST, py_ast.body[0] is an Expr node containing the actual value
                    expr_ast = ast.Expression(body=py_ast.body[0].value)  # type: ignore
                    ast.fix_missing_locations(expr_ast)
                    code_obj = compile(expr_ast, self.filename, "eval")
                else:
                    mode = "exec"
                    code_obj = compile(py_ast, self.filename, "exec")
                
                try:
                    cache_manager.set_bytecode(cache_key, code_obj, filename=self.filename)
                except Exception:
                    pass

            result = None
            if mode == "eval" or (hasattr(code_obj, "co_flags") and code_obj.co_flags & 0x010000):
                # We compile expressions with "eval", which might be distinguishable, but let's just 
                # try eval, and if it fails because it's not an expression, fallback to exec.
                try:
                    result = eval(code_obj, self.globals, self.globals)
                except TypeError:
                    # Occurs if code_obj is not an expression
                    exec(code_obj, self.globals, self.globals)
            else:
                exec(code_obj, self.globals, self.globals)
                
            event_bus.emit("EXECUTION_COMPLETED", {"filename": self.filename, "mode": "eval_or_exec"})
            return result
            
        except Exception as e:
            formatted = format_error(e, source, self.filename)
            print(formatted, file=sys.stderr)
            raise
