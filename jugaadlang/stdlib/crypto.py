"""
crypto — JugaadLang Cryptography Module.
"""

import base64
import hashlib


def sha256(text: str) -> str:
    """Generate SHA-256 hash of a string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def md5(text: str) -> str:
    """Generate MD5 hash of a string."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def base64_encode(text: str) -> str:
    """Base64 encode a string."""
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def base64_decode(encoded_text: str) -> str:
    """Base64 decode a string."""
    return base64.b64decode(encoded_text.encode("utf-8")).decode("utf-8")
