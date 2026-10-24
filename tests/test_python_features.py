"""
Tests for the Python 3.14 / 3.15 features JugaadLang supports:

* t-strings (PEP 750)            — 3.14+, degrade to f-strings on older Pythons
* bracket-less `except` (PEP 758) — emits a Tuple, valid on every version
* `{{`/`}}` escapes + `!r`/`:spec` interpolation syntax
* comprehension unpacking (PEP 798) — native on 3.15+, lowered on older Pythons
* lazy imports (PEP 810)          — `sust lao x`, native on 3.15+
* `frozendict`/`sentinel` builtins (PEP 814 / PEP 661) — 3.15+
* version-aware bytecode cache keys
"""

from __future__ import annotations

import ast
import sys

import pytest

from jugaadlang.ast_nodes.nodes import (
    Assign,
    Constant,
    DictComp,
    FormattedValue,
    GeneratorExp,
    Import,
    ImportFrom,
    Interpolation,
    JoinedStr,
    List,
    ListComp,
    SetComp,
    Starred,
    TemplateStr,
)
from jugaadlang.errors.messages import JugaadError
from jugaadlang.lexer.lexer import Lexer, LexerError
from jugaadlang.lexer.tokens import TokenType
from jugaadlang.parser.parser import ParseError, Parser
from jugaadlang.runtime.interpreter import JugaadInterpreter
from jugaadlang.transformer.to_python import JugaadToPythonTransformer

PY314 = sys.version_info >= (3, 14)
PY315 = sys.version_info >= (3, 15)


# ── Helpers ────────────────────────────────────────────────────────────────────


def tokenize(source: str) -> list:
    return Lexer(source, "<test>").tokenize()


def parse(source: str):
    return Parser(tokenize(source), "<test>", source).parse()


def to_py(source: str) -> ast.Module:
    return JugaadToPythonTransformer("<test>").transform(parse(source))


def unparse(source: str) -> str:
    return ast.unparse(to_py(source))


def execute(source: str) -> dict:
    """Compile the transpiled module with the running interpreter and run it."""
    code = compile(to_py(source), "<test>", "exec")
    namespace: dict = {}
    exec(code, namespace, namespace)
    return namespace


def run(source: str, capsys) -> str:
    JugaadInterpreter("features.jug").run(source)
    # rstrip only: left padding matters for format-spec assertions
    return capsys.readouterr().out.rstrip("\n")


# ── Lexer: t-strings (PEP 750) ────────────────────────────────────────────────


def test_tstring_token_type():
    tokens = tokenize('t"namaste {naam}"')
    assert tokens[0].type is TokenType.TSTRING
    assert tokens[0].value == "namaste {naam}"


@pytest.mark.parametrize("literal", ["t'hi'", 't"""hi"""', "t'''hi'''"])
def test_tstring_prefix_variants(literal):
    assert tokenize(literal)[0].type is TokenType.TSTRING


def test_fstring_and_plain_string_still_tokenize():
    assert tokenize('f"{x}"')[0].type is TokenType.FSTRING
    assert tokenize('"plain"')[0].type is TokenType.STRING


@pytest.mark.parametrize("source", ["test = 1", "tf = 2", "tr = 3", "f = 4", "t = 5"])
def test_prefix_letters_still_work_as_identifiers(source):
    tokens = tokenize(source)
    assert tokens[0].type is TokenType.IDENTIFIER


def test_raw_string_prefix_is_rejected_clearly():
    with pytest.raises(LexerError, match="Raw string"):
        tokenize(r'pattern = r"\d+"')


def test_conflicting_prefixes_are_rejected():
    with pytest.raises(LexerError, match="prefix"):
        tokenize('ft"x"')


# ── Parser: t-strings ─────────────────────────────────────────────────────────


def test_tstring_parses_into_template_str():
    module = parse('t"namaste {x}"')
    template = module.body[0].value
    assert isinstance(template, TemplateStr)
    assert template.values[0].value == "namaste "
    assert isinstance(template.values[1], Interpolation)
    assert template.values[1].str == "x"
    assert template.values[1].conversion == -1


