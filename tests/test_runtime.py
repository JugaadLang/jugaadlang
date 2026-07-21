"""
Tests for JugaadLang Runtime/Interpreter.
"""

import os

import pytest

from jugaadlang.runtime.interpreter import JugaadInterpreter


def test_interpreter_exec():
    interpreter = JugaadInterpreter()
    interpreter.run("x = 5\ny = x + 10")
    assert interpreter.globals["x"] == 5
    assert interpreter.globals["y"] == 15


def test_interpreter_eval_expr():
    interpreter = JugaadInterpreter()
    res = interpreter.run_expression("10 * 2 + 5")
    assert res == 25


def test_interpreter_builtins(capsys):
    interpreter = JugaadInterpreter()

    interpreter.run("chai()")
    captured = capsys.readouterr()
    assert "Chai ready hai" in captured.out

    interpreter.run("motivation()")
    captured = capsys.readouterr()
    assert "Keep coding" in captured.out

    interpreter.run("ghaas_chhoo()")
    captured = capsys.readouterr()
    assert "Bahar jao" in captured.out


def test_interpreter_stdlib():
    interpreter = JugaadInterpreter()
    interpreter.run("lao ganit\nx = ganit.sqrt(16)")
    assert interpreter.globals["x"] == 4.0


def test_class_inheritance():
    interpreter = JugaadInterpreter()
    code = """
ustad Parent:
    banao shuru(khud, val):
        khud.val = val
    banao show(khud):
        wapas khud.val

ustad Child(Parent):
    banao show_double(khud):
        wapas khud.show() * 2

c = Child(10)
res_val = c.show_double()
"""
    interpreter.run(code)
    assert interpreter.globals["res_val"] == 20


def test_comprehensions_and_loops():
    interpreter = JugaadInterpreter()
    code = """
# List comprehension
vals = [x * 2 ghumo x mein range(5)]
# Dict comprehension
d_vals = {x: x * 3 ghumo x mein range(3)}
# Set comprehension
s_vals = {x ghumo x mein range(3)}
# Ternary expression
res = "yes" agar sahi warna "no"
"""
    interpreter.run(code)
    assert interpreter.globals["vals"] == [0, 2, 4, 6, 8]
    assert interpreter.globals["d_vals"] == {0: 0, 1: 3, 2: 6}
    assert interpreter.globals["s_vals"] == {0, 1, 2}
    assert interpreter.globals["res"] == "yes"


def test_try_except_runtime():
    interpreter = JugaadInterpreter()
    code = """
caught = galat
koshish:
    x = 10 / 0
gadbad ZeroDivisionError:
    caught = sahi
"""
    interpreter.run(code)
    assert interpreter.globals["caught"] is True


def test_jugaad_orm():
    # Clean up DBs before start
    for db in ("jugaad.db", "test_jugaad.db"):
        if os.path.exists(db):
            os.remove(db)

    interpreter = JugaadInterpreter()
    code = """
lao database
database.Model._db_path = "test_jugaad.db"

ustad Person(database.Model):
    name = database.String()
    age = database.Integer()

Person.banao_table()
p1 = Person(name="Aman", age=25)
p1.bachao()

results = Person.filter(name="Aman")
res_len = len(results)
res_name = results[0].name
res_age = results[0].age
"""
    try:
        interpreter.run(code)
        assert interpreter.globals["res_len"] == 1
        assert interpreter.globals["res_name"] == "Aman"
        assert interpreter.globals["res_age"] == 25
    finally:
        # Clean up test DB
        for db in ("jugaad.db", "test_jugaad.db"):
            if os.path.exists(db):
                os.remove(db)


def test_jugaad_web():
    interpreter = JugaadInterpreter()
    code = """
lao web
@web.agar_route("/test")
banao hello_test():
    wapas "working"
"""
    interpreter.run(code)

    # Verify that the route was correctly registered in web default app
    import sys

    web_module = sys.modules["web"]
    assert "/test" in web_module._default_app.routes
    handler, methods = web_module._default_app.routes["/test"]
    assert handler() == "working"
    assert "GET" in methods


def test_pattern_matching_runtime():
    interpreter = JugaadInterpreter()
    code = """
banao test_match(x):
    agar_match x:
        kaand sahi:
            wapas "boolean true"
        kaand 1:
            wapas "one"
        kaand [a, b]:
            wapas "sequence of " + str(a) + " and " + str(b)
        kaand _:
            wapas "something else"

res1 = test_match(1)
res2 = test_match(sahi)
res3 = test_match([10, 20])
res4 = test_match("random")
"""
    interpreter.run(code)
    assert interpreter.globals["res1"] == "one"
    assert interpreter.globals["res2"] == "boolean true"
    assert interpreter.globals["res3"] == "sequence of 10 and 20"
    assert interpreter.globals["res4"] == "something else"


def test_lockfile_generation(tmp_path):
    import os
    import json
    from jugaadlang.package_manager.manager import JugaadPackageManager
    from unittest.mock import patch

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        with patch("subprocess.run"), patch("importlib.metadata.version", return_value="1.2.3"):
            JugaadPackageManager.install("dummy-pkg")

            lock_file = tmp_path / "jug.lock"
            assert lock_file.exists()
            with open(lock_file, "r") as f:
                data = json.load(f)
            assert "packages" in data
            assert data["packages"]["dummy-pkg"] == "1.2.3"

            JugaadPackageManager.remove("dummy-pkg")
            with open(lock_file, "r") as f:
                data = json.load(f)
            assert "dummy-pkg" not in data["packages"]
    finally:
        os.chdir(old_cwd)


