from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,
        bottom_up_once, basic_fns)
from sympy.strategies.util import expr_fns
from sympy import Basic, symbols, Symbol, S

zero_symbols = lambda x: S.Zero if isinstance(x, Symbol) else x
x,y,z = symbols('x,y,z')

def test_sall():
    zero_onelevel = sall(zero_symbols)

    assert zero_onelevel(Basic(x, y, Basic(x, z))) == \
                         Basic(0, 0, Basic(x, z))

def test_bottom_up():
    _test_global_traversal(bottom_up)
    _test_stop_on_non_basics(bottom_up)

def test_top_down():
    _test_global_traversal(top_down)
    _test_stop_on_non_basics(top_down)

def _test_global_traversal(trav):
    x,y,z = symbols('x,y,z')
    zero_all_symbols = trav(zero_symbols)

    assert zero_all_symbols(Basic(x, y, Basic(x, z))) == \
                            Basic(0, 0, Basic(0, 0))

def _test_stop_on_non_basics(trav):
    def add_one_if_can(expr):
        try:    return expr + 1
        except: return expr

    expr     = Basic(1, 'a', Basic(2, 'b'))
    expected = Basic(2, 'a', Basic(3, 'b'))
    rl = trav(add_one_if_can)

    assert rl(expr) == expected

class Basic2(Basic):
    pass
rl = lambda x: Basic2(*x.args) if isinstance(x, Basic) else x

def test_top_down_once():
    top_rl = top_down_once(rl)

    assert top_rl(Basic(1, 2, Basic(3, 4))) == \
                  Basic2(1, 2, Basic(3, 4))

def test_bottom_up_once():
    bottom_rl = bottom_up_once(rl)

    assert bottom_rl(Basic(1, 2, Basic(3, 4))) == \
                     Basic(1, 2, Basic2(3, 4))

def test_expr_fns():
    from sympy.strategies.rl import rebuild
    from sympy import Add
    x, y = map(Symbol, 'xy')
    expr = x + y**3
    e = bottom_up(lambda x: x + 1, expr_fns)(expr)
    b = bottom_up(lambda x: Basic.__new__(Add, x, 1), basic_fns)(expr)

    assert rebuild(b) == e
