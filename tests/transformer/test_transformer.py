import pytest
import ast
from jugaadlang.lexer.lexer import Lexer
from jugaadlang.parser.parser import Parser
from jugaadlang.transformer.to_python import JugaadToPythonTransformer

def transpile(source: str) -> str:
    """Helper to parse and transpile JugaadLang source to Python source string."""
    lexer = Lexer(source, "<test>")
    tokens = lexer.tokenize()
    parser = Parser(tokens, "<test>", source)
    ast_mod = parser.parse()
    transformer = JugaadToPythonTransformer("<test>")
    py_ast = transformer.transform(ast_mod)
    return ast.unparse(py_ast)

@pytest.mark.parametrize(
    "jug_source, expected_py_source",
    [
        # Simple statements and primitive keywords
        ("bolo('hello')", "print('hello')"),
        ("x = poochho()", "x = input()"),
        ("x = khud", "x = self"),
        
        # Operators
        ("a = 1 + 2 * 3 - 4 / 2", "a = 1 + 2 * 3 - 4 / 2"),
        ("a = 2 ** 3", "a = 2 ** 3"),
        ("a = 5 % 2", "a = 5 % 2"),
        ("a = 5 << 1", "a = 5 << 1"),
        ("b = sahi aur galat ya kuch_nahi", "b = True and False or None"),
        ("b = nahi sahi", "b = not True"),
        ("c = 5 == 5 aur 4 != 3", "c = 5 == 5 and 4 != 3"),
        ("c = x mein y aur z mein_nahi w", "c = x in y and z not in w"),
        ("c = x hai y aur z nahi_hai w", "c = x is y and z is not w"),
        
        # Conditionals
        (
            "agar x > 5:\n    bolo('bada')\nshayad x == 5:\n    bolo('barabar')\nwarna:\n    bolo('chota')",
            "if x > 5:\n    print('bada')\nelif x == 5:\n    print('barabar')\nelse:\n    print('chota')"
        ),
        
        # Loops
        (
            "ghumo i mein kramwar([3, 1, 2]):\n    bolo(i)",
            "for i in sorted([3, 1, 2]):\n    print(i)"
        ),
        (
            "jabtak x < 10:\n    x += 1\n    agar x == 5:\n        chalte_raho\n    agar x == 9:\n        rukja",
            "while x < 10:\n    x += 1\n    if x == 5:\n        continue\n    if x == 9:\n        break"
        ),
        
        # Functions and Lambda
        (
            "banao add(a, b=0):\n    wapas a + b",
            "def add(a, b=0):\n    return a + b"
        ),
        (
            "f = chota_funkshan x: x * 2",
            "f = lambda x: x * 2"
        ),
        
        # Classes
        (
            "ustad Animal:\n    banao shuru(khud, name):\n        khud.name = name\n\n    banao speak(khud):\n        wapas 'noise'",
            "class Animal:\n\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return 'noise'"
        ),
        
        # Exceptions
        (
            "koshish:\n    1 / 0\ngadbad ZeroDivisionError jaise e:\n    bolo(e)\naakhir_me:\n    bolo('done')",
            "try:\n    1 / 0\nexcept ZeroDivisionError as e:\n    print(e)\nfinally:\n    print('done')"
        ),
        
        # Context Manager
        (
            "ke_saath kholo('file.txt') jaise f:\n    bolo(f.read())",
            "with open('file.txt') as f:\n    print(f.read())"
        ),
        
        # Builtins mapping
        (
            "x = lambaee(suchi()) + adhiktam([1,2]) + nyuntam([1])",
            "x = len(list()) + max([1, 2]) + min([1])"
        ),
        
        # List/Dict Comprehension
        (
            "squares = [x**2 ghumo x mein ginti([1,2,3])]",
            "squares = [x ** 2 for x in enumerate([1, 2, 3])]"
        ),
        
        # Asserts & Deletions
        (
            "pakka x == 5",
            "assert x == 5"
        ),
        (
            "hatao x",
            "del x"
        ),
    ]
)
def test_transformer_constructs(jug_source, expected_py_source):
    result = transpile(jug_source)
    assert result == expected_py_source
