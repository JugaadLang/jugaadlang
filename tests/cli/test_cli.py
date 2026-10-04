import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from jug_cli.main import main


@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "JugaadLang" in result.output
    assert "Examples:" in result.output
    assert "jug run <file.jug>" in result.output
    assert "jug compile <file.jug>" in result.output
    assert "jug repl" in result.output
    assert "jug install <package>" in result.output
    assert "jug search <query>" in result.output
    assert "jug doctor" in result.output
    # Check that short help for install is cleanly displayed without truncation
    assert "Install a package or custom bundle." in result.output


def test_cli_help_short_flag(runner):
    result = runner.invoke(main, ['-h'])
    assert result.exit_code == 0
    assert "JugaadLang" in result.output
    assert "Examples:" in result.output


def test_cli_subcommand_help_examples(runner):
    for cmd, expected_example in [
        ('run', 'jug run hello.jug'),
        ('compile', 'jug compile hello.jug'),
        ('repl', 'jug repl'),
        ('install', 'jug install chai'),
        ('remove', 'jug remove chai'),
        ('update', 'jug update chai'),
        ('search', 'jug search chai'),
        ('new', 'jug new my_project'),
        ('check', 'jug check hello.jug'),
        ('typecheck', 'jug typecheck hello.jug'),
        ('doctor', 'jug doctor'),
    ]:
        result = runner.invoke(main, [cmd, '--help'])
        assert result.exit_code == 0
        assert "Examples:" in result.output
        assert expected_example in result.output

def test_cli_run(runner, tmp_path):
    jug_file = tmp_path / "hello.jug"
    jug_file.write_text("bolo('namaste')", encoding="utf-8")
    result = runner.invoke(main, ['run', str(jug_file)])
    assert result.exit_code == 0

def test_cli_run_non_existent(runner):
    result = runner.invoke(main, ['run', 'does_not_exist.jug'])
    assert result.exit_code != 0

def test_cli_compile(runner, tmp_path):
    jug_file = tmp_path / "hello.jug"
    jug_file.write_text("bolo('namaste')", encoding="utf-8")
    out_file = tmp_path / "hello.py"
    result = runner.invoke(main, ['compile', str(jug_file), '-o', str(out_file)])
    assert result.exit_code == 0
    assert out_file.exists()
    assert "print('namaste')" in out_file.read_text(encoding="utf-8")

def test_cli_compile_stdout(runner, tmp_path):
    jug_file = tmp_path / "hello.jug"
    jug_file.write_text("bolo('namaste')", encoding="utf-8")
    result = runner.invoke(main, ['compile', str(jug_file)])
    assert result.exit_code == 0
    assert "print('namaste')" in result.output

def test_cli_check(runner, tmp_path):
    jug_file = tmp_path / "hello.jug"
    jug_file.write_text("bolo('namaste')", encoding="utf-8")
    result = runner.invoke(main, ['check', str(jug_file)])
    assert result.exit_code == 0
    assert "sahi hai" in result.output

def test_cli_check_invalid(runner, tmp_path):
    jug_file = tmp_path / "hello.jug"
    jug_file.write_text("bolo('namaste'", encoding="utf-8")  # missing paren
    result = runner.invoke(main, ['check', str(jug_file)])
    assert result.exit_code != 0
    assert "Syntax check failed" in result.output
def test_cli_new(runner, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(main, ['new', 'myproject'])
    assert result.exit_code == 0
    assert os.path.exists("myproject")
    assert os.path.exists(os.path.join("myproject", "main.jug"))
    assert os.path.exists(os.path.join("myproject", "README.md"))

def test_cli_new_existing_dir(runner, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.mkdir("myproject")
    result = runner.invoke(main, ['new', 'myproject'])
    assert result.exit_code != 0
    assert "pehle se hi hai" in result.output

# Mock PackageManager for install, remove, update, search
@patch("jugaadlang.package_manager.manager.JugaadPackageManager.search")
@patch("jugaadlang.package_manager.manager.JugaadPackageManager.update")
@patch("jugaadlang.package_manager.manager.JugaadPackageManager.remove")
@patch("jugaadlang.package_manager.manager.JugaadPackageManager.install")
def test_cli_package_commands(mock_install, mock_remove, mock_update, mock_search, runner):

    r1 = runner.invoke(main, ['install', 'web'])
    assert r1.exit_code == 0
    mock_install.assert_called_once_with('web')

    r2 = runner.invoke(main, ['remove', 'web'])
    assert r2.exit_code == 0
    mock_remove.assert_called_once_with('web')

    r3 = runner.invoke(main, ['update', 'web'])
    assert r3.exit_code == 0
    mock_update.assert_called_once_with('web')

    r4 = runner.invoke(main, ['search', 'web'])
    assert r4.exit_code == 0
    mock_search.assert_called_once_with('web')

def test_cli_doctor(runner):
    # Just run doctor, it doesn't do harmful side effects
    result = runner.invoke(main, ['doctor'])
    # Might exit 0 or 1 depending on whether all deps are found
    assert result.exit_code in [0, 1]
    assert "JugaadLang Doctor" in result.output

@patch("jugaadlang.repl.repl.JugaadREPL.start")
def test_cli_repl(mock_repl, runner):
    result = runner.invoke(main, ['repl'])
    assert result.exit_code == 0
    mock_repl.assert_called_once()


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert "JugaadLang v" in result.output
