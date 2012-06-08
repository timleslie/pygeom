from nose.tools import assert_raises

from pygeom.core import Point, Line, Conic
from pygeom.pairs import LineSegment, Vertex, PointLine
from pygeom.field import FiniteField, Rational
from pygeom.geometry import blue, red, green, Geometry
from pygeom.util import GeometryError, NullLineError
from util import random_point, random_line, random_geometry, random_pointline, generate_fuzz_data


def test_init():
    p = Point(0, 0)
    assert p.x == 0
    assert p.y == 0
    assert p.geometry == None

    assert_raises(TypeError, Point, Rational(0), 0)
    
def test_null():
    f = Rational
    blue_ = blue(Rational)
    red_ = red(Rational)
    green_ = green(Rational)

    p0 = Point(f(0), f(0))
    p0b = Point(f(0), f(0), blue_)
    p0r = Point(f(0), f(0), red_)
    p0g = Point(f(0), f(0), green_)

    assert_raises(GeometryError, p0.null)
    assert p0b.null()
    assert p0r.null()
    assert p0g.null()


    p1b = Point(f(1), f(1), blue_)
    p1r = Point(f(1), f(1), red_)
    p1g = Point(f(1), f(1), green_)
    
    assert not p1b.null()
    assert p1r.null()
    assert not p1g.null()

    p1b = Point(f(1), f(0), blue_)
    p1r = Point(f(1), f(0), red_)
    p1g = Point(f(1), f(0), green_)
    
    assert not p1b.null()
    assert not p1r.null()
    assert p1g.null()

    p1b = Point(f(0), f(1), blue_)
    p1r = Point(f(0), f(1), red_)
    p1g = Point(f(0), f(1), green_)
    
    assert not p1b.null()
    assert not p1r.null()
    assert p1g.null()

def test_repr():
    f = Rational
    blue_ = blue(Rational)
    red_ = red(Rational)
    green_ = green(Rational)

    print blue_, red_, green_
    print Point(f(1), f(2), None)
    print Point(f(1), f(2), blue_)
    print Line(f(1), f(2), f(3), None)
    print Line(f(1), f(2), f(3), blue_)
    print Conic(f(1), f(2), f(3), f(4), f(5), f(6), None)
    print Conic(f(1), f(2), f(3), f(4), f(5), f(6), blue_)

def test_eq():
    f = Rational
    blue_ = blue(Rational)
    red_ = red(Rational)
    green_ = green(Rational)

    p0 = Point(f(0), f(0))
    p0b = Point(f(0), f(0), blue_)
    p0r = Point(f(0), f(0), red_)
    p0g = Point(f(0), f(0), green_)

    assert p0 == p0
    assert p0b == p0b
    assert p0r == p0r
    assert p0g == p0g
    
    assert p0 != p0b
    assert p0 != p0r
    assert p0 != p0g
    assert p0b != p0r
    assert p0b != p0g
    assert p0r != p0g

    p1 = Point(f(1), f(0))
    p1b = Point(f(1), f(0), blue_)
    p1r = Point(f(1), f(0), red_)
    p1g = Point(f(1), f(0), green_)

    assert p1b == p1b
    assert p1r == p1r
    assert p1g == p1g

    assert p0 != p1
    assert p0r != p1r
    assert p0g != p1g
    assert p0b != p1b

def test_mul():
    for data in generate_fuzz_data(20, points=1, spreads=1):
        point = data.points[0]
        x = data.spreads[0]
        assert point*x == x*point

def test_div():
    for data in generate_fuzz_data(20, points=1, spreads=1):
        point = data.points[0]
        x = data.spreads[0]
        if x == 0:
            assert_raises(ZeroDivisionError, point.__div__, x)
        else:
            assert x*(point/x) == point

def test_add():
    for data in generate_fuzz_data(20, points=2):
        point1, point2 = data.points
        assert point1 + point2 == point2 + point1


def test_sub():
    for data in generate_fuzz_data(20, points=2):
        point1, point2 = data.points
        p1 = point1 - point1
        p2 = point2 - point2
        p3 = (point1 - point2) + (point2 - point1)

        assert p1.x == p1.y == 0
        assert p2.x == p2.y == 0
        assert p3.x == p3.y == 0

def test_eval():
    for data in generate_fuzz_data(20, points=2, lines=1):
        point1, point2 = data.points
        line = data.lines[0]
        
        x1, y1 = point1.form()
        x2, y2 = point2.form()
        a, b, c = line.form()

        assert point1.eval(x1, y1) == 0
        assert point2.eval(x2, y2) == 0
        if point1 != point2:
            assert point1.eval(x2, y2) == 1
            assert point2.eval(x1, y1) == 1
        else:
            assert point1.eval(x2, y2) == 0
            assert point2.eval(x1, y1) == 0

        assert line.eval(x1, y1) == a*x1 + b*y1 + c
        assert line.eval(x2, y2) == a*x2 + b*y2 + c
