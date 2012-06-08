from pygeom.util import shanks_tonelli, M, all_equal

def test_shanks():
    p = 37
    for i in range(1, p):
        n = i*i % p
        st = shanks_tonelli(n, p)
        assert st*st % p == n

def test_M():
    a, b, c = M(10, 37)
    assert a == 100
    assert b == 370
    assert c == 37*37

def test_all_equal():
    assert all_equal([])
    assert all_equal([1])
    assert all_equal([1, 1, 1])
    assert not all_equal([2, 1, 1, 1])
    assert not all_equal([1, 2])
