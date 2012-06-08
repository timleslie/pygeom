import nose
from nose.tools import assert_raises

from pygeom.field import Field, FiniteField, Rational
from util import random_finite_fields

def test_base_class():
    """
    Ensure that the base class interface is as expected.
    """
    f = Field
    x = f(0)

    assert_raises(NotImplementedError, x.__add__, 0)
    assert_raises(NotImplementedError, x.__sub__, 0)
    assert_raises(NotImplementedError, x.__mul__, 0)
    assert_raises(NotImplementedError, x.__div__, 0)

    assert_raises(NotImplementedError, x.__radd__, 0)
    assert_raises(NotImplementedError, x.__rsub__, 0)
    assert_raises(NotImplementedError, x.__rmul__, 0)
    assert_raises(NotImplementedError, x.__rdiv__, 0)

    assert_raises(NotImplementedError, x.__neg__)
    assert_raises(NotImplementedError, x.__eq__, 0)

    assert_raises(NotImplementedError, x.is_square)
    assert_raises(NotImplementedError, x.sqrt)
    assert_raises(NotImplementedError, x.reduce, [])
    
    assert_raises(NotImplementedError, f.random)

def test_init():
    f = FiniteField
    f.base = 7
    assert f(-2) == 5
    assert f(-1) == 6
    assert f(0) == 0
    assert f(1) == 1
    assert f(2) == 2
    assert f(3) == 3
    assert f(4) == 4
    assert f(5) == 5
    assert f(6) == 6
    assert f(7) == 0
    assert f(8) == 1

    assert_raises(TypeError, f, None)
    assert_raises(TypeError, f, 1, 1.0)
    assert_raises(ValueError, f, 1, 1)

def test_finite_add():
    f = FiniteField
    f.base = 7
    x = f(0)
    y = f(0)
    assert (x + y) == 0
    assert (x + 0) == 0
    assert (0 + y) == 0
    assert_raises(TypeError, x.__add__, None)

    assert (f(2) + f(3)) == 5
    assert (f(2) + f(5)) == 0
    assert (f(6) + f(2)) == 1

    assert (f(-6) + f(-2)) == 6


def test_finite_sub():
    f = FiniteField
    f.base = 7
    x = f(0)
    y = f(0)
    assert (x - y) == 0
    assert (x - 0) == 0
    assert (0 - y) == 0
    assert_raises(TypeError, x.__sub__, None)

    assert (f(2) - f(3)) == 6
    assert (f(2) - f(5)) == 4
    assert (f(6) - f(2)) == 4

    assert (f(-6) - f(-2)) == 3


def test_finite_neg():
    f = FiniteField
    f.base = 7

    assert (-f(-1)) == 1
    assert (-f(0)) == 0
    assert (-f(1)) == 6
    assert (-f(2)) == 5
    assert (-f(3)) == 4
    assert (-f(4)) == 3
    assert (-f(5)) == 2
    assert (-f(6)) == 1
    assert (-f(7)) == 0


def test_finite_mul():
    f = FiniteField
    f.base = 7
    x = f(0)
    y = f(0)
    assert (x * y) == 0
    assert (x * 0) == 0
    assert (0 * y) == 0
    assert_raises(TypeError, x.__mul__, None)

    assert (f(2) * f(3)) == 6
    assert (f(2) * f(5)) == 3
    assert (f(6) * f(2)) == 5

    assert (f(-6) * f(-2)) == 5

def test_finite_div():
    f = FiniteField
    f.base = 7
    x = f(1)
    y = f(1)
    assert (x / y) == 1
    assert (x / 1) == 1
    assert (0 / y) == 0
    assert_raises(TypeError, x.__div__, None)

    assert (f(2) / f(3)) == 3
    assert (f(2) / f(5)) == 6
    assert (f(6) / f(2)) == 3

    assert (f(-6) / f(-2)) == 3

def test_finite_eq():
    f = FiniteField
    f.base = 7
    x = f(1)
    y = f(5)
    z = f(12)

    # Identity
    assert x == x
    assert y == y
    assert z == z

    # Equaity of field objects mod p
    assert y == z

    # field objects over different p are always different
    f.base = 11
    w = f(5)
    assert w != y

    # Field objects against ints convert the int mod p
    assert x == 1
    assert x == 8
    assert x == -6
    assert x != 2

    # Comparing to strings, floats, etc is always invalid
    assert_raises(TypeError, x.__eq__, 1.0)
    assert_raises(TypeError, x.__eq__, "fail")
    assert_raises(TypeError, x.__eq__, None)

def test_fuzz_axioms():

    for field in list(random_finite_fields(3)) + [Rational]:
        for _ in range(100):
            x, y, z = field.random(), field.random(), field.random()
            zero = field(0)
            one = field(1)

            # 1. Closure under addition
            assert type(x + y) == field
        

            # 2. Associative law of addition
            assert (x + y) + z == x + (y + z)

            # 3. Commutative law of addition
            assert x + y == y + x

            # 4. Existance of a zero
            assert x + zero == zero + x == x

            # 5. Existance of a negative
            w = -x
            assert x + w == 0

            # 6. Closure under multiplication
            assert type(x*y) == field

            # 7. Associative law of multiplication
            assert x*(y*z) == (x*y)*z

            # 8. Commutative law of multiplication
            assert x*y == y*x

            # 9. Existance of a one
            assert x*one == one*x == x
        
            # 10. Existance of an inverse for multiplication
            if x != 0:
                print "X =", x, x == 0, x != 0
                w = one/x
                assert x*w == x*w == one
            else:
                assert_raises(ZeroDivisionError, x.__rdiv__, one)
                assert_raises(ZeroDivisionError, one.__div__, x)

            # 11. Distributive law
            assert x*(y + z) == x*y + x*z

            # 12. Distributive law
            assert (x + y)*z == x*z + y*z

def test_fuzz_sqrt():
    for field in list(random_finite_fields(3)) + [Rational]:
        for _ in range(100):
            x = field.random()
            if x.is_square():
                y = x.sqrt()
                assert y*y == x
            else:
                assert_raises(ValueError, x.sqrt)


def test_fuzz_reduce():
    for field in list(random_finite_fields(3)) + [Rational]:
        for _ in range(100):
            x, y, z = field.random(), field.random(), field.random()
            x1, y1, z1 = x.reduce([y, z])
            assert x*y1 == y*x1
            assert y*z1 == z*y1
            assert z*x1 == x*z1
            
            x1.reduce([])[0] == x1
            y1.reduce([])[0] == y1
            z1.reduce([])[0] == z1
