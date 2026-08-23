"""
Tests for JugaadLang Standard Library modules.

Covers all 18 stdlib modules accessed through the interpreter or directly
when name collisions prevent interpreter import (e.g., json).
"""

from __future__ import annotations

import datetime
import hashlib
import os
import sys
from pathlib import Path
from typing import Any

import pytest

from jugaadlang.runtime.interpreter import JugaadInterpreter


# ── Helpers ────────────────────────────────────────────────────────────────


@pytest.fixture
def interpreter() -> JugaadInterpreter:
    """Provide a fresh interpreter per test."""
    return JugaadInterpreter()


def import_module_via_interpreter(
    interp: JugaadInterpreter, module_name: str
) -> None:
    """Import a stdlib module into the interpreter's global scope."""
    interp.run(f"lao {module_name}")


def _norm_path(p: Path) -> str:
    """Return a forward-slash path string safe for embedding in JugaadLang source.

    On Windows, pytest's tmp_path produces backslashes which get mangled
    when embedded in Python f-strings (e.g. \\t becomes tab). Using
    forward slashes avoids this.
    """
    return p.as_posix()


# ═══════════════════════════════════════════════════════════════════════════
# 1. Ganit (Mathematics)
# ═══════════════════════════════════════════════════════════════════════════


class TestGanit:
    """Tests for jug.stdlib.ganit — math wrappers."""

    def test_constants(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "ganit")
        interpreter.run("pi_val = ganit.pi")
        assert isinstance(interpreter.globals["pi_val"], float)
        interpreter.run("e_val = ganit.e")
        assert isinstance(interpreter.globals["e_val"], float)

    def test_sqrt(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "ganit")
        interpreter.run("x = ganit.sqrt(16)")
        assert interpreter.globals["x"] == 4.0

    def test_square(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "ganit")
        interpreter.run("x = ganit.square(5)")
        assert interpreter.globals["x"] == 25

    def test_cube(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "ganit")
        interpreter.run("x = ganit.cube(3)")
        assert interpreter.globals["x"] == 27

    def test_sin(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "ganit")
        interpreter.run("x = ganit.sin(0)")
        assert interpreter.globals["x"] == 0.0

    def test_factorial(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "ganit")
        interpreter.run("x = ganit.factorial(5)")
        assert interpreter.globals["x"] == 120


# ═══════════════════════════════════════════════════════════════════════════
# 2. Samay (Date/Time)
# ═══════════════════════════════════════════════════════════════════════════


class TestSamay:
    """Tests for jug.stdlib.samay — date/time wrappers."""

    def test_abhibhi_type(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "samay")
        interpreter.run("now = samay.abhibhi()")
        assert isinstance(interpreter.globals["now"], datetime.datetime)

    def test_aaj_type(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "samay")
        interpreter.run("today = samay.aaj()")
        assert isinstance(interpreter.globals["today"], datetime.date)

    def test_format_karo(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "samay")
        interpreter.run(
            "now = samay.abhibhi()\n"
            'formatted = samay.format_karo(now, "%Y")\n'
        )
        formatted: str = interpreter.globals["formatted"]
        assert formatted.isdigit() and len(formatted) == 4


# ═══════════════════════════════════════════════════════════════════════════
# 3. Crypto (Hash / Base64)
# ═══════════════════════════════════════════════════════════════════════════


class TestCrypto:
    """Tests for jug.stdlib.crypto — hashing & encoding."""

    def test_sha256(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "crypto")
        interpreter.run('h = crypto.sha256("hello")')
        expected = hashlib.sha256(b"hello").hexdigest()
        assert interpreter.globals["h"] == expected

    def test_md5(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "crypto")
        interpreter.run('h = crypto.md5("hello")')
        expected = hashlib.md5(b"hello").hexdigest()
        assert interpreter.globals["h"] == expected

    def test_base64_encode(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "crypto")
        interpreter.run('enc = crypto.base64_encode("hello")')
        assert interpreter.globals["enc"] == "aGVsbG8="

    def test_base64_decode(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "crypto")
        interpreter.run('dec = crypto.base64_decode("aGVsbG8=")')
        assert interpreter.globals["dec"] == "hello"


# ═══════════════════════════════════════════════════════════════════════════
# 4. Faili (File System Operations)
# ═══════════════════════════════════════════════════════════════════════════


