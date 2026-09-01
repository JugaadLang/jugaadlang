"""
paath — JugaadLang Text/String Module.
"""


def ulta(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


def palindrome_hai(text: str) -> bool:
    """Check whether a string is a palindrome (case- and space-insensitive)."""
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def shabd_gino(text: str) -> int:
    """Count the words in a string."""
    return len(text.split())


def akshar_gino(text: str) -> int:
    """Count the characters in a string."""
    return len(text)


def bada(text: str) -> str:
    """Convert a string to uppercase."""
    return text.upper()


def chota(text: str) -> str:
    """Convert a string to lowercase."""
    return text.lower()


def title_banao(text: str) -> str:
    """Convert a string to title case."""
    return text.title()


def saaf(text: str) -> str:
    """Trim leading and trailing whitespace from a string."""
    return text.strip()


def badlo(text: str, purana: str, naya: str) -> str:
    """Replace all occurrences of a substring with another."""
    return text.replace(purana, naya)


def shamil_hai(text: str, khoj: str) -> bool:
    """Check whether a string contains a substring."""
    return khoj in text


def dohrao(text: str, n: int) -> str:
    """Repeat a string n times."""
    return text * n
