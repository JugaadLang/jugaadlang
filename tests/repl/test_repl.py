import io
import os
import sys
from unittest.mock import MagicMock, call, patch

from jugaadlang.repl.repl import JugaadREPL, _open_bracket_depth


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
        with patch("jugaadlang.repl.repl.console.print") :
            captured = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured
            try:
                repl.start()
            finally:
                sys.stdout = old_stdout
            assert "hello" in captured.getvalue()

def test_repl_syntax_error():
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = ["bolo('missing_paren", EOFError]
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print") :
            repl.start()

def test_repl_runtime_error():
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = ["1 / 0", EOFError]
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print") :
            repl.start()

def test_repl_history_file_creation(tmp_path):
    with patch("os.path.expanduser", return_value=str(tmp_path)):
        repl = JugaadREPL()
        assert os.path.exists(tmp_path)
        assert repl.history_file == str(tmp_path / "repl_history.txt")

def test_open_bracket_depth_counts_unclosed_brackets():
    assert _open_bracket_depth("") == 0
    assert _open_bracket_depth("bolo(1, 2)") == 0
    assert _open_bracket_depth("bolo(") == 1
    assert _open_bracket_depth("d = {") == 1
    assert _open_bracket_depth("x = [1, (2,") == 2
    assert _open_bracket_depth("]") == 0

def test_open_bracket_depth_ignores_strings_and_comments():
    assert _open_bracket_depth('bolo("(")') == 0
    assert _open_bracket_depth("s = ')'") == 0
    assert _open_bracket_depth('s = "[" # ( comment') == 0
    assert _open_bracket_depth("x = 1 // [ comment") == 0

def test_repl_multiline_call():
    repl = JugaadREPL()
    inputs = [
        "bolo(",
        "  1,",
        "  2,",
        ")",
        EOFError
    ]
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = inputs
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print"):
            captured = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured
            try:
                repl.start()
            finally:
                sys.stdout = old_stdout
            assert "1 2" in captured.getvalue()
        prompts = [entry.args[0] for entry in mock_session.prompt.call_args_list if entry.args]
        assert prompts[1:4] == [".. ", ".. ", ".. "]

def test_repl_multiline_list_literal():
    repl = JugaadREPL()
    inputs = [
        "[1,",
        " 2,",
        " 3]",
        EOFError
    ]
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = inputs
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print") as mock_print:
            repl.start()
            mock_print.assert_any_call([1, 2, 3])

def test_repl_balanced_brackets_do_not_continue():
    repl = JugaadREPL()
    inputs = ['bolo("(")', EOFError]
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = inputs
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print"):
            repl.start()
        assert mock_session.prompt.call_args_list == [call(">> "), call(">> ")]
