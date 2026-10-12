import random
from typing import Any


# ☕ Daily Life
def chai() -> None:
    print("☕ Chai ready hai bhai!\nCoding shuru karo.")


def pani_pilo() -> None:
    print("💧 Hydration reminder!\nPaani pi lo warna bug aur badhenge.")


def soja() -> None:
    print("😴 3 AM ho gaya bhai.\nAb laptop band karo.")


def ghaas_chhoo() -> None:
    print("🌱 Bahar jao.\nReal graphics bhi achhe hote hain.")


# ❤️ Love & Couple
def crush() -> None:
    print("😍 Crush online hai...\nMessage bhejna hai? (Y/N)")


def proposal(name: str) -> None:
    print(f"💌 {name} ko proposal bheja gaya.\n\nResult:")
    if random.random() < 0.2:
        print("💖 Accepted")
    else:
        print("❌ Friendzone")


def couple_days() -> None:
    days = random.randint(1, 1000)
    print(f"❤️ Relationship survival streak:\n{days} days")


def breakup() -> None:
    print("💔 Error 404:\nRelationship not found.")


def love_percentage(name1: str, name2: str) -> None:
    percent = random.randint(0, 100)
    print(f"💕 Love Match for {name1} & {name2}:\n{percent}%")


# 📚 Student
def attendance() -> None:
    print("📋 Attendance:\n73%\n\nWarning:\nExam mein baithne layak ho.")


def assignment() -> None:
    print("📝 Submission:\nTomorrow\n\nStress Level:\n999+")


def exam_mode() -> None:
    print("📚 Exam mode activated.\n\nSocial life disabled.")


def cgpa() -> None:
    print("🎓 Current CGPA:\n8.2")


def bunk() -> None:
    print("🏃 Attendance skipped successfully.")


# 👨‍💻 Programmer
def debug_fun() -> None:
    print("🐛 Bug found.\n\nCongratulations.\nNow find the remaining 47 bugs.")


def motivation() -> None:
    print("🔥 Keep coding.\n\nGoogle bhi garage se shuru hua tha.")


def stackoverflow() -> None:
    print("🔍 Searching...\n\nAnswer copied successfully.")


def deploy() -> None:
    print("🚀 Deployment successful.\n\nProduction broken.")


def git_push() -> None:
    print("📤 Pushing code...\n\nPraying...")


# 🎮 Gaming
def ludo() -> None:
    print("🎲 Ludo game started... (Waiting for 3 other players to drop out)")


def snake_game() -> None:
    print("🐍 Snake game launched... Don't bite yourself!")


def tic_tac_toe() -> None:
    print("❌⭕ Tic Tac Toe started... It's a draw anyway.")


def rock_paper_scissors() -> None:
    print("✊✋✌️ Rock Paper Scissors... Computer chose Gun. You lose.")


def guess_number() -> None:
    print("🔢 Guess the number between 1 and 100... Too bad, you guessed wrong!")


def hangman() -> None:
    print("🪢 Hangman game started... Don't leave him hanging!")


# 😂 Entertainment
def meme() -> None:
    print("😂 Meme Loaded:\n\nTeacher:\nProject kab submit karoge?\n\nStudent:\nNext version mein.")


def joke() -> None:
    print("🤣 Why do programmers prefer dark mode?\n\nBecause light attracts bugs.")


def roast() -> None:
    print("🔥 Tumhara code itna slow hai,\nki Internet Explorer bhi has raha hai.")


# 🔮 Fortune
def fortune_fun() -> None:
    print("🔮 Future Prediction:\n\nKal bug milega.\nPar fix bhi tum hi karoge.")


def kundli_fun() -> None:
    print("🪐 Saturn detected in loop.\n\nInfinite loop chances: 83%")


# 🏆 Productivity
def pomodoro(minutes: int = 25) -> None:
    print(f"🍅 Starting {minutes}-minute focus timer...")
    # non-blocking dummy for REPL / exec environment
    print("🍅 Time's up! Take a break.")


def todo() -> None:
    print("📝 Todo list created:\n1. Fix bugs\n2. Add more bugs\n3. Sleep")


def habit_tracker() -> None:
    print("📈 Habit tracking:\nCoding: 10 hrs\nSleeping: 2 hrs")


