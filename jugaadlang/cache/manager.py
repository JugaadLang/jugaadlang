"""
Two-tier AST and precompiled representation caching system for JugaadLang.
L1: In-Memory cache (fast lookups within same process/session).
L2: Disk-based caching in deterministic `__jugcache__/` directory.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import os
from typing import Any, Optional

from .. import __version__
from ..ast_nodes import nodes as ast_nodes
from ..ast_nodes.nodes import Module
from ..events.bus import event_bus

CACHE_VERSION: int = 1

# Allowed AST node classes strictly restricted to ASTNode subclasses in nodes module
NODE_TYPE_MAP: dict[str, type[ast_nodes.ASTNode]] = {
    name: cls
    for name, cls in ast_nodes.__dict__.items()
    if isinstance(cls, type) and issubclass(cls, ast_nodes.ASTNode)
}


def serialize_ast(node: Any) -> Any:
    """
    Safely serialize a JugaadLang AST node tree into a JSON-compatible dictionary.
    Only primitive scalars (int, float, str, bool, None) and ASTNode instances
    are serialized.
    """
    if isinstance(node, ast_nodes.ASTNode):
        data: dict[str, Any] = {"_type": type(node).__name__}
        for f in dataclasses.fields(node):
            val = getattr(node, f.name)
            if val is Ellipsis:
                data[f.name] = {"_special": "ellipsis"}
            elif isinstance(val, list):
                data[f.name] = [serialize_ast(item) for item in val]
            elif isinstance(val, ast_nodes.ASTNode):
                data[f.name] = serialize_ast(val)
            else:
                data[f.name] = val
        return data
    elif node is Ellipsis:
        return {"_special": "ellipsis"}
    elif isinstance(node, list):
        return [serialize_ast(item) for item in node]
    elif isinstance(node, (str, int, float, bool)) or node is None:
        return node
    else:
        return str(node)


def deserialize_ast(data: Any) -> Any:
    """
    Safely reconstruct a JugaadLang AST node tree from a dictionary.
    Only classes defined in `jugaadlang.ast_nodes.nodes` inheriting from `ASTNode`
    can be instantiated, preventing arbitrary code or object execution.
    """
    if isinstance(data, dict):
        if data.get("_special") == "ellipsis":
            return Ellipsis
        if "_type" in data:
            node_type = data["_type"]
            cls = NODE_TYPE_MAP.get(node_type)
            if cls is None:
                raise ValueError(f"Unknown or unauthorized AST node type: {node_type}")
            kwargs: dict[str, Any] = {}
            for f in dataclasses.fields(cls):
                if f.name in data:
                    raw_val = data[f.name]
                    if isinstance(raw_val, list):
                        kwargs[f.name] = [deserialize_ast(x) for x in raw_val]
                    elif isinstance(raw_val, dict):
                        kwargs[f.name] = deserialize_ast(raw_val)
                    else:
                        kwargs[f.name] = raw_val
                elif f.default is not dataclasses.MISSING:
                    kwargs[f.name] = f.default
                elif f.default_factory is not dataclasses.MISSING:
                    kwargs[f.name] = f.default_factory()
            return cls(**kwargs)
        return {k: deserialize_ast(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [deserialize_ast(x) for x in data]
    return data


class CacheManager:
    """
    Two-tier AST caching system for JugaadLang.
    L1: In-Memory dictionary for rapid access.
    L2: Disk-based caching in deterministic `__jugcache__` directory with SHA-256 validation.
    """

    def __init__(self, cache_dir: str = "__jugcache__", enabled: bool = True) -> None:
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

    def _resolve_cache_dir(self, filename: Optional[str] = None) -> str:
        """Resolve the deterministic directory where cache files should be saved."""
        if self.cache_dir != "__jugcache__":
            return self.cache_dir
        if filename and filename not in ("<stdin>", "<repl>", ""):
            try:
                file_dir = os.path.dirname(os.path.abspath(filename))
                if os.path.exists(file_dir) and os.path.isdir(file_dir):
                    return os.path.join(file_dir, "__jugcache__")
            except Exception:
                pass
        return os.path.join(os.getcwd(), "__jugcache__")

    def _get_l2_path(
        self, key: str, filename: Optional[str] = None, ext: str = ".jugc"
    ) -> str:
        cache_dir = self._resolve_cache_dir(filename)
        return os.path.join(cache_dir, f"{key}{ext}")

    def get_ast(self, source: str, filename: Optional[str] = None) -> Optional[Module]:
        """
        Get cached JugaadLang AST Module for the given source code.
        Returns None on cache miss, corruption, hash mismatch, or version incompatibility.
        """
        if not self.enabled:
            return None

        key = self._get_key(source)

        # 1. Check L1 in-memory cache
        if key in self._l1_ast_cache:
            self.hits += 1
            event_bus.emit(
                "CACHE_HIT",
                {"source_hash": key, "filename": filename, "tier": "L1"},
            )
            return copy.deepcopy(self._l1_ast_cache[key])

        # 2. Check L2 disk cache
        cache_path = self._get_l2_path(key, filename=filename, ext=".jugc")
        if not os.path.exists(cache_path):
            self.misses += 1
            event_bus.emit(
                "CACHE_MISS",
                {"source_hash": key, "filename": filename, "reason": "not_found"},
            )
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                payload = json.load(f)

            if not isinstance(payload, dict):
                raise ValueError("Cache payload must be a JSON object")

            if payload.get("cache_version") != CACHE_VERSION:
                raise ValueError(
                    f"Incompatible cache version: {payload.get('cache_version')}"
                )

            if payload.get("jugaadlang_version") != __version__:
                raise ValueError(
                    f"Incompatible JugaadLang version: {payload.get('jugaadlang_version')}"
                )

            if payload.get("source_hash") != key:
                raise ValueError("Source hash mismatch")

            ast_data = payload.get("ast")
            if not isinstance(ast_data, dict) or ast_data.get("_type") != "Module":
                raise ValueError("Missing or invalid Module AST in cache")

            ast_mod = deserialize_ast(ast_data)
            if not isinstance(ast_mod, Module):
                raise ValueError("Deserialized object is not an AST Module")

            self._l1_ast_cache[key] = ast_mod
            if payload.get("py_source"):
                self._l1_py_cache[key] = payload["py_source"]

            self.hits += 1
            event_bus.emit(
                "CACHE_HIT",
                {"source_hash": key, "filename": filename, "tier": "L2"},
            )
            return copy.deepcopy(ast_mod)

        except Exception as e:
            self.misses += 1
            event_bus.emit(
                "CACHE_MISS",
                {"source_hash": key, "filename": filename, "reason": f"error: {str(e)}"},
            )
            return None

    def set_ast(
        self,
        source: str,
        ast_mod: Module,
        filename: Optional[str] = None,
        py_source: Optional[str] = None,
    ) -> None:
        """
        Store JugaadLang AST Module in both L1 and L2 caches.
        Writes are atomic to prevent reading corrupted partial files.
        Failures to write to disk are caught and suppressed so normal execution is never interrupted.
        """
        if not self.enabled:
            return

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
                with open(legacy_path, "r", encoding="utf-8") as f:
                    py_source = f.read()
                self._l1_py_cache[key] = py_source
                return py_source
            except OSError:
                pass

        return None

    def set(self, source: str, py_source: str, filename: Optional[str] = None) -> None:
        """
        Store compiled Python source in cache (for backward compatibility).
        """
        if not self.enabled:
            return

        key = self._get_key(source)

        # Set L1 cache
        self._l1_py_cache[key] = py_source

        # Set L2 cache
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
                "ast": None,
                "py_source": py_source,
            }

            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False)

            os.replace(tmp_path, target_path)

            # If a custom cache directory was specified, also write legacy .py
            if self.cache_dir != "__jugcache__":
                legacy_path = os.path.join(cache_dir, f"{key}.py")
                with open(legacy_path, "w", encoding="utf-8") as f:
                    f.write(py_source)

        except Exception:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
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
                for filename in os.listdir(directory):
                    if (
                        filename.endswith(".jugc")
                        or filename.endswith(".py")
                        or ".tmp." in filename
                    ):
                        try:
                            os.remove(os.path.join(directory, filename))
                        except OSError:
                            pass
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
