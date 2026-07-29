import os
import hashlib
from typing import Optional

class CacheManager:
    """
    Two-tier caching system for JugaadLang.
    L1: In-Memory dictionary.
    L2: Disk-based caching in .jug_cache/ directory.
    """

    def __init__(self, cache_dir: str = ".jug_cache"):
        self._l1_cache: dict[str, str] = {}
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
        return os.path.join(self.cache_dir, f"{key}.py")

    def get(self, source: str) -> Optional[str]:
        """Get compiled Python source from cache."""
        key = self._get_key(source)
        
        # Check L1 cache
        if key in self._l1_cache:
            return self._l1_cache[key]
            
        # Check L2 cache
        l2_path = self._get_l2_path(key)
        if os.path.exists(l2_path):
            try:
                with open(l2_path, "r", encoding="utf-8") as f:
                    py_source = f.read()
                self._l1_cache[key] = py_source
                return py_source
            except OSError:
                pass
                
        return None

    def set(self, source: str, py_source: str) -> None:
        """Store compiled Python source in cache."""
        key = self._get_key(source)
        
        # Set L1 cache
        self._l1_cache[key] = py_source
        
        # Set L2 cache
        self._ensure_cache_dir()
        l2_path = self._get_l2_path(key)
        try:
            with open(l2_path, "w", encoding="utf-8") as f:
                f.write(py_source)
        except OSError:
            pass

    def clear(self) -> None:
        """Clear all caches."""
        self._l1_cache.clear()
        if os.path.exists(self.cache_dir):
            try:
                for filename in os.listdir(self.cache_dir):
                    if filename.endswith(".py"):
                        os.remove(os.path.join(self.cache_dir, filename))
            except OSError:
                pass

cache_manager = CacheManager()
