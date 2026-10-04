"""
Two-tier AST and precompiled representation caching system for JugaadLang.
L1: In-Memory cache (fast lookups within same process/session).
L2: Disk-based caching in deterministic `__jugcache__/` directory.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import marshal
import os
from types import CodeType
from typing import Optional


class CacheManager:
    """
    Two-tier caching system for JugaadLang.
    L1: In-Memory dictionary.
    L2: Disk-based bytecode caching in __jugcache__/ directory.
    """

    def __init__(self, cache_dir: str = "__jugcache__"):
        self._l1_cache: dict[str, CodeType] = {}
        self.cache_dir = cache_dir
        if os.environ.get("JUG_NO_CACHE", "").lower() in ("1", "true", "yes"):
            self.enabled = False
        else:
            self.enabled = enabled

        self._l1_ast_cache: dict[str, Module] = {}
        self._l1_py_cache: dict[str, str] = {}
        self.hits: int = 0
        self.misses: int = 0
        self._ensure_cache_dir()

    def _ensure_cache_dir(self, directory: Optional[str] = None) -> None:
        target = directory or self.cache_dir
        if not os.path.exists(target):
            try:
                os.makedirs(target, exist_ok=True)
            except OSError:
                pass

    def _get_key(self, source: str) -> str:
        return hashlib.sha256(source.encode("utf-8")).hexdigest()

    def _get_l2_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.jugc")

    def get(self, source: str) -> Optional[CodeType]:
        """Get compiled Python bytecode from cache."""
        key = self._get_key(source)

        # 1. Set L1 cache
        self._l1_ast_cache[key] = copy.deepcopy(ast_mod)
        if py_source:
            self._l1_py_cache[key] = py_source

        # 2. Set L2 cache
        tmp_path: Optional[str] = None
        try:
            cache_dir = self._resolve_cache_dir(filename)
            self._ensure_cache_dir(cache_dir)

            target_path = os.path.join(cache_dir, f"{key}.jugc")
            tmp_path = os.path.join(cache_dir, f"{key}.tmp.{os.getpid()}.jugc")

            payload = {
                "cache_version": CACHE_VERSION,
                "jugaadlang_version": __version__,
                "source_hash": key,
                "filename": os.path.basename(filename) if filename else None,
                "ast": serialize_ast(ast_mod),
                "py_source": py_source,
            }

            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False)

            os.replace(tmp_path, target_path)

        except Exception:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

    def get(self, source: str, filename: Optional[str] = None) -> Optional[str]:
        """
        Get compiled Python source from cache (for backward compatibility).
        Checks L1, then .jugc payload, then legacy .py file.
        """
        if not self.enabled:
            return None

        key = self._get_key(source)

        # Check L1 cache
        if key in self._l1_py_cache:
            return self._l1_py_cache[key]

        # Check L2 .jugc cache
        jugc_path = self._get_l2_path(key, filename=filename, ext=".jugc")
        if os.path.exists(jugc_path):
            try:
                with open(jugc_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                if (
                    isinstance(payload, dict)
                    and payload.get("cache_version") == CACHE_VERSION
                    and payload.get("source_hash") == key
                    and payload.get("py_source") is not None
                ):
                    py_src = payload["py_source"]
                    self._l1_py_cache[key] = py_src
                    return py_src
            except Exception:
                pass

        # Check legacy .py cache
        legacy_path = self._get_l2_path(key, filename=filename, ext=".py")
        if os.path.exists(legacy_path):
            try:
                with open(l2_path, "rb") as f:
                    code_obj = marshal.load(f)
                if isinstance(code_obj, CodeType):
                    self._l1_cache[key] = code_obj
                    return code_obj
            except (OSError, ValueError, EOFError):
                pass

        return None

    def set(self, source: str, code_obj: CodeType) -> None:
        """Store compiled Python bytecode in cache."""
        key = self._get_key(source)

        # Set L1 cache
        self._l1_cache[key] = code_obj
        
        # Set L2 cache
        tmp_path: Optional[str] = None
        try:
            with open(l2_path, "wb") as f:
                marshal.dump(code_obj, f)
        except OSError:
            pass

    def clear(self) -> None:
        """Clear all caches (both memory and disk)."""
        self._l1_ast_cache.clear()
        self._l1_py_cache.clear()
        self.hits = 0
        self.misses = 0

        self._clean_dir(self.cache_dir)
        cwd_cache = os.path.join(os.getcwd(), "__jugcache__")
        if os.path.exists(cwd_cache) and os.path.abspath(cwd_cache) != os.path.abspath(
            self.cache_dir
        ):
            self._clean_dir(cwd_cache)

    def _clean_dir(self, directory: str) -> None:
        if os.path.exists(directory):
            try:
                for filename in os.listdir(self.cache_dir):
                    if filename.endswith(".jugc"):
                        os.remove(os.path.join(self.cache_dir, filename))
            except OSError:
                pass

    def invalidate(self, source: str, filename: Optional[str] = None) -> None:
        """Explicitly invalidate cache for the given source."""
        key = self._get_key(source)
        self._l1_ast_cache.pop(key, None)
        self._l1_py_cache.pop(key, None)

        for ext in (".jugc", ".py"):
            path = self._get_l2_path(key, filename=filename, ext=ext)
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


cache_manager = CacheManager()
