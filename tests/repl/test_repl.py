import os
import pytest
from unittest.mock import patch, MagicMock
from jugaadlang.repl.repl import JugaadREPL

def test_repl_eof():
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = EOFError
        mock_session_cls.return_value = mock_session
        repl.start()

def test_repl_keyboard_interrupt():
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = [KeyboardInterrupt, EOFError]
        mock_session_cls.return_value = mock_session
        repl.start()

def test_repl_empty_line():
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = ["   ", EOFError]
        mock_session_cls.return_value = mock_session
        repl.start()

def test_repl_single_line_execution():
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = ["1 + 2", EOFError]
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print") as mock_print:
            repl.start()
            mock_print.assert_any_call(3)

def test_repl_multiline_block():
    repl = JugaadREPL()
    inputs = [
        "agar 1 == 1:",
        "bolo('hello')",
        "", # End of block
        EOFError
    ]
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = inputs
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print") as mock_print:
            with patch("builtins.print") as mock_builtin_print:
                repl.start()
                mock_builtin_print.assert_called_with("hello")

def test_repl_syntax_error():
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = ["bolo('missing_paren", EOFError]
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print") as mock_print:
            repl.start()

def test_repl_runtime_error():
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = ["1 / 0", EOFError]
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print") as mock_print:
            repl.start()

def test_repl_history_file_creation(tmp_path):
    with patch("os.path.expanduser", return_value=str(tmp_path)):
        repl = JugaadREPL()
        assert os.path.exists(tmp_path)
        assert repl.history_file == str(tmp_path / "repl_history.txt")
