import json
import os
import tempfile
import sys
from pathlib import Path

from jugaadlang.lexer.lexer import Lexer
from jugaadlang.lexer.tokens import TokenType, KEYWORDS
from jugaadlang.config import load_config

def test_custom_keyword_registration():
    # Save current working directory
    original_cwd = Path.cwd()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Change cwd to tmpdir so load_config finds jug.json there
        os.chdir(tmp_path)
        
        try:
            # Create a jug.json with custom keywords
            config = {
                "keywords": {
                    "print": ["chhap", "likho"],
                    "if": "yadi",
                    "else": "nahi_to",
                    "def": "vidhi"
                }
            }
            
            with open(tmp_path / "jug.json", "w", encoding="utf-8") as f:
                json.dump(config, f)
                
            # Load config
            load_config()
            
            # Verify keywords were registered in the token map
            assert "chhap" in KEYWORDS
            assert "likho" in KEYWORDS
            assert "yadi" in KEYWORDS
            assert "nahi_to" in KEYWORDS
            assert "vidhi" in KEYWORDS
            
            assert KEYWORDS["chhap"] == TokenType.BOLO
            assert KEYWORDS["yadi"] == TokenType.AGAR
            assert KEYWORDS["nahi_to"] == TokenType.WARNA
            assert KEYWORDS["vidhi"] == TokenType.BANAO
            
            # Verify the lexer correctly tokenizes a custom keyword script
            source = """
            vidhi test():
                yadi 1 == 1:
                    chhap("Success")
                nahi_to:
                    likho("Fail")
            """
            
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT, TokenType.EOF)]
            
            assert TokenType.BANAO in types  # 'vidhi'
            assert TokenType.AGAR in types  # 'yadi'
            assert TokenType.BOLO in types  # 'chhap'
            
        finally:
            # Restore cwd
            os.chdir(original_cwd)
