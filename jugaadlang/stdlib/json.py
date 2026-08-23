"""
json — JugaadLang JSON parser and stringifier.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Optional

# Temporarily remove local dir from path to import the real stdlib json
local_dir = os.path.dirname(__file__)
paths_to_remove = [local_dir, ""]
removed_paths = []

for p in list(sys.path):
    if os.path.abspath(p) == os.path.abspath(local_dir):
        sys.path.remove(p)
        removed_paths.append(p)

import json as _real_json  # noqa: E402

# Restore path
for p in removed_paths:
    sys.path.insert(0, p)

# Re-export everything from real json
globals().update({k: v for k, v in _real_json.__dict__.items() if not k.startswith("__")})


def banao_string(obj: Any, indent: Optional[int] = None) -> str:
    """Convert object to JSON string (JSON.stringify / json.dumps)."""
    return _real_json.dumps(obj, indent=indent)


def banao_object(string: str) -> Any:
    """Parse JSON string to object (JSON.parse / json.loads)."""
    return _real_json.loads(string)
