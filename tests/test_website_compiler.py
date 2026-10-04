"""
Tests for JugaadLang website online compiler bundle and transpiler pipeline.
Verifies GitHub Issue #114 requirements.
"""

from __future__ import annotations

import ast
import base64
import io
import sys
import types
import zipfile
from typing import Any

from scripts.build_website_bundle import OUTPUT_FILE, build_bundle


def setup_rich_shim() -> None:
    """Ensure rich shim is active in sys.modules if rich is not installed."""
    if "rich" in sys.modules:
        return

    rich = types.ModuleType("rich")
    rich_console = types.ModuleType("rich.console")

    class SimpleCapture:
        def __init__(self, console: Any) -> None:
            self.console = console
            self.lines: list[str] = []

        def __enter__(self) -> SimpleCapture:
            self.orig_print = self.console.print
            self.lines = []

            def cap_print(*args: Any, **kwargs: Any) -> None:
                import re

                text = " ".join(str(a) for a in args)
                clean = re.sub(r"\[/?[a-zA-Z0-9_ #]+\]", "", text)
                self.lines.append(clean)

            self.console.print = cap_print
            return self

        def __exit__(self, *args: Any) -> None:
            self.console.print = self.orig_print

        def get(self) -> str:
            return "\n".join(self.lines)

    class ConsoleShim:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def capture(self) -> SimpleCapture:
            return SimpleCapture(self)

        def print(self, *args: Any, **kwargs: Any) -> None:
            import re

            text = " ".join(str(a) for a in args)
            clean = re.sub(r"\[/?[a-zA-Z0-9_ #]+\]", "", text)
            print(clean)

    rich_console.Console = ConsoleShim  # type: ignore[attr-defined]
    rich.console = rich_console  # type: ignore[attr-defined]
    sys.modules["rich"] = rich
    sys.modules["rich.console"] = rich_console


def run_pipeline(source: str, filename: str = "program.jug") -> dict[str, Any]:
    """Browser runner emulation."""
    setup_rich_shim()

    from jugaadlang.errors.messages import format_error
    from jugaadlang.lexer.lexer import Lexer
    from jugaadlang.parser.parser import Parser
    from jugaadlang.runtime.interpreter import JugaadInterpreter
    from jugaadlang.transformer.to_python import JugaadToPythonTransformer

    # Phase 1: Transpilation
    try:
        lexer = Lexer(source, filename)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename, source)
        ast_mod = parser.parse()
        transformer = JugaadToPythonTransformer(filename)
        py_ast = transformer.transform(ast_mod)
        py_source = ast.unparse(py_ast)
    except Exception as e:
        err_msg = format_error(e, source, filename)
        return {
            "phase": "compile",
            "success": False,
            "py_source": None,
            "output": "",
            "error": err_msg,
        }

    # Phase 2: Execution
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    out_buf = io.StringIO()
    err_buf = io.StringIO()
    sys.stdout = out_buf
    sys.stderr = err_buf

    try:
        interp = JugaadInterpreter(filename=filename)
        code_obj = compile(py_ast, filename, "exec")
        exec(code_obj, interp.globals, interp.globals)
        return {
            "phase": "complete",
            "success": True,
            "py_source": py_source,
            "output": out_buf.getvalue(),
            "error": err_buf.getvalue(),
        }
    except Exception as e:
        err_msg = format_error(e, source, filename)
        return {
            "phase": "runtime",
            "success": False,
            "py_source": py_source,
            "output": out_buf.getvalue(),
            "error": err_msg,
        }
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def test_bundle_generation_and_contents() -> None:
    """Verify scripts/build_website_bundle.py produces a valid, extractable zip bundle."""
    build_bundle()
    assert OUTPUT_FILE.endswith("jugaad_bundle.js")

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    prefix = 'window.JUGAADLANG_ZIP_BASE64 = "'
    assert prefix in content
    start = content.index(prefix) + len(prefix)
    end = content.rindex('";')
    b64_str = content[start:end]

    zip_bytes = base64.b64decode(b64_str)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = zf.namelist()
        # Verify essential compiler modules are present
        assert "jugaadlang/__init__.py" in names
        assert "jugaadlang/lexer/lexer.py" in names
        assert "jugaadlang/parser/parser.py" in names
        assert "jugaadlang/transformer/to_python.py" in names
        assert "jugaadlang/runtime/interpreter.py" in names
        assert "jugaadlang/stdlib/ganit.py" in names
        assert "jugaadlang/stdlib/paath.py" in names


def test_transpile_and_run_hello_world() -> None:
    """Verify basic compilation and execution of a .jug program."""
    code = 'bolo("Namaste Duniya!")'
    res = run_pipeline(code)
    assert res["success"] is True
    assert res["phase"] == "complete"
    assert "print('Namaste Duniya!')" in res["py_source"]
    assert "Namaste Duniya!" in res["output"]
    assert not res["error"]


def test_transpile_and_run_variables_and_loops() -> None:
    """Verify variables, loops (ghumo), and conditional logic."""
    code = """
naam = "Jugaad"
ghumo i mein range(1, 4):
    agar i == 2:
        bolo(naam + " " + shabd(i))
"""
    res = run_pipeline(code)
    assert res["success"] is True
    assert "for i in range(1, 4):" in res["py_source"]
    assert "Jugaad 2" in res["output"]


def test_transpile_and_run_functions() -> None:
    """Verify function definition (banao) and calling."""
    code = """
banao jod(a, b):
    wapas a + b

bolo(jod(10, 25))
"""
    res = run_pipeline(code)
    assert res["success"] is True
    assert "def jod(a, b):" in res["py_source"]
    assert "35" in res["output"]


def test_transpile_and_run_stdlib_ganit() -> None:
    """Verify importing and using stdlib modules (ganit)."""
    code = """
lao ganit
ans = ganit.sqrt(64)
bolo("Root:", ans)
"""
    res = run_pipeline(code)
    assert res["success"] is True
    assert "import ganit" in res["py_source"]
    assert "Root: 8.0" in res["output"]


def test_compilation_error_handling() -> None:
    """Verify syntax/parse errors return phase='compile' with formatted error."""
    invalid_code = "agar 10 > 5"  # Missing colon and block
    res = run_pipeline(invalid_code)
    assert res["success"] is False
    assert res["phase"] == "compile"
    assert res["py_source"] is None
    assert "Gadbad" in res["error"] or "Bhai kya likh diya" in res["error"]


def test_runtime_error_handling() -> None:
    """Verify runtime errors return phase='runtime' and retain py_source."""
    runtime_err_code = """
bolo("Pehle chal gaya")
bolo(kisi_ne_declare_nahi_kiya)
"""
    res = run_pipeline(runtime_err_code)
    assert res["success"] is False
    assert res["phase"] == "runtime"
    assert res["py_source"] is not None
    assert "Pehle chal gaya" in res["output"]
    assert "kisi_ne_declare_nahi_kiya" in res["error"]
    assert "dhundte dhundte thak gaya" in res["error"]


def test_empty_source() -> None:
    """Verify empty source executes cleanly without errors."""
    res = run_pipeline("")
    assert res["success"] is True
    assert res["phase"] == "complete"
    assert res["output"] == ""
    assert res["error"] == ""
