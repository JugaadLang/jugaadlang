import json
import os
from pathlib import Path
from typing import Any

from jugaadlang.lexer.tokens import register_custom_keywords

def load_config() -> None:
    """
    Attempts to load a 'jug.json' config file from the current working directory.
    If found, applies custom keyword mappings to the lexer.
    """
    config_path = Path.cwd() / "jug.json"
    if not config_path.exists():
        return
        
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        if "keywords" in config and isinstance(config["keywords"], dict):
            register_custom_keywords(config["keywords"])
    except Exception as e:
        print(f"Warning: Failed to load custom configurations from jug.json: {e}")
