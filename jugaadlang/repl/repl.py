"""
JugaadLang REPL — Interactive Read-Eval-Print Loop.
Uses prompt_toolkit and pygments for premium terminal capabilities.
"""

from __future__ import annotations

import os

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexer import RegexLexer, words
from pygments.token import Comment, Keyword, Name, Number, Operator, String, Text
from rich.console import Console

from ..runtime.interpreter import JugaadInterpreter

console = Console(color_system="truecolor", force_terminal=True)

# ── Pygments Lexer for JugaadLang ─────────────────────────────────────────────


class JugaadPygmentsLexer(RegexLexer):
    """Custom Pygments Lexer for live REPL syntax highlighting."""

    name = "JugaadLang"
    aliases = ["jugaadlang", "jug"]
    filenames = ["*.jug"]

    tokens = {
        "root": [
            (r"#.*$", Comment.Single),
            (r"//.*$", Comment.Single),
            (r"/\*.*?\*/", Comment.Multiline),
            (
                words(
                    (
                        "agar",
                        "shayad",
                        "warna",
                        "ghumo",
                        "jabtak",
                        "koshish",
                        "gadbad",
                        "aakhir_me",
                        "rukja",
                        "chalte_raho",
                        "wapas",
                        "tez",
                        "intezaar",
                        "baanto",
                        "theek_hai",
                        "sabka",
                        "chota_funkshan",
                        "mein",
                        "mein_nahi",
                        "hai",
                        "nahi_hai",
                        "bulawo",
                        "lao",
                        "se",
                        "khud",
                        "udao",
                        "banao",
                        "ustad",
                        "jaise",
                        "as",
                        "pakka",
                        "hatao",
                        "gair_local",
                        "ke_saath",
                    ),
                    suffix=r"\b",
                ),
                Keyword,
            ),
            (words(("sahi", "galat", "kuch_nahi"), suffix=r"\b"), Keyword.Constant),
            (
                words(
                    (
                        "bolo",
                        "poochho",
                        "kismat",
                        "sikka",
                        "saaf",
                        "ruk",
                        "bahar",
                        "namaste",
                        "version",
                        "chai",
                        "himmat",
                        "ghaas_chhoo",
                        "bachao",
                        "fortune",
                        "jugaad",
                        "maan",
                        "sab",
                        "koi_bhi",
                        "binary",
                        "satyata",
                        "bulaane_yogya",
                        "akshar",
                        "gun_hatao",
                        "kosh",
                        "bhag_shesh",
                        "ginti",
                        "chalao",
                        "chhano",
                        "gun_lao",
                        "gun_hai",
                        "madad",
                        "pehchan",
                        "purnank",
                        "prakar_hai",
                        "subclass_hai",
                        "lambaee",
                        "suchi",
                        "adhiktam",
                        "nyuntam",
                        "agla",
                        "vastu",
                        "kholo",
                        "ghat",
                        "ulta",
                        "gun_badlo",
                        "tukda",
                        "kramwar",
                        "shabd",
                        "yog",
                        "prakar",
                        "nazar",
                        "ashirwad",
                        "dhanya_waad",
                        "bhagwan_bhala_kare",
                        "paisa_wasool",
                        "bas_kar_bhai",
                        "chilla_mat",
                        "kundli",
                        "pani_pilo",
                        "soja",
                        "crush",
                        "proposal",
                        "couple_days",
                        "breakup",
                        "love_percentage",
                        "attendance",
                        "assignment",
                        "exam_mode",
                        "cgpa",
                        "bunk",
                        "debug",
                        "motivation",
                        "stackoverflow",
                        "deploy",
                        "git_push",
                        "ludo",
                        "snake_game",
                        "tic_tac_toe",
                        "rock_paper_scissors",
                        "guess_number",
                        "hangman",
                        "meme",
                        "joke",
                        "roast",
                        "pomodoro",
                        "todo",
                        "habit_tracker",
                        "focus_mode",
                        "study_with_me",
                        "ai_bhai",
                        "resume_banao",
                        "interview_prep",
                        "roadmap",
                        "leetcode_bachao",
                    ),
                    suffix=r"\b",
                ),
                Name.Builtin,
            ),
            (r"[a-zA-Z_][a-zA-Z0-9_]*", Name),
            (r"==|!=|<=|>=|->|:=|\+=|-=|\*=|=/|%=|\*\*=|//=|\*\*|//|\+|-|\*|/|%|=|<|>", Operator),
            (r"\d+\.\d+", Number.Float),
            (r"\d+", Number.Integer),
            (r'"([^"\\]|\\.)*"', String.Double),
            (r"'([^'\\]|\\.)*'", String.Single),
            (r"[{}()\[\],.:;]", Operator),
            (r"\s+", Text),
        ]
    }


# ── Word Completer ────────────────────────────────────────────────────────────

