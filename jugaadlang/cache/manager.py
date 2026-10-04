"""
Three-tier caching system for JugaadLang.
L1: In-Memory cache (fast lookups within same process/session).
L2: Disk-based AST caching in JSON format (`.jugc`).
L3: Disk-based Bytecode caching via marshal (`.jugb`).
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import marshal
import os
from types import CodeType
from typing import Any, Optional

from .. import __version__
from ..ast_nodes import nodes as ast_nodes
from ..ast_nodes.nodes import Module
from ..events.bus import event_bus

CACHE_VERSION: int = 1

NODE_TYPE_MAP: dict[str, type[ast_nodes.ASTNode]] = {
    name: cls
    for name, cls in ast_nodes.__dict__.items()
    if isinstance(cls, type) and issubclass(cls, ast_nodes.ASTNode)
}

def serialize_ast(node: Any) -> Any:
    if isinstance(node, ast_nodes.ASTNode):
        data = {"_type": node.__class__.__name__}
        for field in dataclasses.fields(node):
            val = getattr(node, field.name)
            data[field.name] = serialize_ast(val)
        return data
    elif isinstance(node, list):
        return [serialize_ast(item) for item in node]
    elif isinstance(node, dict):
        return {k: serialize_ast(v) for k, v in node.items()}
    elif node is Ellipsis:
        return {"_type": "Ellipsis"}
    else:
        return node

def deserialize_ast(data: Any) -> Any:
    if isinstance(data, dict):
        if "_type" in data:
            cls_name = data["_type"]
            if cls_name == "Ellipsis":
                return Ellipsis
            cls = NODE_TYPE_MAP.get(cls_name)
            if not cls:
                raise ValueError(f"Unknown AST node type: {cls_name}")
            kwargs = {k: deserialize_ast(v) for k, v in data.items() if k != "_type"}
            return cls(**kwargs)
        else:
            return {k: deserialize_ast(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [deserialize_ast(item) for item in data]
    else:
        return data

class CacheManager:
    def __init__(self, cache_dir: str = "__jugcache__"):
        self._l1_ast_cache: dict[str, Module] = {}
        self._l1_bytecode_cache: dict[str, CodeType] = {}
        self.cache_dir = cache_dir
        if os.environ.get("JUG_NO_CACHE", "").lower() in ("1", "true", "yes"):
            self.enabled = False
        else:
            self.enabled = True
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

    def _get_l2_path(self, key: str, filename: Optional[str] = None, ext: str = ".jugc") -> str:
        # If filename is given, group cache by basename if desired, but here we just use cache_dir
        return os.path.join(self.cache_dir, f"{key}{ext}")

    def get_ast(self, source: str, filename: Optional[str] = None) -> Optional[Module]:
        if not self.enabled:
            return None
        key = self._get_key(source)
        if key in self._l1_ast_cache:
            self.hits += 1
            event_bus.emit("CACHE_HIT", {"source_hash": key, "filename": filename, "tier": "L1_AST"})
            return copy.deepcopy(self._l1_ast_cache[key])
        
        cache_path = self._get_l2_path(key, filename=filename, ext=".jugc")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                if not isinstance(payload, dict):
                    raise ValueError("Cache file is not a valid JSON dictionary")
                if payload.get("cache_version") != CACHE_VERSION:
                    raise ValueError("Incompatible cache version")
                if payload.get("jugaadlang_version") != __version__:
                    raise ValueError("Incompatible JugaadLang version")
                if payload.get("source_hash") != key:
                    raise ValueError("Source hash mismatch")
                ast_data = payload.get("ast")
                if not isinstance(ast_data, dict) or ast_data.get("_type") != "Module":
                    raise ValueError("Missing or invalid Module AST in cache")
                ast_mod = deserialize_ast(ast_data)
                if not isinstance(ast_mod, Module):
                    raise ValueError("Deserialized object is not an AST Module")
                
                self._l1_ast_cache[key] = ast_mod
                self.hits += 1
                event_bus.emit("CACHE_HIT", {"source_hash": key, "filename": filename, "tier": "L2_AST"})
                return copy.deepcopy(ast_mod)
            except Exception as e:
                self.misses += 1
                event_bus.emit("CACHE_MISS", {"source_hash": key, "filename": filename, "reason": f"error: {str(e)}"})
                return None
        self.misses += 1
        return None

    def set_ast(self, source: str, ast_mod: Module, filename: Optional[str] = None) -> None:
        if not self.enabled:
            return
        key = self._get_key(source)
        self._l1_ast_cache[key] = copy.deepcopy(ast_mod)
        tmp_path: Optional[str] = None
        try:
            self._ensure_cache_dir()
            target_path = self._get_l2_path(key, filename=filename, ext=".jugc")
            tmp_path = self._get_l2_path(key, filename=filename, ext=f".tmp.{os.getpid()}.jugc")
            payload = {
                "cache_version": CACHE_VERSION,
                "jugaadlang_version": __version__,
                "source_hash": key,
                "filename": os.path.basename(filename) if filename else None,
                "ast": serialize_ast(ast_mod),
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

    def get_bytecode(self, source: str, filename: Optional[str] = None) -> Optional[CodeType]:
        if not self.enabled:
            return None
        key = self._get_key(source)
        if key in self._l1_bytecode_cache:
            self.hits += 1
            return self._l1_bytecode_cache[key]
            
        cache_path = self._get_l2_path(key, filename=filename, ext=".jugb")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "rb") as f:
                    code_obj = marshal.load(f)
                if isinstance(code_obj, CodeType):
                    self._l1_bytecode_cache[key] = code_obj
                    self.hits += 1
                    return code_obj
            except Exception:
                pass
        self.misses += 1
        return None

    def set_bytecode(self, source: str, code_obj: CodeType, filename: Optional[str] = None) -> None:
        if not self.enabled:
            return
        key = self._get_key(source)
        self._l1_bytecode_cache[key] = code_obj
        tmp_path: Optional[str] = None
        try:
            self._ensure_cache_dir()
            target_path = self._get_l2_path(key, filename=filename, ext=".jugb")
            tmp_path = self._get_l2_path(key, filename=filename, ext=f".tmp.{os.getpid()}.jugb")
            with open(tmp_path, "wb") as f:
                marshal.dump(code_obj, f)
            os.replace(tmp_path, target_path)
        except Exception:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

    def clear(self) -> None:
        self._l1_ast_cache.clear()
        self._l1_bytecode_cache.clear()
        self.hits = 0
        self.misses = 0
        self._clean_dir(self.cache_dir)
        cwd_cache = os.path.join(os.getcwd(), "__jugcache__")
        if os.path.exists(cwd_cache) and os.path.abspath(cwd_cache) != os.path.abspath(self.cache_dir):
            self._clean_dir(cwd_cache)

    def _clean_dir(self, directory: str) -> None:
        if os.path.exists(directory):
            try:
                for filename in os.listdir(directory):
                    if filename.endswith(".jugc") or filename.endswith(".jugb") or ".tmp." in filename:
                        try:
                            os.remove(os.path.join(directory, filename))
                        except OSError:
                            pass
            except OSError:
                pass

    def invalidate(self, source: str, filename: Optional[str] = None) -> None:
        key = self._get_key(source)
        self._l1_ast_cache.pop(key, None)
        self._l1_bytecode_cache.pop(key, None)
        for ext in (".jugc", ".jugb"):
            path = self._get_l2_path(key, filename=filename, ext=ext)
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass

cache_manager = CacheManager()