def test_tstring_keeps_raw_expression_text():
    module = parse('t"{ x }"')
    assert module.body[0].value.values[0].str == " x "  # same as CPython's ast


def test_tstring_conversion_and_spec():
    module = parse('t"{x!r:>4}"')
    interpolation = module.body[0].value.values[0]
    assert interpolation.conversion == ord("r")
    assert isinstance(interpolation.format_spec, JoinedStr)
    assert interpolation.format_spec.values[0].value == ">4"


# ── Parser: f-string improvements ─────────────────────────────────────────────


def test_fstring_conversion_and_spec():
    module = parse('bolo(f"{w!r:0{d}d}")')
    joined = module.body[0].value.args[0]
    assert isinstance(joined, JoinedStr)
    formatted = joined.values[0]
    assert isinstance(formatted, FormattedValue)
    assert formatted.conversion == ord("r")
    assert isinstance(formatted.format_spec, JoinedStr)
    assert [type(v).__name__ for v in formatted.format_spec.values] == [
        "Constant",
        "FormattedValue",
        "Constant",
    ]
    assert formatted.format_spec.values[0].value == "0"
    assert formatted.format_spec.values[2].value == "d"
    assert formatted.format_spec.values[1].value.id == "d"


def test_fstring_double_braces_are_literal():
    module = parse('bolo(f"{{{1}}}")')
    values = module.body[0].value.args[0].values
    assert values[0].value == "{"
    assert values[-1].value == "}"


def test_fstring_debug_specifier_keeps_source_text():
    module = parse('bolo(f"{x=}")')
    joined = module.body[0].value.args[0]
    assert isinstance(joined, JoinedStr)
    assert [type(v).__name__ for v in joined.values] == ["Constant", "FormattedValue"]
    assert joined.values[0].value == "x="
    formatted = joined.values[1]
    assert formatted.conversion == ord("r")
    assert formatted.format_spec is None


def test_fstring_debug_specifier_keeps_spaces():
    module = parse('bolo(f"{x = }")')
    joined = module.body[0].value.args[0]
    assert joined.values[0].value == "x = "
    assert joined.values[1].value.id == "x"


def test_fstring_debug_specifier_with_format_spec():
    module = parse('bolo(f"{x=:>5}")')
    formatted = module.body[0].value.args[0].values[1]
    assert formatted.conversion == -1
    assert isinstance(formatted.format_spec, JoinedStr)


def test_fstring_debug_specifier_with_conversion():
    module = parse('bolo(f"{x=!s}")')
    formatted = module.body[0].value.args[0].values[1]
    assert formatted.conversion == ord("s")


def test_fstring_comparison_is_not_debug_specifier():
    module = parse('bolo(f"{x==42}")')
    joined = module.body[0].value.args[0]
    assert [type(v).__name__ for v in joined.values] == ["FormattedValue"]
    assert joined.values[0].conversion == -1


def test_tstring_debug_specifier():
    module = parse('t"{x=}"')
    template = module.body[0].value
    assert [type(v).__name__ for v in template.values] == ["Constant", "Interpolation"]
    assert template.values[0].value == "x="
    assert template.values[1].str == "x"
    assert template.values[1].conversion == ord("r")
# ── Parser: adjacent string literal concatenation ─────────────────────────────


def test_adjacent_plain_strings_concatenate():
    module = parse('msg = "a" "b" "c"')
    value = module.body[0].value
    assert isinstance(value, Constant)
    assert value.value == "abc"


def test_adjacent_plain_and_fstring_concatenate():
    module = parse('msg = "a" f"b{c}"')
    joined = module.body[0].value
    assert isinstance(joined, JoinedStr)
    assert [type(v).__name__ for v in joined.values] == ["Constant", "FormattedValue"]
    assert joined.values[0].value == "ab"
    assert joined.values[1].value.id == "c"


