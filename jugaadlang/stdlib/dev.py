import random
import sys
import time


def fake_commit() -> str:
    """Returns a generic, believable commit message."""
    commits = [
        "Minor fixes",
        "Update config",
        "Fix typo",
        "Refactoring stuff",
        "WIP: Do not merge",
        "Fixed the thing that was broken",
        "It compiles now",
    ]
    commit = random.choice(commits)
    print(f"📝 Suggested Commit Message: '{commit}'")
    return commit


def coffee_break(minutes: int = 5) -> None:
    """
    Renders a fake 'Compiling...' progress bar in the terminal
    that takes exactly 'minutes' to complete.
    """
    seconds = minutes * 60
    print(f"☕ Initiating {minutes} minute Coffee Break sequence...")
    print("💻 Terminal will now look busy. Go grab a coffee!")

    total_steps = 50
    sleep_per_step = seconds / total_steps

    sys.stdout.write("Compiling C++ Dependencies: [")
    sys.stdout.flush()

    try:
        for i in range(total_steps):
            time.sleep(sleep_per_step)
            sys.stdout.write("#")
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n❌ Boss caught you? Coffee break aborted!")
        return

    print("] 100% DONE")
    print("✅ Build Successful! Welcome back.")


def blame_someone_else() -> str:
    """Returns a random excuse for why the code is broken."""
    excuses = [
        "It works on my machine.",
        "Must be a caching issue.",
        "The API response changed without any warning.",
        "It's a known bug in the third-party library.",
        "Somebody merged into main without testing.",
    ]
    excuse = random.choice(excuses)
    print(f"🤷‍♂️ Developer Excuse: {excuse}")
    return excuse
