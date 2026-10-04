import marshal
from types import CodeType
from jugaadlang.cache.manager import CacheManager


def test_cache_l1_set_get():
    manager = CacheManager(cache_dir=".test_cache_1")
    manager.clear()
    
    code_obj = compile("print('hello')", "<string>", "exec")
    manager.set("print('hello')", code_obj)
    
    cached = manager.get("print('hello')")
    assert isinstance(cached, CodeType)
    assert cached.co_code == code_obj.co_code
    assert manager.get("print('world')") is None


def test_cache_l2_persistence():
    manager = CacheManager(cache_dir=".test_cache_2")
    manager.clear()
    
    code_obj = compile("x = 1\n", "<string>", "exec")
    manager.set("x = 1", code_obj)
    
    # Create a new manager with the same directory to simulate restarting the app
    new_manager = CacheManager(cache_dir=".test_cache_2")
    cached = new_manager.get("x = 1")
    assert isinstance(cached, CodeType)
    assert cached.co_code == code_obj.co_code
    
def test_cache_clear():
    manager = CacheManager(cache_dir=".test_cache_3")
    manager.clear()
    
    code_obj = compile("print('hi')", "<string>", "exec")
    manager.set("bolo('hi')", code_obj)
    
    cached = manager.get("bolo('hi')")
    assert isinstance(cached, CodeType)
    
    manager.clear()
    assert manager.get("bolo('hi')") is None

    new_manager = CacheManager(cache_dir=".test_cache_3")
    assert new_manager.get("bolo('hi')") is None


def test_cache_module_reexport():
    """Verify dedicated jugaadlang/cache_manager.py module exports identical interfaces."""
    assert CacheManagerFromModule is CacheManager


def test_cache_creation_after_successful_parsing(tmp_path):
    """Requirement 1: Cache file is created on disk after successful parsing/execution."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source = "bolo('Jai Hind')"
    tokens = Lexer(source, "test.jug").tokenize()
    ast_mod = Parser(tokens, "test.jug", source).parse()

    manager.set_ast(source, ast_mod, filename="test.jug")

    key = manager._get_key(source)
    cache_file = os.path.join(cache_dir, f"{key}.jugc")
    assert os.path.exists(cache_file), "Cache file (.jugc) must exist after set_ast"

    with open(cache_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["cache_version"] == CACHE_VERSION
    assert data["source_hash"] == key
    assert data["ast"]["_type"] == "Module"
    assert data["filename"] == "test.jug"


def test_second_execution_uses_cache(tmp_path):
    """Requirement 2: Second execution uses the cache and bypasses lexing/parsing."""
    cache_dir = str(tmp_path / "__jugcache__")
    custom_manager = CacheManager(cache_dir=cache_dir)

    source = "x = 42\ny = x * 2"
    file_path = str(tmp_path / "calc.jug")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(source)

    with patch("jugaadlang.runtime.interpreter.cache_manager", custom_manager):
        # First execution (Cold start: cache miss)
        interp1 = JugaadInterpreter(filename=file_path)
        interp1.run(source)
        assert interp1.globals["y"] == 84
        assert custom_manager.misses == 1
        assert custom_manager.hits == 0

        # Second execution: Lexer and Parser should be completely bypassed!
        with patch.object(Lexer, "tokenize", side_effect=AssertionError("Lexer should not run on cache hit!")):
            with patch.object(Parser, "parse", side_effect=AssertionError("Parser should not run on cache hit!")):
                interp2 = JugaadInterpreter(filename=file_path)
                interp2.run(source)
                assert interp2.globals["y"] == 84
                assert custom_manager.hits >= 1


def test_unchanged_source_results_in_cache_hit(tmp_path):
    """Requirement 3: Unchanged source results in a deterministic cache hit."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source = "bolo('namaste')"
    tokens = Lexer(source, "code.jug").tokenize()
    ast_mod = Parser(tokens, "code.jug", source).parse()

    manager.set_ast(source, ast_mod, filename="code.jug")

    # Load from cache
    cached_ast = manager.get_ast(source, filename="code.jug")
    assert cached_ast is not None
    assert cached_ast == ast_mod
    assert manager.hits == 1
    assert manager.misses == 0