class TestFaili:
    """Tests for jug.stdlib.faili — file system operations."""

    def test_likho_padho(
        self, tmp_path: Path, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "faili")
        test_file = _norm_path(tmp_path / "test.txt")
        interpreter.run(f'faili.likho("{test_file}", "Hello JugaadLang!")')
        assert (tmp_path / "test.txt").read_text(encoding="utf-8") == "Hello JugaadLang!"
        interpreter.run(f'content = faili.padho("{test_file}")')
        assert interpreter.globals["content"] == "Hello JugaadLang!"

    def test_jodo(self, tmp_path: Path, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "faili")
        test_file = _norm_path(tmp_path / "append.txt")
        (tmp_path / "append.txt").write_text("line1\n", encoding="utf-8")
        interpreter.run(f'faili.jodo("{test_file}", "line2\\n")')
        assert (tmp_path / "append.txt").read_text(encoding="utf-8") == "line1\nline2\n"

    def test_hai_kya(
        self, tmp_path: Path, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "faili")
        test_file = _norm_path(tmp_path / "exists.txt")
        (tmp_path / "exists.txt").write_text("hi", encoding="utf-8")
        interpreter.run(f'exists = faili.hai_kya("{test_file}")')
        assert interpreter.globals["exists"] is True
        interpreter.run(
            f'no_exist = faili.hai_kya("{_norm_path(tmp_path / "nope.txt")}")'
        )
        assert interpreter.globals["no_exist"] is False

    def test_list_karo(
        self, tmp_path: Path, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "faili")
        (tmp_path / "a.txt").write_text("a", encoding="utf-8")
        (tmp_path / "b.txt").write_text("b", encoding="utf-8")
        interpreter.run(
            f'items = faili.list_karo("{_norm_path(tmp_path)}")\n'
            "items = kramwar(items)"
        )
        assert interpreter.globals["items"] == ["a.txt", "b.txt"]

    def test_folder_banao(
        self, tmp_path: Path, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "faili")
        new_dir = _norm_path(tmp_path / "new_folder")
        interpreter.run(f'faili.folder_banao("{new_dir}")')
        assert (tmp_path / "new_folder").is_dir()

    def test_mitao_file(
        self, tmp_path: Path, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "faili")
        test_file = _norm_path(tmp_path / "delete_me.txt")
        (tmp_path / "delete_me.txt").write_text("bye", encoding="utf-8")
        interpreter.run(f'faili.mitao("{test_file}")')
        assert not (tmp_path / "delete_me.txt").exists()


# ═══════════════════════════════════════════════════════════════════════════
# 5. JSON (direct Python import — name collides with stdlib json)
# ═══════════════════════════════════════════════════════════════════════════


class TestJsonModule:
    """Tests for jug.stdlib.json via direct Python import.

    The module name 'json' collides with Python's stdlib json module,
    so interpreter import resolves to the wrong one. We test directly.
    """

    def test_banao_string(self) -> None:
        from jugaadlang.stdlib.json import banao_string

        result = banao_string({"a": 1})
        assert result == '{"a": 1}'

    def test_banao_string_with_indent(self) -> None:
        from jugaadlang.stdlib.json import banao_string

        result = banao_string({"a": 1}, 2)
        assert '"a":' in result

    def test_banao_object(self) -> None:
        from jugaadlang.stdlib.json import banao_object

        obj = banao_object('{"x": 10}')
        assert obj == {"x": 10}


# ═══════════════════════════════════════════════════════════════════════════
# 6. Tantra (System / Environment)
# ═══════════════════════════════════════════════════════════════════════════


class TestTantra:
    """Tests for jug.stdlib.tantra — system attributes."""

    def test_platform_attribute(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "tantra")
        interpreter.run("plat = tantra.platform")
        assert interpreter.globals["plat"] == sys.platform

    def test_pid(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "tantra")
        interpreter.run("proc_id = tantra.pid()")
        assert interpreter.globals["proc_id"] == os.getpid()

    def test_folder_ka_naam(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "tantra")
        interpreter.run("cwd = tantra.folder_ka_naam()")
        assert interpreter.globals["cwd"] == os.getcwd()


# ═══════════════════════════════════════════════════════════════════════════
# 7. Chai (Fun — Tea Break)
# ═══════════════════════════════════════════════════════════════════════════


class TestChai:
    """Tests for jug.stdlib.chai — tea break module."""

    def test_piyo(self, capsys: Any, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "chai")
        interpreter.run("chai.piyo()")
        captured = capsys.readouterr()
        assert "Chai" in captured.out

    def test_status(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "chai")
        interpreter.run("s = chai.status()")
        s = interpreter.globals["s"]
        assert isinstance(s, str)
        assert "chai" in s.lower() or "coding" in s


