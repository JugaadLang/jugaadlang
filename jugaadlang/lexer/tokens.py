"""
JugaadLang Token Types and Keyword Mapping.
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # ── Literals ──────────────────────────────────────────────────────
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    FSTRING = auto()

    # ── Identifier ───────────────────────────────────────────────────
    IDENTIFIER = auto()

    # ── JugaadLang Keywords ──────────────────────────────────────────
    BOLO = auto()  # print
    POOCHHO = auto()  # input
    AGAR = auto()  # if
    SHAYAD = auto()  # elif
    WARNA = auto()  # else
    GHUMO = auto()  # for
    JABTAK = auto()  # while
    BANAO = auto()  # def
    WAPAS = auto()  # return
    USTAD = auto()  # class
    KHUD = auto()  # self
    LAO = auto()  # import
    SE = auto()  # from
    RUKJA = auto()  # break
    CHALTE_RAHO = auto()  # continue
    KOSHISH = auto()  # try
    GADBAD = auto()  # except
    AAKHIR_ME = auto()  # finally
    UDAO = auto()  # raise
    SAHI = auto()  # True
    GALAT = auto()  # False
    KUCH_NAHI = auto()  # None
    AUR = auto()  # and
    YA = auto()  # or
    NAHI = auto()  # not
    TEZ = auto()  # async
    INTEZAAR = auto()  # await
    BAANTO = auto()  # yield
    THEEK_HAI = auto()  # pass
    SABKA = auto()  # global
    CHOTA_FUNKSHAN = auto()  # lambda
    MEIN = auto()  # in
    MEIN_NAHI = auto()  # not in  (compound keyword)
    HAI = auto()  # is
    NAHI_HAI = auto()  # is not  (compound keyword)
    BULAWO = auto()  # call (optional sugar)
    DEL = auto()  # del (kept as English for now)
    NONLOCAL = auto()  # nonlocal
    WITH = auto()  # with
    AS = auto()  # as
    ASSERT = auto()  # assert
    AGAR_MATCH = auto()  # match
    KAAND = auto()  # case

    # ── Operators ────────────────────────────────────────────────────
    PLUS = auto()  # +
    MINUS = auto()  # -
    STAR = auto()  # *
    SLASH = auto()  # /
    DOUBLESLASH = auto()  # //
    PERCENT = auto()  # %
    DOUBLESTAR = auto()  # **
    EQ = auto()  # ==
    NEQ = auto()  # !=
    LT = auto()  # <
    GT = auto()  # >
    LTE = auto()  # <=
    GTE = auto()  # >=
    ASSIGN = auto()  # =
    PLUS_ASSIGN = auto()  # +=
    MINUS_ASSIGN = auto()  # -=
    STAR_ASSIGN = auto()  # *=
    SLASH_ASSIGN = auto()  # /=
    PERCENT_ASSIGN = auto()  # %=
    DOUBLESTAR_ASSIGN = auto()  # **=
    DOUBLESLASH_ASSIGN = auto()  # //=
    ARROW = auto()  # ->
    WALRUS = auto()  # :=
    AT = auto()  # @
    AT_ASSIGN = auto()  # @=
    TILDE = auto()  # ~
    AMP = auto()  # &
    PIPE = auto()  # |
    CARET = auto()  # ^
    LSHIFT = auto()  # <<
    RSHIFT = auto()  # >>
    AMP_ASSIGN = auto()  # &=
    PIPE_ASSIGN = auto()  # |=
    CARET_ASSIGN = auto()  # ^=
    LSHIFT_ASSIGN = auto()  # <<=
    RSHIFT_ASSIGN = auto()  # >>=

    # ── Delimiters ───────────────────────────────────────────────────
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    COMMA = auto()  # ,
    DOT = auto()  # .
    COLON = auto()  # :
    SEMICOLON = auto()  # ;
    ELLIPSIS = auto()  # ...

    # ── Layout ───────────────────────────────────────────────────────
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()

    # ── Special ──────────────────────────────────────────────────────
    COMMENT = auto()
    EOF = auto()


# ── Keyword string → TokenType mapping ───────────────────────────────
KEYWORDS: dict[str, TokenType] = {
    "bolo": TokenType.BOLO,
    "poochho": TokenType.POOCHHO,
    "agar": TokenType.AGAR,
    "shayad": TokenType.SHAYAD,
    "warna": TokenType.WARNA,
    "ghumo": TokenType.GHUMO,
    "jabtak": TokenType.JABTAK,
    "banao": TokenType.BANAO,
    "wapas": TokenType.WAPAS,
    "ustad": TokenType.USTAD,
    "khud": TokenType.KHUD,
    "lao": TokenType.LAO,
    "se": TokenType.SE,
    "rukja": TokenType.RUKJA,
    "chalte_raho": TokenType.CHALTE_RAHO,
    "koshish": TokenType.KOSHISH,
    "gadbad": TokenType.GADBAD,
    "aakhir_me": TokenType.AAKHIR_ME,
    "udao": TokenType.UDAO,
    "sahi": TokenType.SAHI,
    "galat": TokenType.GALAT,
    "kuch_nahi": TokenType.KUCH_NAHI,
    "aur": TokenType.AUR,
    "ya": TokenType.YA,
    "nahi": TokenType.NAHI,
    "tez": TokenType.TEZ,
    "intezaar": TokenType.INTEZAAR,
    "baanto": TokenType.BAANTO,
    "theek_hai": TokenType.THEEK_HAI,
    "sabka": TokenType.SABKA,
    "chota_funkshan": TokenType.CHOTA_FUNKSHAN,
    "mein": TokenType.MEIN,
    "mein_nahi": TokenType.MEIN_NAHI,
    "hai": TokenType.HAI,
    "nahi_hai": TokenType.NAHI_HAI,
    "bulawo": TokenType.BULAWO,
    "del": TokenType.DEL,
    "hatao": TokenType.DEL,
    "nonlocal": TokenType.NONLOCAL,
    "gair_local": TokenType.NONLOCAL,
    "with": TokenType.WITH,
    "ke_saath": TokenType.WITH,
    "as": TokenType.AS,
    "jaise": TokenType.AS,
    "assert": TokenType.ASSERT,
    "pakka": TokenType.ASSERT,
    "agar_match": TokenType.AGAR_MATCH,
    "kaand": TokenType.KAAND,
}

def register_custom_keywords(custom_mapping: dict[str, str | list[str]]) -> None:
    """
    Dynamically register custom keywords/aliases mapped to the standard English/Python keyword equivalents.
    For example: `{"print": "chhap"}` or `{"print": ["chhap", "bolo"]}`
    """
    # Inverse map to find the TokenType for a given standard token name
    # e.g., "print" -> TokenType.BOLO (since bolo maps to print conceptually)
    # Wait, the config uses english equivalents or standard jugaadlang names?
    # According to plan: `print = ["chhap", "bolo"]`. So the key is the conceptual name or default jug keyword.
    
    # We can create a reverse mapping from string representation of TokenType (like BOLO) 
    # to the enum type to make it easy.
    type_map = {t.name.lower(): t for t in TokenType}
    
    # Also map common python names to their JugaadLang TokenTypes for ease of use
    python_to_jug = {
        "print": TokenType.BOLO,
        "input": TokenType.POOCHHO,
        "if": TokenType.AGAR,
        "elif": TokenType.SHAYAD,
        "else": TokenType.WARNA,
        "for": TokenType.GHUMO,
        "while": TokenType.JABTAK,
        "def": TokenType.BANAO,
        "return": TokenType.WAPAS,
        "class": TokenType.USTAD,
        "self": TokenType.KHUD,
        "import": TokenType.LAO,
        "from": TokenType.SE,
        "break": TokenType.RUKJA,
        "continue": TokenType.CHALTE_RAHO,
        "try": TokenType.KOSHISH,
        "except": TokenType.GADBAD,
        "finally": TokenType.AAKHIR_ME,
        "raise": TokenType.UDAO,
        "true": TokenType.SAHI,
        "false": TokenType.GALAT,
        "none": TokenType.KUCH_NAHI,
        "and": TokenType.AUR,
        "or": TokenType.YA,
        "not": TokenType.NAHI,
        "async": TokenType.TEZ,
        "await": TokenType.INTEZAAR,
        "yield": TokenType.BAANTO,
        "pass": TokenType.THEEK_HAI,
        "global": TokenType.SABKA,
        "lambda": TokenType.CHOTA_FUNKSHAN,
        "in": TokenType.MEIN,
        "is": TokenType.HAI,
        "del": TokenType.DEL,
        "nonlocal": TokenType.NONLOCAL,
        "with": TokenType.WITH,
        "as": TokenType.AS,
        "assert": TokenType.ASSERT,
        "match": TokenType.AGAR_MATCH,
        "case": TokenType.KAAND,
    }

    for key, aliases in custom_mapping.items():
        # Find the correct TokenType
        key_lower = key.lower()
        target_type = None
        if key_lower in type_map:
            target_type = type_map[key_lower]
        elif key_lower in python_to_jug:
            target_type = python_to_jug[key_lower]
        
        if not target_type:
            continue
            
        if isinstance(aliases, str):
            aliases = [aliases]
            
        for alias in aliases:
            KEYWORDS[alias] = target_type

# Human-readable names for error messages
TOKEN_NAMES: dict[TokenType, str] = {
    TokenType.INT: "integer",
    TokenType.FLOAT: "float",
    TokenType.STRING: "string",
    TokenType.IDENTIFIER: "identifier",
    TokenType.NEWLINE: "newline",
    TokenType.INDENT: "indent",
    TokenType.DEDENT: "dedent",
    TokenType.EOF: "end of file",
    TokenType.LPAREN: "'('",
    TokenType.RPAREN: "')'",
    TokenType.LBRACKET: "'['",
    TokenType.RBRACKET: "']'",
    TokenType.LBRACE: "'{'",
    TokenType.RBRACE: "'}'",
    TokenType.COMMA: "','",
    TokenType.DOT: "'.'",
    TokenType.COLON: "':'",
    TokenType.ASSIGN: "'='",
    TokenType.EQ: "'=='",
    TokenType.ARROW: "'->'",
}


@dataclass(slots=True)
class Token:
    """A single lexical token."""

    type: TokenType
    value: str
    line: int
    col: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.col})"

    def is_keyword(self) -> bool:
        return self.type in KEYWORDS.values()
