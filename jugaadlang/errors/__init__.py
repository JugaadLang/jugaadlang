# jugaadlang/errors/__init__.py
from .messages import (
    FUNNY_ERRORS,
    JugaadError,
    JugaadNameError,
    JugaadRuntimeError,
    JugaadSyntaxError,
    JugaadTypeError,
    JugaadZeroDivisionError,
    format_error,
    format_syntax_error,
)

__all__ = [
    "format_error",
    "format_syntax_error",
    "JugaadError",
    "JugaadSyntaxError",
    "JugaadRuntimeError",
    "JugaadNameError",
    "JugaadTypeError",
    "JugaadZeroDivisionError",
    "FUNNY_ERRORS",
]
