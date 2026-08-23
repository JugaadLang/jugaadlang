from jugaadlang.cache.manager import CacheManager

def test_cache_l1_set_get():
    manager = CacheManager(cache_dir=".test_cache_1")
    manager.clear()
    
    manager.set("print('hello')", "print('hello')")
    assert manager.get("print('hello')") == "print('hello')"
    assert manager.get("print('world')") is None

def test_cache_l2_persistence():
    manager = CacheManager(cache_dir=".test_cache_2")
    manager.clear()
    
    manager.set("x = 1", "x = 1\n")
    
    # Create a new manager with the same directory to simulate restarting the app
    new_manager = CacheManager(cache_dir=".test_cache_2")
    assert new_manager.get("x = 1") == "x = 1\n"
    
def test_cache_clear():
    manager = CacheManager(cache_dir=".test_cache_3")
    manager.clear()
    
    manager.set("bolo('hi')", "print('hi')")
    assert manager.get("bolo('hi')") == "print('hi')"
    
    manager.clear()
    assert manager.get("bolo('hi')") is None
    
    new_manager = CacheManager(cache_dir=".test_cache_3")
    assert new_manager.get("bolo('hi')") is None