def test_modifying_source_invalidates_cache(tmp_path):
    """Requirement 4: Modifying source content produces a new hash and invalidates cache."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source_v1 = "bolo('version 1')"
    source_v2 = "bolo('version 2')"

    tokens1 = Lexer(source_v1, "v.jug").tokenize()
    ast1 = Parser(tokens1, "v.jug", source_v1).parse()
    manager.set_ast(source_v1, ast1, filename="v.jug")

    # Source v1 is cached
    assert manager.get_ast(source_v1, filename="v.jug") is not None

    # Source v2 is modified, must result in a cache miss
    assert manager.get_ast(source_v2, filename="v.jug") is None

    # Cache source v2
    tokens2 = Lexer(source_v2, "v.jug").tokenize()
    ast2 = Parser(tokens2, "v.jug", source_v2).parse()
    manager.set_ast(source_v2, ast2, filename="v.jug")

    # Both hashes now exist independently in cache
    assert manager.get_ast(source_v1, filename="v.jug") == ast1
    assert manager.get_ast(source_v2, filename="v.jug") == ast2


def test_missing_cache_falls_back_to_normal_parsing(tmp_path):
    """Requirement 5: Missing cache gracefully falls back to cold-start parsing."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source = "result = 100 + 200"
    # Never stored in cache
    assert manager.get_ast(source) is None

    # End-to-end execution still succeeds smoothly
    with patch("jugaadlang.runtime.interpreter.cache_manager", manager):
        interp = JugaadInterpreter(filename="fallback.jug")
        interp.run(source)
        assert interp.globals["result"] == 300


def test_corrupted_cache_falls_back_safely(tmp_path):
    """Requirement 6: Corrupted cache JSON / bytes falls back safely to cold-start parsing."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source = "status = 'all good'"
    key = manager._get_key(source)
    cache_path = os.path.join(cache_dir, f"{key}.jugc")

    # Write corrupt data
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write("{this is not valid json! corrupted bytes %$^&*")

    # manager.get_ast must catch error and return None
    assert manager.get_ast(source) is None

    # Interpreter execution must not crash, and should overwrite corrupt cache with valid one
    with patch("jugaadlang.runtime.interpreter.cache_manager", manager):
        interp = JugaadInterpreter(filename="corrupt.jug")
        interp.run(source)
        assert interp.globals["status"] == "all good"

    # Verify cache was repaired with valid content
    repaired_ast = manager.get_ast(source)
    assert repaired_ast is not None


def test_incompatible_cache_version_falls_back_safely(tmp_path):
    """Requirement 7: Incompatible cache version is safely rejected and falls back."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source = "val = 99"
    key = manager._get_key(source)
    cache_path = os.path.join(cache_dir, f"{key}.jugc")

    payload = {
        "cache_version": 9999,  # Incompatible future version
        "jugaadlang_version": "99.0.0",
        "source_hash": key,
        "filename": "test.jug",
        "ast": {"_type": "Module", "line": 1, "col": 1, "body": []},
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)

    assert manager.get_ast(source) is None

    # End-to-end interpreter executes safely and updates version
    with patch("jugaadlang.runtime.interpreter.cache_manager", manager):
        interp = JugaadInterpreter(filename="ver.jug")
        interp.run(source)
        assert interp.globals["val"] == 99


