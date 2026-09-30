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