# ═══════════════════════════════════════════════════════════════════════════
# 8. Dev (Developer Humor)
# ═══════════════════════════════════════════════════════════════════════════


class TestDev:
    """Tests for jug.stdlib.dev — developer humor tools."""

    def test_fake_commit(
        self, capsys: Any, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "dev")
        interpreter.run("msg = dev.fake_commit()")
        assert isinstance(interpreter.globals["msg"], str)
        assert len(interpreter.globals["msg"]) > 0

    def test_blame_someone_else(
        self, capsys: Any, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "dev")
        interpreter.run("excuse = dev.blame_someone_else()")
        assert isinstance(interpreter.globals["excuse"], str)
        assert len(interpreter.globals["excuse"]) > 0


# ═══════════════════════════════════════════════════════════════════════════
# 9. Fortune (Developer Fortune Teller)
# ═══════════════════════════════════════════════════════════════════════════


class TestFortune:
    """Tests for jug.stdlib.fortune — fortune teller."""

    def test_batao(self, capsys: Any, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "fortune")
        interpreter.run("fortune.batao()")
        captured = capsys.readouterr()
        assert len(captured.out) > 0


# ═══════════════════════════════════════════════════════════════════════════
# 10. Motivation (Developer Motivation)
# ═══════════════════════════════════════════════════════════════════════════


class TestMotivation:
    """Tests for jug.stdlib.motivation — dev motivation."""

    def test_gyan(self, capsys: Any, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "motivation")
        interpreter.run("motivation.gyan()")
        captured = capsys.readouterr()
        assert len(captured.out) > 0


# ═══════════════════════════════════════════════════════════════════════════
# 11. Love (Romance Humor)
# ═══════════════════════════════════════════════════════════════════════════


class TestLove:
    """Tests for jug.stdlib.love — romance humor."""

    def test_flirt(self, capsys: Any, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "love")
        interpreter.run("line = love.flirt()")
        assert isinstance(interpreter.globals["line"], str)
        assert len(interpreter.globals["line"]) > 0

    def test_date_idea(
        self, capsys: Any, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "love")
        interpreter.run("idea = love.date_idea()")
        assert isinstance(interpreter.globals["idea"], str)
        assert len(interpreter.globals["idea"]) > 0

    def test_sorry_message(
        self, capsys: Any, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "love")
        interpreter.run('msg = love.sorry_message("Dev")')
        msg = interpreter.globals["msg"]
        assert isinstance(msg, str)
        assert "Dev" in msg or "dev" in msg.lower()


# ═══════════════════════════════════════════════════════════════════════════
# 12. Student (Student Humor)
# ═══════════════════════════════════════════════════════════════════════════


class TestStudent:
    """Tests for jug.stdlib.student — student humor."""

    def test_bahana(
        self, capsys: Any, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "student")
        interpreter.run("excuse = student.bahana()")
        assert isinstance(interpreter.globals["excuse"], str)
        assert len(interpreter.globals["excuse"]) > 0

    def test_cgpa_calc(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "student")
        interpreter.run("cgpa = student.cgpa_calc([8, 9, 7])")
        assert interpreter.globals["cgpa"] == 8.0


# ═══════════════════════════════════════════════════════════════════════════
# 13. Jokes & Memes
# ═══════════════════════════════════════════════════════════════════════════


class TestJokes:
    """Tests for jug.stdlib.jokes."""

    def test_sunao(self, capsys: Any, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "jokes")
        interpreter.run("jokes.sunao()")
        captured = capsys.readouterr()
        assert len(captured.out) > 0


class TestMemes:
    """Tests for jug.stdlib.memes."""

    def test_dikhao(
        self, capsys: Any, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "memes")
        interpreter.run("memes.dikhao()")
        captured = capsys.readouterr()
        assert len(captured.out) > 0


# ═══════════════════════════════════════════════════════════════════════════
# 14. Database (JugaadORM — SQLite ORM)
# ═══════════════════════════════════════════════════════════════════════════


