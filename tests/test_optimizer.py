import pytest
from jugaadlang.ast_nodes.nodes import BinOp, BoolOp, Constant, If, UnaryOp, ExprStmt, Module
from jugaadlang.optimizer.ast_optimizer import JugaadASTOptimizer

def test_constant_folding_binop():
    optimizer = JugaadASTOptimizer()
    
    # 10 * 24
    node = BinOp(left=Constant(value=10), op='*', right=Constant(value=24))
    optimized = optimizer.optimize(node)
    
    assert isinstance(optimized, Constant)
    assert optimized.value == 240

def test_constant_folding_boolop():
    optimizer = JugaadASTOptimizer()
    
    # True aur False
    node = BoolOp(op='aur', values=[Constant(value=True), Constant(value=False)])
    optimized = optimizer.optimize(node)
    
    assert isinstance(optimized, Constant)
    assert optimized.value is False

def test_constant_folding_unaryop():
    optimizer = JugaadASTOptimizer()
    
    # nahi sahi
    node = UnaryOp(op='nahi', operand=Constant(value=True))
    optimized = optimizer.optimize(node)
    
    assert isinstance(optimized, Constant)
    assert optimized.value is False

def test_dead_code_elimination_if_true():
    optimizer = JugaadASTOptimizer()
    
    body_stmt = ExprStmt(value=Constant(value="kept"))
    orelse_stmt = ExprStmt(value=Constant(value="pruned"))
    
    node = If(test=Constant(value=True), body=[body_stmt], orelse=[orelse_stmt])
    optimized = optimizer.optimize(node)
    
    assert isinstance(optimized, list)
    assert len(optimized) == 1
    assert optimized[0] == body_stmt

def test_dead_code_elimination_if_false():
    optimizer = JugaadASTOptimizer()
    
    body_stmt = ExprStmt(value=Constant(value="pruned"))
    orelse_stmt = ExprStmt(value=Constant(value="kept"))
    
    node = If(test=Constant(value=False), body=[body_stmt], orelse=[orelse_stmt])
    optimized = optimizer.optimize(node)
    
    assert isinstance(optimized, list)
    assert len(optimized) == 1
    assert optimized[0] == orelse_stmt
