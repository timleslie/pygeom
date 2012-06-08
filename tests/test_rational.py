from nose.tools import assert_raises

from pygeom.field import Rational
from pygeom.core import Point

def test_init_from_int():
    r1 = Rational(1)
    assert r1.num == 1
    assert r1.den == 1

    r1 = Rational(10)
    assert r1.num == 10
    assert r1.den == 1

    r1 = Rational(-1)
    assert r1.num == -1
    assert r1.den == 1

    r1 = Rational(0)
    assert r1.num == 0
    assert r1.den == 1

def test_init_from_pair():
    r1 = Rational(1, 1)
    assert r1.num == 1
    assert r1.den == 1

    r1 = Rational(10, 1)
    assert r1.num == 10
    assert r1.den == 1

    r1 = Rational(-1, 1)
    assert r1.num == -1
    assert r1.den == 1

    r1 = Rational(0, 1)
    assert r1.num == 0
    assert r1.den == 1

    r1 = Rational(-1, -1)
    assert r1.num == 1
    assert r1.den == 1

    r1 = Rational(-10, -2)
    assert r1.num == 5
    assert r1.den == 1

    r1 = Rational(10, -3)
    assert r1.num == -10
    assert r1.den == 3

def test_init_fails():
    
    assert_raises(ValueError, Rational, 1, 0)
    assert_raises(TypeError, Rational, "fail", 1)
    assert_raises(TypeError, Rational, 1, "fail")
    assert_raises(TypeError, Rational, None, 1)
    assert_raises(TypeError, Rational, 1, None)

def test_add():
    r1 = Rational(5)
    r2 = Rational(10)

    assert r1 + r2 == Rational(15)
    assert r1 + r2 == 15

    assert 5 + r2 == Rational(15)
    assert 5 + r2 == 15

    assert r1 + 10 == Rational(15)
    assert r1 + 10 == 15

    r1 = Rational(3, 2)
    r2 = Rational(5, 3)

    assert r1 + r2 == Rational(19, 6)
    assert r2 + r1 == Rational(19, 6)

    assert r1 + r1 == 3
    assert r1 + r1 == Rational(3)
    assert r1 + r1 == Rational(6, 2)

    assert r2 + r2 + r2 == 5
    assert r2 + r2 + r2 == Rational(5)
    assert r2 + r2 + r2 == Rational(15, 3)

    assert_raises(TypeError, r1.__add__, None)
    assert_raises(TypeError, r1.__add__, 5.5)

    assert_raises(TypeError, r1.__radd__, None)
    assert_raises(TypeError, r1.__radd__, 5.5)


def test_sub():
    r1 = Rational(5)
    r2 = Rational(10)

    assert r1 - r2 == Rational(-5)
    assert r1 - r2 == -5

    assert 5 - r2 == Rational(-5)
    assert 5 - r2 == -5

    assert r1 - 10 == Rational(-5)
    assert r1 - 10 == -5

    r1 = Rational(3, 2)
    r2 = Rational(5, 3)

    assert r1 - r2 == Rational(-1, 6)
    assert r2 - r1 == Rational(1, 6)

    assert r1 - r1 == 0
    assert r1 - r1 == Rational(0)
    assert r1 - r1 == Rational(0, 1)

    assert r2 - r2 - r2 == -r2
    assert r2 - r2 - r2 == Rational(-5, 3)
    assert r2 - r2 - r2 == Rational(-15, 9)

    assert_raises(TypeError, r1.__sub__, None)
    assert_raises(TypeError, r1.__sub__, 5.5)

    assert_raises(TypeError, r1.__rsub__, None)
    assert_raises(TypeError, r1.__rsub__, 5.5)


def test_mul():
    r1 = Rational(5)
    r2 = Rational(10)

    assert r1 * r2 == Rational(50)
    assert r1 * r2 == 50

    assert 5 * r2 == Rational(50)
    assert 5 * r2 == 50

    assert r1 * 10 == Rational(50)
    assert r1 * 10 == 50

    r1 = Rational(3, 2)
    r2 = Rational(5, 3)

    assert r1 * r2 == Rational(5, 2)
    assert r2 * r1 == Rational(5, 2)

    assert r1 * r1 == Rational(9, 4)
    assert r2 * r2 * r2 == Rational(125, 27)

    assert_raises(TypeError, r1.__mul__, None)
    assert_raises(TypeError, r1.__mul__, 5.5)

    assert_raises(TypeError, r1.__rmul__, None)
    assert_raises(TypeError, r1.__rmul__, 5.5)

    p = Point(r1, r2)
    p2 = p * r1
    p3 = r1 * p

def test_div():
    r2 = Rational(10)
    r1 = Rational(5)

    assert r1 / r2 == Rational(1, 2)

    assert 10 / r2 == Rational(1)
    assert 10 / r2 == 1

    assert r1 / 5 == Rational(1)
    assert r1 / 5 == 1

    r1 = Rational(3, 2)
    r2 = Rational(5, 3)

    assert r1 / r2 == Rational(9, 10)
    assert r2 / r1 == Rational(10, 9)
    assert 1 / r1 == Rational(2, 3)

    assert r1 / r1 == Rational(1)
    assert r2 / r2 / r2 == Rational(3, 5)

    assert_raises(TypeError, r1.__div__, None)
    assert_raises(TypeError, r1.__div__, 5.5)

    assert_raises(TypeError, r1.__rdiv__, None)
    assert_raises(TypeError, r1.__rdiv__, 5.5)

def test_eq():
    r1 = Rational(5, 3)
    assert r1 == r1
    assert_raises(TypeError, r1.__eq__, 5.0)
    assert_raises(TypeError, r1.__eq__, "fail")
    assert_raises(TypeError, r1.__eq__, None)