def test_adjacent_fstrings_merge_parts():
    module = parse('msg = f"a{c}" f"d{e}"')
    joined = module.body[0].value
    assert isinstance(joined, JoinedStr)
    assert [type(v).__name__ for v in joined.values] == [
        "Constant",
        "FormattedValue",
        "Constant",
        "FormattedValue",
    ]
    assert joined.values[0].value == "a"
    assert joined.values[2].value == "d"


def test_adjacent_tstrings_merge_parts():
    module = parse('msg = t"a{c}" t"d"')
    template = module.body[0].value
    assert isinstance(template, TemplateStr)
    assert [type(v).__name__ for v in template.values] == [
        "Constant",
        "Interpolation",
        "Constant",
    ]
    assert template.values[0].value == "a"
    assert template.values[2].value == "d"


def test_tstring_cannot_mix_with_plain_string():
    with pytest.raises(ParseError):
        parse('msg = "a" t"b"')
    with pytest.raises(ParseError):
        parse('msg = t"a" "b"')


def test_tstring_cannot_mix_with_fstring():
    with pytest.raises(ParseError):
        parse('msg = f"a" t"b"')
    with pytest.raises(ParseError):
        parse('msg = t"a" f"b"')


def test_adjacent_strings_runtime(capsys):
    source = (
        "x = 1\n"
        'bolo("a" "b" "c")\n'
        'bolo(f"v={x}" "!")\n'
        'bolo("do" "ne")\n'
        'bolo("multi" "word")\n'
        'bolo("part1" "part2", "part3", sep="-")\n'
    )
    lines = run(source, capsys).splitlines()
    assert lines == ["abc", "v=1!", "done", "multiword", "part1part2-part3"]


def test_adjacent_strings_value():
    namespace = execute('msg = "kon" "nichiwa"\nother = f"{msg}" "!"')
    assert namespace["msg"] == "konnichiwa"
    assert namespace["other"] == "konnichiwa!"
def test_named_unicode_escape_in_fstring():
    namespace = execute('msg = f"\\N{SNOWMAN} {1 + 1}"')
    assert namespace["msg"] == "\u2603 2"


# ── Parser: PEP 758 bracket-less except ───────────────────────────────────────


def test_bracketless_except_builds_tuple_type():
    module = parse("koshish:\n    1/0\ngadbad ValueError, TypeError:\n    pass")
    handler = module.body[0].handlers[0]
    assert isinstance(handler.type, tuple) or handler.type.__class__.__name__ == "Tuple"
    assert [elt.id for elt in handler.type.elts] == ["ValueError", "TypeError"]
    assert handler.name is None


def test_single_exception_handler_is_untouched():
    module = parse("koshish:\n    1/0\ngadbad ValueError:\n    pass")
    handler = module.body[0].handlers[0]
    assert handler.type.__class__.__name__ == "Name"


def test_bracketless_except_multiple_with_as_is_rejected():
    source = "koshish:\n    pass\ngadbad ValueError, TypeError as e:\n    pass"
    with pytest.raises(ParseError, match="bracket"):
        parse(source)


def test_bracketless_except_compiles_everywhere():
    source = (
        "koshish:\n"
        "    udao ValueError('x')\n"
        "gadbad ValueError, TypeError:\n"
        "    bolo('pakda')\n"
    )
    # Emitted as `except (ValueError, TypeError):`, valid on every supported Python
    compile(to_py(source), "<test>", "exec")


# ── Parser: PEP 798 comprehension unpacking + PEP 448 literals ────────────────


def test_list_comprehension_unpacking():
    module = parse("bolo([*l ghumo l mein lists])")
    comp = module.body[0].value.args[0]
    assert isinstance(comp, ListComp)
    assert isinstance(comp.elt, Starred)
    assert comp.elt.value.id == "l"


def test_set_comprehension_unpacking():
    comp = parse("bolo({*s ghumo s mein sets})").body[0].value.args[0]
    assert isinstance(comp, SetComp)
    assert isinstance(comp.elt, Starred)