def focus_mode() -> None:
    print("🧘 Focus mode enabled.\nAll distractions blocked.")


def study_with_me() -> None:
    print("📖 Study session started... Lofi beats playing in the background 🎧")


# 🏅 Legendary
def nazar() -> None:
    print("🧿 Nazar Protection Enabled.\nBugs blocked.")


def ashirwad() -> None:
    print("👵 Dadi Blessing Activated.\n\nSuccess Rate +100%")


def paisa_wasool() -> None:
    print("💸 JugaadLang is free.\n\nMoney saved successfully.")


def bhagwan_bhala_kare() -> None:
    print("📿 Error recovery prayer sent.")


def bas_kar_bhai() -> None:
    print("🛑 Coding time exceeded.\n\nGo sleep.")


# 🤖 AI
def ai_bhai(prompt: str) -> None:
    print(
        f"🤖 AI Bhai is thinking about: '{prompt}'...\nWait karo, response generate ho raha hai... done!"
    )


def resume_banao() -> None:
    print("📄 Resume Generated:\nSkills: JugaadLang, Googling\nExperience: 10 years of debugging")


def interview_prep() -> None:
    print(
        "👔 Interview Prep:\nQuestion: What is polymorphism?\nAnswer: Jo bhi ho, apne ko package se matlab hai."
    )


def roadmap(topic: str) -> None:
    print(
        f"🗺️ Roadmap for '{topic}':\n1. Watch 10 hour tutorial\n2. Do nothing\n3. Forget everything"
    )


def leetcode_bachao() -> None:
    print("🆘 LeetCode Rescue:\nHere is the O(1) solution: Just skip the question.")


# 🧩 Python 3.14 t-strings (PEP 750)
def roop(maal: Any) -> str:
    """Template (t-string) ko render karke text (str) banao — f-string jaisa."""
    if isinstance(maal, str):
        return maal  # Python < 3.14: t-strings already degrade to plain strings
    try:
        from string.templatelib import Interpolation
    except ImportError:  # pragma: no cover - guarded by the check above
        return str(maal)

    parts = []
    for item in maal:  # iterating a Template yields str + Interpolation chunks
        if isinstance(item, Interpolation):
            value = item.value
            # Runtime conversions are 'r'/'s'/'a' (or None); the AST uses 114/115/97
            conv = item.conversion
            if conv in (114, "r"):
                value = repr(value)
            elif conv in (97, "a"):
                value = ascii(value)
            elif conv in (115, "s"):
                value = str(value)
            value = format(value, item.format_spec) if item.format_spec else str(value)
            parts.append(value)
        else:
            parts.append(item)
    return "".join(parts)


FUN_BUILTINS = {
    "chai": chai,
    "pani_pilo": pani_pilo,
    "soja": soja,
    "ghaas_chhoo": ghaas_chhoo,
    "crush": crush,
    "proposal": proposal,
    "couple_days": couple_days,
    "breakup": breakup,
    "love_percentage": love_percentage,
    "attendance": attendance,
    "assignment": assignment,
    "exam_mode": exam_mode,
    "cgpa": cgpa,
    "bunk": bunk,
    "debug": debug_fun,
    "motivation": motivation,
    "stackoverflow": stackoverflow,
    "deploy": deploy,
    "git_push": git_push,
    "ludo": ludo,
    "snake_game": snake_game,
    "tic_tac_toe": tic_tac_toe,
    "rock_paper_scissors": rock_paper_scissors,
    "guess_number": guess_number,
    "hangman": hangman,
    "meme": meme,
    "joke": joke,
    "roast": roast,
    "fortune": fortune_fun,
    "kundli": kundli_fun,
    "pomodoro": pomodoro,
    "todo": todo,
    "habit_tracker": habit_tracker,
    "focus_mode": focus_mode,
    "study_with_me": study_with_me,
    "nazar": nazar,
    "ashirwad": ashirwad,
    "paisa_wasool": paisa_wasool,
    "bhagwan_bhala_kare": bhagwan_bhala_kare,
    "bas_kar_bhai": bas_kar_bhai,
    "ai_bhai": ai_bhai,
    "resume_banao": resume_banao,
    "interview_prep": interview_prep,
    "roadmap": roadmap,
    "leetcode_bachao": leetcode_bachao,
    "roop": roop,
}
