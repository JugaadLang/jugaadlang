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


def run_repl_inputs(inputs):
    """Run a REPL session over scripted prompts and return captured stdout."""
    repl = JugaadREPL()
    with patch("jugaadlang.repl.repl.PromptSession") as mock_session_cls:
        mock_session = MagicMock()
        mock_session.prompt.side_effect = list(inputs) + [EOFError]
        mock_session_cls.return_value = mock_session
        with patch("jugaadlang.repl.repl.console.print"):
            captured = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured
            try:
                repl.start()
            finally:
                sys.stdout = old_stdout
        return captured.getvalue(), mock_session


def test_repl_nested_block_in_function():
    # "agar sahi:" is indented one level deeper than the function body
    output, _ = run_repl_inputs(
        [
            "banao greet():",
            "agar sahi:",
            "bolo('andar')",
            "",
            "greet()",
        ]
    )
    assert "andar" in output


def test_repl_nested_block_false_condition_runs_nothing():
    output, _ = run_repl_inputs(
        [
            "banao greet():",
            "agar galat:",
            "bolo('andar')",
            "",
            "greet()",
        ]
    )
    assert "andar" not in output


def test_repl_loop_inside_function():
    output, _ = run_repl_inputs(
        [
            "banao count():",
            "ghumo i mein range(3):",
            "bolo(i)",
            "",
            "count()",
        ]
    )
    assert output.split() == ["0", "1", "2"]


def test_repl_typed_indent_returns_to_outer_level():
    # The fourth line is typed with four spaces, which closes the inner
    # 'agar' block and puts 'wapas 5' back in the function body.
    output, _ = run_repl_inputs(
        [
            "banao f():",
            "agar sahi:",
            "bolo('inner')",
            "    wapas 5",
            "",
            "result = f()",
            "bolo(result)",
        ]
    )
    assert output.split() == ["inner", "5"]


def test_repl_prompt_shows_nesting_depth():
    _, mock_session = run_repl_inputs(
        [
            "banao f():",
            "agar sahi:",
            "bolo('x')",
            "",
        ]
    )
    prompts = [call.args[0] for call in mock_session.prompt.call_args_list]
    # First continuation line at depth 1, the body of 'agar' at depth 2.
    assert ".. " + ("    " * 1) in prompts
    assert ".. " + ("    " * 2) in prompts


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