def test_dict_comprehension_unpacking():
    comp = parse("bolo({**d ghumo d mein dicts})").body[0].value.args[0]
    assert isinstance(comp, DictComp)
    assert comp.unpack is True
    assert comp.value is None
    assert comp.key.id == "d"


def test_generator_unpacking():
    gen = parse("bolo((*l ghumo l mein lists))").body[0].value.args[0]
    assert isinstance(gen, GeneratorExp)
    assert isinstance(gen.elt, Starred)


def test_literal_unpacking():
    module = parse("a = [1]\nbolo([*a, 2])\nbolo({'x': 1, **{'y': 2}})")
    list_node = module.body[1].value.args[0]
    assert isinstance(list_node, List)
    assert isinstance(list_node.elts[0], Starred)
    dict_node = module.body[2].value.args[0]
    assert dict_node.keys[1] is None  # `**` marker


def test_comprehension_filter_still_parses():
    # `agar` after `mein` belongs to the comprehension, not a ternary
    comp = parse("bolo([x ghumo x mein range(4) agar x % 2 == 0])").body[0].value.args[0]
    assert len(comp.generators[0].ifs) == 1


def test_comprehension_accepts_multiple_filters_per_clause():
    module = parse("bolo([x ghumo x mein row agar x > 1 agar x < 5 agar x != 3])")
    comp = module.body[0].value.args[0]
    assert isinstance(comp, ListComp)
    assert len(comp.generators[0].ifs) == 3


def test_comprehension_multiple_clauses_multiple_filters():
    src = "bolo([(x, y) ghumo x mein a agar x > 0 ghumo y mein b agar y > 0 agar y != x])"
    comp = parse(src).body[0].value.args[0]
    assert len(comp.generators) == 2
    assert len(comp.generators[0].ifs) == 1
    assert len(comp.generators[1].ifs) == 2


def test_comprehension_multiple_filters_runtime(capsys):
    source = (
        "evens = [x ghumo x mein range(10) agar x > 2 agar x < 8 agar x % 2 == 0]\n"
        "bolo(evens)\n"
        "pairs = [(x, y) ghumo x mein range(3) agar x > 0 "
        "ghumo y mein range(3) agar y > 0 agar y != x]\n"
        "bolo(pairs)\n"
    )
    lines = run(source, capsys).splitlines()
    assert lines[0] == "[4, 6]"
    assert lines[1] == "[(1, 2), (2, 1)]"


def test_comprehension_multiple_filters_all_kinds(capsys):
    source = (
        "s = {x ghumo x mein range(6) agar x > 1 agar x < 5}\n"
        "d = {x: x * x ghumo x mein range(6) agar x > 1 agar x < 5}\n"
        "g = (x ghumo x mein range(6) agar x > 1 agar x < 5)\n"
        "bolo(sorted(s))\n"
        "bolo(d)\n"
        "bolo(sum(g))\n"
    )
    lines = run(source, capsys).splitlines()
    assert lines[0] == "[2, 3, 4]"
    assert lines[1] == "{2: 4, 3: 9, 4: 16}"
    assert lines[2] == "9"


def test_comprehension_ternary_still_works(capsys):
    source = (
        'labels = [("bada" agar x > 2 warna "chota") ghumo x mein range(5)]\n'
        "bolo(labels)\n"
        "kept = [x ghumo x mein range(5) agar (sahi agar x > 2 warna galat)]\n"
        "bolo(kept)\n"
    )
    lines = run(source, capsys).splitlines()
    assert lines[0] == "['chota', 'chota', 'chota', 'bada', 'bada']"
    assert lines[1] == "[3, 4]"


# ── Parser: PEP 810 lazy imports ──────────────────────────────────────────────


def test_sust_marks_import_as_lazy():
    module = parse("sust lao json")
    assert isinstance(module.body[0], Import)
    assert module.body[0].is_lazy is True
    assert module.body[0].names[0].name == "json"