class TestDatabase:
    """Tests for jug.stdlib.database — JugaadORM."""

    _DB_DIR_VAR: str = ""

    @pytest.fixture(autouse=True)
    def _cleanup(self, tmp_path: Path) -> None:
        yield
        for f in tmp_path.glob("*.db"):
            try:
                f.unlink()
            except PermissionError:
                pass  # Windows file lock — skip

    def test_field_types(self) -> None:
        from jugaadlang.stdlib.database import String, Integer, Float, Boolean

        s = String()
        assert s.sql_type == "TEXT"
        i = Integer()
        assert i.sql_type == "INTEGER"
        f = Float()
        assert f.sql_type == "REAL"
        b = Boolean()
        assert b.sql_type == "INTEGER"

    def _run_with_db(
        self, interpreter: JugaadInterpreter, tmp_path: Path, code: str
    ) -> None:
        """Run interpreter code with a unique per-test DB path prepended."""
        db_path = _norm_path(tmp_path / "test.db")
        full_code = f'database.Model._db_path = "{db_path}"\n' + code
        interpreter.run(full_code)

    def test_model_create_and_query(
        self, tmp_path: Path, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "database")
        self._run_with_db(
            interpreter,
            tmp_path,
            """
ustad Person(database.Model):
    name = database.String()
    age = database.Integer()

Person.banao_table()
p1 = Person(name="Amit", age=30)
p1.bachao()

results = Person.filter(name="Amit")
res_len = lambaee(results)
res_name = results[0].name
res_age = results[0].age
""",
        )
        assert interpreter.globals["res_len"] == 1
        assert interpreter.globals["res_name"] == "Amit"
        assert interpreter.globals["res_age"] == 30

    def test_model_update(
        self, tmp_path: Path, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "database")
        self._run_with_db(
            interpreter,
            tmp_path,
            """
ustad Item(database.Model):
    name = database.String()
    qty = database.Integer()

Item.banao_table()
i1 = Item(name="widget", qty=5)
i1.bachao()
i1.qty = 10
i1.bachao()

results = Item.filter(name="widget")
updated_qty = results[0].qty
""",
        )
        assert interpreter.globals["updated_qty"] == 10

    def test_model_sab(
        self, tmp_path: Path, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "database")
        self._run_with_db(
            interpreter,
            tmp_path,
            """
ustad Task(database.Model):
    title = database.String()

Task.banao_table()
ghumo i mein range(3):
    t = Task(title="task " + shabd(i))
    t.bachao()

all_tasks = Task.sab()
total = lambaee(all_tasks)
""",
        )
        assert interpreter.globals["total"] == 3


# ═══════════════════════════════════════════════════════════════════════════
# 15. Web (JugaadWeb — micro web framework)
# ═══════════════════════════════════════════════════════════════════════════


class TestWeb:
    """Tests for jug.stdlib.web — JugaadWeb (route registration only, no server)."""

    @property
    def _web_module(self) -> Any:
        import sys
        return sys.modules["web"]

    def test_route_registration(self, interpreter: JugaadInterpreter) -> None:
        import_module_via_interpreter(interpreter, "web")
        interpreter.run(
            """
@web.agar_route("/ping")
banao ping():
    wapas "pong"
"""
        )
        web_mod = self._web_module
        assert "/ping" in web_mod._default_app.routes
        handler, methods = web_mod._default_app.routes["/ping"]
        assert handler() == "pong"
        assert "GET" in methods

    def test_route_with_custom_method(
        self, interpreter: JugaadInterpreter
    ) -> None:
        import_module_via_interpreter(interpreter, "web")
        interpreter.run(
            """
@web.agar_route("/data", ["POST"])
banao create():
    wapas "created"
"""
        )
        web_mod = self._web_module
        assert "/data" in web_mod._default_app.routes
        _, methods = web_mod._default_app.routes["/data"]
        assert "POST" in methods


# ═══════════════════════════════════════════════════════════════════════════
# 16. Module import smoke tests (modules with external deps)
# ═══════════════════════════════════════════════════════════════════════════


def test_catfacts_module_importable() -> None:
    """Verify catfacts module can be imported without error."""
    from jugaadlang.stdlib import catfacts  # noqa: F401


def test_whatsapp_module_importable() -> None:
    """Verify whatsapp module can be imported without error."""
    from jugaadlang.stdlib import whatsapp  # noqa: F401


# ═══════════════════════════════════════════════════════════════════════════
# 17. Crypto module re-export test
# ═══════════════════════════════════════════════════════════════════════════


def test_crypto_module_re_exports() -> None:
    """Verify crypto_module.py re-exports everything from crypto.py."""
    from jugaadlang.stdlib import crypto_module

    assert hasattr(crypto_module, "sha256")
    assert hasattr(crypto_module, "md5")
    assert hasattr(crypto_module, "base64_encode")
    assert hasattr(crypto_module, "base64_decode")
