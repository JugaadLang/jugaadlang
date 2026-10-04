"""
JugaadLang AST and Precompiled Representation Cache Manager.
"""

from .cache.manager import (
    CACHE_VERSION,
    CacheManager,
    cache_manager,
    deserialize_ast,
    serialize_ast,
)

__all__ = [
    "CACHE_VERSION",
    "CacheManager",
    "cache_manager",
    "serialize_ast",
    "deserialize_ast",
]
