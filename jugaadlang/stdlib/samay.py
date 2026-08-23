"""
samay — JugaadLang Date and Time Module.
"""

import datetime
import time

# Standard time helpers
samay = time.time
soja = time.sleep


def ek_second_rukja() -> None:
    """Sleep for exactly one second."""
    time.sleep(1)


def abhibhi() -> datetime.datetime:
    """Get current timestamp (datetime.now)."""
    return datetime.datetime.now()


def aaj() -> datetime.date:
    """Get current date (date.today)."""
    return datetime.date.today()


def format_karo(dt: datetime.datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string."""
    return dt.strftime(fmt)
