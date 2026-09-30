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
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        if not os.path.exists(self.cache_dir):
            try:
                os.makedirs(self.cache_dir)
            except OSError:
                pass  # Ignore if we can't create it

    def _get_key(self, source: str) -> str:
        return hashlib.sha256(source.encode("utf-8")).hexdigest()

    def _get_l2_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.jugc")

    def get(self, source: str) -> Optional[CodeType]:
        """Get compiled Python bytecode from cache."""
        key = self._get_key(source)
        
        # Check L1 cache
        if key in self._l1_cache:
            return self._l1_cache[key]
            
        # Check L2 cache
        l2_path = self._get_l2_path(key)
        if os.path.exists(l2_path):
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
        self._ensure_cache_dir()
        l2_path = self._get_l2_path(key)
        try:
            with open(l2_path, "wb") as f:
                marshal.dump(code_obj, f)
        except OSError:
            pass

    def clear(self) -> None:
        """Clear all caches."""
        self._l1_cache.clear()
        if os.path.exists(self.cache_dir):
            try:
                for filename in os.listdir(self.cache_dir):
                    if filename.endswith(".jugc"):
                        os.remove(os.path.join(self.cache_dir, filename))
            except OSError:
                pass

cache_manager = CacheManager()