def test_sust_marks_from_import_as_lazy():
    module = parse("sust se json lao dumps")
    assert isinstance(module.body[0], ImportFrom)
    assert module.body[0].is_lazy is True
    assert module.body[0].module == "json"


def test_regular_imports_are_not_lazy():
    module = parse("lao json\nse json lao dumps")
    assert module.body[0].is_lazy is False
    assert module.body[1].is_lazy is False


def test_sust_stays_usable_as_a_variable():
    module = parse("sust = 5")
    assert isinstance(module.body[0], Assign)
    assert module.body[0].targets[0].id == "sust"


# ── Transformer: version-gated emission ───────────────────────────────────────


def test_tstring_target_python_ast():
    py_ast = to_py('t"hi {x}"')
    value = py_ast.body[0].value
    if PY314:
        assert isinstance(value, ast.TemplateStr)
        assert isinstance(value.values[1], ast.Interpolation)
    else:
        # Graceful degradation: an f-string is semantically equivalent text
        assert isinstance(value, ast.JoinedStr)
        assert isinstance(value.values[1], ast.FormattedValue)
    compile(py_ast, "<test>", "exec")


def test_tstring_runs_and_prints(capsys):
    source = 'naam = "Ravi"\nbolo(roop(t"namaste {naam}!"))'
    assert run(source, capsys) == "namaste Ravi!"


def test_roop_matches_fstring_output(capsys):
    source = (
        "x = 5\n"
        "w = 3\n"
        's = "chaai"\n'
        'bolo(roop(t"{x!r:>8}|{w:0{w}d}|{s!r}"))\n'
        'bolo(f"{x!r:>8}|{w:0{w}d}|{s!r}")\n'
    )
    rendered, expected = run(source, capsys).splitlines()
    assert rendered == expected
    assert "'chaai'" in rendered  # !r conversion really happened


def test_roop_is_a_noop_for_plain_strings():
    interpreter = JugaadInterpreter()
    interpreter.run("s = roop('seedha text')")
    assert interpreter.globals["s"] == "seedha text"


def test_fstring_debug_output_matches_cpython(capsys):
    source = (
        "x = 42\n"
        's = "abc"\n'
        'bolo(f"{x=}")\n'
        'bolo(f"{x = }")\n'
        'bolo(f"{x=:>5}")\n'
        'bolo(f"{s=}")\n'
        'bolo(f"{s=:>8}")\n'
        'bolo(f"{x==42}")\n'
    )
    lines = run(source, capsys).splitlines()
    assert lines == ["x=42", "x = 42", "x=   42", "s='abc'", "s=     abc", "True"]


def test_tstring_debug_output_matches_fstring(capsys):
    source = (
        "x = 42\n"
        'bolo(roop(t"{x=}"))\n'
        'bolo(f"{x=}")\n'
        'bolo(roop(t"{x=:>5}"))\n'
        'bolo(f"{x=:>5}")\n'
    )
    lines = run(source, capsys).splitlines()
    assert lines[0] == lines[1] == "x=42"
    assert lines[2] == lines[3] == "x=   42"


def test_lazy_import_target_python_ast():
    py_ast = to_py("sust lao json")
    import_node = py_ast.body[0]
    if PY315:
        assert import_node.is_lazy == 1
    else:
        assert not hasattr(import_node, "is_lazy")
    compile(py_ast, "<test>", "exec")


def test_unpack_comprehension_target_python_ast():
    py_ast = to_py("bolo([*l ghumo l mein lists])")
    comp = py_ast.body[0].value.args[0]
    if PY315:
        assert isinstance(comp.elt, ast.Starred)
    else:
        # Lowered to `[t for l in lists for t in l]`
        assert isinstance(comp.elt, ast.Name)
        assert comp.elt.id.startswith("_jug_unpack_")
        assert len(comp.generators) == 2
    compile(py_ast, "<test>", "exec")