KEYWORDS_LIST = [
    "bolo",
    "poochho",
    "agar",
    "shayad",
    "warna",
    "ghumo",
    "jabtak",
    "banao",
    "wapas",
    "ustad",
    "khud",
    "lao",
    "se",
    "sust",
    "rukja",
    "chalte_raho",
    "koshish",
    "gadbad",
    "aakhir_me",
    "udao",
    "sahi",
    "galat",
    "kuch_nahi",
    "aur",
    "ya",
    "nahi",
    "tez",
    "intezaar",
    "baanto",
    "theek_hai",
    "sabka",
    "chota_funkshan",
    "mein",
    "mein_nahi",
    "hai",
    "nahi_hai",
    "bulawo",
    "chai",
    "kismat",
    "sikka",
    "saaf",
    "ruk",
    "bahar",
    "namaste",
    "version",
    "roop",
    "himmat",
    "ghaas_chhoo",
    "bachao",
    "fortune",
    "jugaad",
    "maan",
    "sab",
    "koi_bhi",
    "binary",
    "satyata",
    "bulaane_yogya",
    "akshar",
    "gun_hatao",
    "kosh",
    "bhag_shesh",
    "ginti",
    "chalao",
    "chhano",
    "gun_lao",
    "gun_hai",
    "madad",
    "pehchan",
    "purnank",
    "prakar_hai",
    "subclass_hai",
    "lambaee",
    "suchi",
    "adhiktam",
    "nyuntam",
    "agla",
    "vastu",
    "kholo",
    "ghat",
    "ulta",
    "gun_badlo",
    "tukda",
    "kramwar",
    "shabd",
    "yog",
    "prakar",
    "nazar",
    "ashirwad",
    "dhanya_waad",
    "bhagwan_bhala_kare",
    "paisa_wasool",
    "bas_kar_bhai",
    "chilla_mat",
    "kundli",
    "pani_pilo",
    "soja",
    "crush",
    "proposal",
    "couple_days",
    "breakup",
    "love_percentage",
    "attendance",
    "assignment",
    "exam_mode",
    "cgpa",
    "bunk",
    "debug",
    "motivation",
    "stackoverflow",
    "deploy",
    "git_push",
    "ludo",
    "snake_game",
    "tic_tac_toe",
    "rock_paper_scissors",
    "guess_number",
    "hangman",
    "meme",
    "joke",
    "roast",
    "pomodoro",
    "todo",
    "habit_tracker",
    "focus_mode",
    "study_with_me",
    "ai_bhai",
    "resume_banao",
    "interview_prep",
    "roadmap",
    "leetcode_bachao",
    "jaise",
    "as",
    "pakka",
    "hatao",
    "gair_local",
    "ke_saath",
    "whatsapp",
    "whatsapp.bhejo",
    "whatsapp.spam",
    "student",
    "student.bahana",
    "student.cgpa_calc",
    "student.proxy_attendance",
    "love",
    "love.flirt",
    "love.date_idea",
    "love.sorry_message",
    "dev",
    "dev.fake_commit",
    "dev.coffee_break",
    "dev.blame_someone_else",
]
completer = WordCompleter(KEYWORDS_LIST, ignore_case=True)


# ── REPL ──────────────────────────────────────────────────────────────────────


class JugaadREPL:
    """
    JugaadLang Interactive REPL session.
    """

    def __init__(self) -> None:
        self.interpreter = JugaadInterpreter(filename="<repl>")
        # Persist history in app data dir
        history_dir = os.path.expanduser("~/.jugaadlang")
        os.makedirs(history_dir, exist_ok=True)
        self.history_file = os.path.join(history_dir, "repl_history.txt")

    def start(self) -> None:
        """Launch the REPL loop."""
        # Print welcome banner
        console.print(
            "[bold orange1]JugaadLang v1.2.8 — Modern Programming Language in Hindi 🇮🇳[/bold orange1]"
        )
        console.print(
            "[dim]Type code and press Enter. Enter blank line to execute block. Ctrl+D to exit.[/dim]\n"
        )
        console.print(
            "[dim]A line ending with ':' opens a block and the next line is indented automatically. "
            "Start a line with your own spaces to return to an outer level.[/dim]\n"
        )

        session: PromptSession = PromptSession(
            history=FileHistory(self.history_file),
            lexer=PygmentsLexer(JugaadPygmentsLexer),
            completer=completer,
            auto_suggest=AutoSuggestFromHistory(),
        )

        while True:
            try:
                # Retrieve first line
                line = session.prompt(">> ")
                if not line.strip():
                    continue

                # Check for block entry
                if line.rstrip().endswith(":"):
                    # Lines are indented automatically. Every line ending with
                    # ':' opens one more level, so nested blocks can be built
                    # one line at a time and the prompt shows the current
                    # depth. A line that starts with whitespace is kept exactly
                    # as typed, which is how an outer level is reached again.
                    lines = [line]
                    level = 1
                    while True:
                        indent = "    " * level
                        sub_line = session.prompt(".. " + indent)
                        if not sub_line.strip():
                            # Double enter / empty line executes
                            break
                        if sub_line[:1] in (" ", "\t"):
                            source_line = sub_line
                            typed_indent = len(sub_line) - len(sub_line.lstrip())
                            level = typed_indent // 4
                        else:
                            source_line = indent + sub_line
                        lines.append(source_line)
                        if source_line.rstrip().endswith(":"):
                            level += 1
                    source = "\n".join(lines)
                else:
                    source = line

                # Execute
                result = self.interpreter.run_expression(source)
                if result is not None:
                    # Print expression result
                    console.print(result)

            except KeyboardInterrupt:
                # Ctrl+C clears line
                console.print("\n[yellow]KeyboardInterrupt (Ctrl+C). Clear line.[/yellow]")
                continue
            except EOFError:
                # Ctrl+D exits
                console.print("\n[bold orange1]Namaste! Chalte hain! 🙏[/bold orange1]")
                break
            except Exception:
                # Catch block errors, stack trace is already printed by run_expression
                pass