def test_package_manager_exits_on_pip_failure():
    import subprocess
    from unittest.mock import patch

    from jugaadlang.package_manager.manager import JugaadPackageManager

    err = subprocess.CalledProcessError(1, ["pip", "install", "fake"], stderr="not found")
    with patch("subprocess.run", side_effect=err):
        try:
            JugaadPackageManager.install("totally-fake-package-xyz")
            assert False, "expected SystemExit"
        except SystemExit as exc:
            assert exc.code == 1


def test_hindi_builtins():
    interpreter = JugaadInterpreter()
    code = """
val_abs = maan(-10)
val_all = sab([sahi, sahi, sahi])
val_any = koi_bhi([galat, sahi, galat])
val_len = lambaee([1, 2, 3])
val_max = adhiktam([5, 10, 2])
val_min = nyuntam([5, 10, 2])
val_sum = yog([1, 2, 3])
val_str = shabd(123)
val_type = prakar("test") == shabd
"""
    interpreter.run(code)
    assert interpreter.globals["val_abs"] == 10
    assert interpreter.globals["val_all"] is True
    assert interpreter.globals["val_any"] is True
    assert interpreter.globals["val_len"] == 3
    assert interpreter.globals["val_max"] == 10
    assert interpreter.globals["val_min"] == 2
    assert interpreter.globals["val_sum"] == 6
    assert interpreter.globals["val_str"] == "123"
    assert interpreter.globals["val_type"] is True


# ── Security: RCE vector regression tests ─────────────────────────────────


def test_chalao_exec_is_removed():
    """Verify 'chalao' (formerly exec) is no longer available."""
    interpreter = JugaadInterpreter()
    with pytest.raises(Exception):
        interpreter.run('chalao("x = 1")')


def test_kholo_open_is_removed():
    """Verify 'kholo' (formerly open) is no longer available."""
    interpreter = JugaadInterpreter()
    with pytest.raises(Exception):
        interpreter.run('kholo("/etc/passwd")')


def test_builtins_excludes_dangerous():
    """Verify that dangerous builtins are not accessible from JugaadLang."""
    interpreter = JugaadInterpreter()
    for dangerous in ("exec", "eval", "compile", "open"):
        # Attempt to access each dangerous builtin directly
        with pytest.raises(Exception, match=dangerous):
            interpreter.run_expression(dangerous)


def test_builtins_includes_safe():
    """Verify that safe builtins remain accessible from JugaadLang."""
    interpreter = JugaadInterpreter()
    interpreter.run_expression("maan(-10)")
    interpreter.run_expression("lambaee([1, 2, 3])")
    interpreter.run_expression("yog([1, 2, 3])")
    interpreter.run_expression("prakar(sahi)")


def test_shell_chalao_uses_shell_false():
    """Verify shell_chalao uses shell=False to prevent injection."""
    from jugaadlang.stdlib.tantra import shell_chalao
    ret = shell_chalao("python --version")
    assert ret == 0


def test_cli_doctor():
    from click.testing import CliRunner
    from jug_cli.main import doctor

    runner = CliRunner()
    result = runner.invoke(doctor)
    assert result.exit_code == 0
    assert "JugaadLang Doctor" in result.output
    assert "Sab theek hai" in result.output


def test_cli_typecheck(tmp_path):
    from click.testing import CliRunner
    from jug_cli.main import typecheck

    # 1. Test valid file
    file_ok = tmp_path / "test_ok.jug"
    file_ok.write_text("naam: shabd = 'Aaman'\numar: purnank = 20\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(typecheck, [str(file_ok)])
    assert result.exit_code == 0
    assert "Type check passed" in result.output

    # 2. Test invalid file (type mismatch)
    file_err = tmp_path / "test_err.jug"
    file_err.write_text("naam: shabd = 'Aaman'\numar: purnank = 'twenty'\n", encoding="utf-8")
    result = runner.invoke(typecheck, [str(file_err)])
    assert result.exit_code != 0
    assert "Type check failed" in result.output
    assert "Incompatible types in assignment" in result.output


def test_import_jaise_alias():
    interpreter = JugaadInterpreter()
    interpreter.run("lao ganit jaise g\nx = g.sqrt(16)")
    assert interpreter.globals["x"] == 4.0

    interpreter.run("""
koshish:
    y = 1 / 0
gadbad ZeroDivisionError jaise e:
    err = "zero"
""")
    assert interpreter.globals["err"] == "zero"


def test_all_keywords_covered():
    interpreter = JugaadInterpreter()

    # 1. Test ke_saath (with) context manager
    interpreter.run("""
ustad Manager:
    banao __enter__(khud):
        wapas 42
    banao __exit__(khud, exc_type, exc_val, exc_tb):
        theek_hai

ke_saath Manager() jaise val:
    res = val
""")
    assert interpreter.globals["res"] == 42

    # 2. Test pakka (assert)
    interpreter.run("pakka sahi, 'it is true'")

    # 3. Test hatao (del)
    interpreter.run("""
x = 99
hatao x
""")
    assert "x" not in interpreter.globals

    # 4. Test gair_local (nonlocal)
    interpreter.run("""
banao outer():
    x = 10
    banao inner():
        gair_local x
        x = 20
    inner()
    wapas x
res = outer()
""")
    assert interpreter.globals["res"] == 20