def test_unpack_dict_comprehension_target_python_ast():
    py_ast = to_py("bolo({**d ghumo d mein dicts})")
    comp = py_ast.body[0].value.args[0]
    if PY315:
        assert comp.value is None
    else:
        assert comp.value is not None  # lowered to `k, v in d.items()`
        assert len(comp.generators) == 2
    compile(py_ast, "<test>", "exec")


def test_unpack_semantics_match_python(capsys):
    source = (
        "lists = [[1, 2], [3]]\n"
        "bolo([*l ghumo l mein lists])\n"
        "bolo({*l ghumo l mein lists})\n"
        "bolo(list((*l ghumo l mein lists)))\n"
        "dicts = [{'a': 1}, {'b': 2}]\n"
        "bolo({**d ghumo d mein dicts})\n"
        "bolo([*l ghumo l mein lists agar l != [3]])\n"
    )
    assert run(source, capsys).splitlines() == [
        "[1, 2, 3]",
        "{1, 2, 3}",
        "[1, 2, 3]",
        "{'a': 1, 'b': 2}",
        "[1, 2]",
    ]


def test_bracketless_except_runs(capsys):
    source = (
        "koshish:\n"
        "    udao ValueError('x')\n"
        "gadbad ValueError, TypeError:\n"
        "    bolo('pakda gaya')\n"
    )
    assert run(source, capsys) == "pakda gaya"


def test_tstring_and_fstring_braces(capsys):
    source = (
        "x = 7\n"
        'bolo(f"{{{x}}}")\n'
        'bolo(f"a }} b {{ c")\n'
        'bolo(roop(t"{{{x}}}"))\n'
        'bolo(f"{ x }")\n'
        'bolo(f"{x:03d}")\n'
    )
    assert run(source, capsys).splitlines() == [
        "{7}",
        "a } b { c",
        "{7}",
        "7",
        "007",
    ]


def test_lazy_import_runs(capsys):
    assert run("sust lao json\nbolo('json ok')", capsys) == "json ok"


def test_lazy_from_import_runs(capsys):
    assert run("sust se json lao dumps\nbolo(dumps({'a': 1}))", capsys) == '{"a": 1}'


# ── Transformer: Python 3.15 builtins ─────────────────────────────────────────


def test_versioned_builtin_alias_gate():
    interpreter = JugaadInterpreter()
    if PY315:
        interpreter.run("k = jamhi_kosh(a=1)\ns = pahredaar")
        assert dict(interpreter.globals["k"]) == {"a": 1}
        assert interpreter.globals["s"] is not None
    else:
        with pytest.raises(JugaadError, match="3.15"):
            JugaadInterpreter().run("bolo(jamhi_kosh(a=1))")
        with pytest.raises(JugaadError, match="3.15"):
            JugaadInterpreter().run("bolo(pahredaar)")


def test_optional_builtins_in_safe_allowlist():
    from jugaadlang.runtime.interpreter import _SAFE_BUILTINS

    assert ("frozendict" in _SAFE_BUILTINS) == PY315
    assert ("sentinel" in _SAFE_BUILTINS) == PY315
    assert ("__lazy_import__" in _SAFE_BUILTINS) == PY315


# ── Cache: versioned keys ─────────────────────────────────────────────────────


def test_cache_key_tracks_bytecode_magic(monkeypatch):
    from jugaadlang.cache import manager as cache_manager_module

    source = "bolo('namaste')"
    default_key = cache_manager_module.CacheManager(cache_dir="__jugcache__")._get_key(source)

    monkeypatch.setattr(cache_manager_module, "MAGIC_NUMBER", b"\x00\x00fake-magic")
    other_key = cache_manager_module.CacheManager(cache_dir="__jugcache__")._get_key(source)

    assert default_key != other_key
    assert len(default_key) == 64


def test_cache_key_is_stable_for_same_source():
    from jugaadlang.cache.manager import CacheManager

    manager = CacheManager(cache_dir="__jugcache__")
    assert manager._get_key("x = 1") == manager._get_key("x = 1")
    assert manager._get_key("x = 1") != manager._get_key("x = 2")