def test_source_hash_mismatch_falls_back_safely(tmp_path):
    """Verification that tampered source hash fails validation and falls back."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source = "bolo('real')"
    key = manager._get_key(source)
    cache_path = os.path.join(cache_dir, f"{key}.jugc")

    payload = {
        "cache_version": CACHE_VERSION,
        "jugaadlang_version": "1.1.6",
        "source_hash": "tampered_hash_value_12345",
        "filename": "tamper.jug",
        "ast": {"_type": "Module", "line": 1, "col": 1, "body": []},
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)

    assert manager.get_ast(source) is None


def test_cache_serialization_deserialization_roundtrip():
    """Requirement 8: AST serialization and deserialization works correctly for language constructs."""
    constructs = [
        # Basic print and assignment
        'bolo("Namaste Duniya!")\nx = 10\ny = 20',
        # Conditionals
        'agar x > 5:\n    bolo("bada")\nshayad x == 5:\n    bolo("barabar")\nwarna:\n    bolo("chota")',
        # Loops
        'ghumo i mein [1, 2, 3]:\n    bolo(i)\njabtak x < 10:\n    x += 1',
        # Functions and lambdas
        'banao add(a: int, b: int = 0) -> int:\n    wapas a + b\nf = chota_funkshan x: x * 2',
        # Classes
        'ustad Animal:\n    banao shuru(khud, name):\n        khud.name = name\n    banao speak(khud):\n        wapas "voice"',
        # Exception handling
        'koshish:\n    1 / 0\ngadbad ZeroDivisionError jaise e:\n    bolo(e)\naakhir_me:\n    bolo("khatam")',
        # Comprehensions and f-strings
        'squares = [x**2 ghumo x mein ginti([1, 2, 3])]\nname = poochho\nbolo(f"Namaste {name}")',
        # Pattern matching
        'agar_match x:\n    kaand 1:\n        bolo("ek")\n    kaand _:\n        bolo("anya")',
        # Ellipsis and pass
        'theek_hai\n...',
    ]

    for code in constructs:
        tokens = Lexer(code, "test.jug").tokenize()
        original_ast = Parser(tokens, "test.jug", code).parse()

        # Serialize to dict and JSON
        serialized = serialize_ast(original_ast)
        json_repr = json.dumps(serialized)

        # Deserialize back to AST
        reconstructed = deserialize_ast(json.loads(json_repr))
        assert original_ast == reconstructed, f"Roundtrip failed for:\n{code}"


def test_cache_failures_do_not_prevent_normal_execution(tmp_path):
    """Requirement 9: Filesystem errors (e.g. read-only disk/permission denied) do not break execution."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source = "answer = 42"

    # Simulate filesystem write permission error during cache write
    with patch("os.replace", side_effect=PermissionError("Permission denied: read-only filesystem")):
        with patch("jugaadlang.runtime.interpreter.cache_manager", manager):
            interp = JugaadInterpreter(filename="readonly.jug")
            # Should not raise! Must execute completely and successfully
            interp.run(source)
            assert interp.globals["answer"] == 42


def test_existing_jugaadlang_behavior_unchanged():
    """Requirement 10: Existing JugaadLang behavior, builtins, and semantics remain unchanged."""
    interp = JugaadInterpreter(filename="test.jug")
    code = (
        "a = 15\n"
        "b = 25\n"
        "sum_result = a + b\n"
        "diff_result = b - a\n"
        "is_greater = b > a\n"
    )
    interp.run(code)
    assert interp.globals["sum_result"] == 40
    assert interp.globals["diff_result"] == 10
    assert interp.globals["is_greater"] is True


def test_performance_cold_vs_cached_demonstration(tmp_path):
    """Demonstrate performance advantage: cached execution skips lexing and parsing."""
    cache_dir = str(tmp_path / "__jugcache__")
    manager = CacheManager(cache_dir=cache_dir)

    source = "\n".join([f"var_{i} = {i} * 2 + {i}" for i in range(200)])

    # Store in cache
    tokens = Lexer(source, "bench.jug").tokenize()
    ast_orig = Parser(tokens, "bench.jug", source).parse()
    manager.set_ast(source, ast_orig, filename="bench.jug")

    # Measure 10 cold parses
    t0 = time.perf_counter()
    for _ in range(10):
        toks = Lexer(source, "bench.jug").tokenize()
        Parser(toks, "bench.jug", source).parse()
    cold_total = time.perf_counter() - t0

    # Measure 10 cached loads (bypassing lexer and parser)
    t0 = time.perf_counter()
    for _ in range(10):
        ast_cached = manager.get_ast(source, filename="bench.jug")
    cached_total = time.perf_counter() - t0

    assert ast_orig == ast_cached
    assert manager.hits == 10
    # Cached loading must be reliably faster or at least demonstrate skipping of parsing
    assert cached_total <= cold_total
