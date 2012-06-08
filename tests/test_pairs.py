from nose.tools import assert_raises

from pygeom.core import Point, Line
from pygeom.pairs import LineSegment, Vertex, PointLine
from pygeom.field import FiniteField, Rational
from pygeom.geometry import blue, red, green, Geometry
from pygeom.util import GeometryError, NullLineError
from util import random_point, random_line, random_geometry, random_pointline, generate_fuzz_data

def test_fuzz_init():
    N = 20
    for data in generate_fuzz_data(N, geoms=2, lines=2, points=2):
        g0, g1 = data.geoms
        l0, l1 = data.lines
        p0, p1 = data.points

        ls0 = LineSegment(p0, p1)
        ls1 = LineSegment(p0, p1)
        assert ls0 == ls1

        v0 = Vertex(l0, l1)
        v1 = Vertex(l1, l0)
        assert v0 == v1

        if g0 != g1:
            l0.geometry = p0.geometry = g0
            l1.geometry = p1.geometry = g1
            assert_raises(GeometryError, Vertex, l0, l1)
            assert_raises(GeometryError, PointLine, p0, l1)
            assert_raises(GeometryError, LineSegment, p0, p1)


def test_fuzz_altitude():
    N = 20
    for data in generate_fuzz_data(N, pointlines=1):
        pl = data.pointlines[0]

        if pl.line.null():
            assert_raises(NullLineError, pl.altitude)
        else:
            alt = pl.altitude()
            assert PointLine(pl.point, alt.line).on()
            assert Vertex(alt.line, pl.line).perpendicular()
            assert PointLine(alt.point, pl.line).on()

def test_fuzz_reflection():
    N = 20
    for data in generate_fuzz_data(N, pointlines=1):
        pl = data.pointlines[0]

        if pl.line.null():
            assert_raises(NullLineError, pl.reflection)
        else:
            ref = pl.reflection()
            assert pl == ref.reflection()
            assert pl.altitude().point == ref.altitude().point
            assert pl.line == ref.line
            assert ref.quadrance() == pl.quadrance()


def test_construct_spread():
    f = FiniteField
    f.base = 7
    geom = blue(f)
    line = Line(f(0), f(1), f(0), geom)
    point = Point(f(1), f(2), geom)

    pl = PointLine(point, line)
    v = pl.construct_spread(f(1)/f(5))

    N = 20
    for data in generate_fuzz_data(N, pointlines=1, spreads=1):
        pl = data.pointlines[0]
        s = data.spreads[0]
        if pl.line.null():
            assert_raises(NullLineError, pl.construct_spread, s)
        else:
            try:
                v = pl.construct_spread(s)
            except ValueError:
                pass
        

def test_parallel():
    N = 20
    for data in generate_fuzz_data(N, lines=1):
        line = data.lines[0]
        if line.null():
            assert_raises(NullLineError, Vertex(line, line).spread)
        else:
            assert Vertex(line, line).spread() == 0
        assert Vertex(line, line).parallel()

def test_construct_quadrance():
    f = FiniteField
    f.base = 37
    geom = blue(f)
    line = Line(f(1), f(1), f(10), geom)
    point = Point(f(0), f(1), geom)

    pl = PointLine(point, line)
    X = pl.construct_quadrance(f(10))

    v = pl.construct_spread(f(1)/f(5))

    N = 20
    for data in generate_fuzz_data(N, pointlines=1, spreads=1):
        pl = data.pointlines[0]
        s = data.spreads[0]
        try:
            ls = pl.construct_quadrance(s)
        except ValueError:
            pass


def test_fuzz_bisect():
    N = 50

    for data in generate_fuzz_data(N, lines=2):
        l1, l2 = data.lines
        if l1.null() or l2.null() or Vertex(l1, l2).parallel() or Vertex(l1, l2).point.null():
            continue

        V = l1.vector()
        U = l2.vector()
        try:
            (U.norm()/V.norm()).sqrt()
        except ValueError:
            continue

        v0 = Vertex(l1, l2)
        bisectors = v0.bisect()
        s0 = v0.spread()

        s1 = Vertex(l1, bisectors.line1).spread()
        s2 = Vertex(l1, bisectors.line2).spread()
        s3 = Vertex(l2, bisectors.line1).spread()
        s4 = Vertex(l2, bisectors.line2).spread()
                
        assert bisectors.spread() == 1

def test_quadrance():
    f = FiniteField
    f.base = 11

    p0 = Point(f(0), f(0))
    p0b = Point(f(0), f(0), blue(f))
    p0r = Point(f(0), f(0), red(f))
    p0g = Point(f(0), f(0), green(f))
    
    # FIXME: These should move to a LineSegment constructor test
    # FIXME: This test should move into some kind of test_line_segment
    assert_raises(GeometryError, LineSegment, p0, p0b)
    assert_raises(GeometryError, LineSegment, p0, p0r)
    assert_raises(GeometryError, LineSegment, p0, p0g)

    assert_raises(GeometryError, LineSegment, p0r, p0)
    assert_raises(GeometryError, LineSegment, p0r, p0b)
    assert_raises(GeometryError, LineSegment, p0r, p0g)

    assert_raises(GeometryError, LineSegment, p0b, p0)
    assert_raises(GeometryError, LineSegment, p0b, p0r)
    assert_raises(GeometryError, LineSegment, p0b, p0g)

    assert_raises(GeometryError, LineSegment, p0g, p0)
    assert_raises(GeometryError, LineSegment, p0g, p0r)
    assert_raises(GeometryError, LineSegment, p0g, p0b)

    p1 = Point(f(1), f(1))
    p1b = Point(f(1), f(1), blue(f))
    p1r = Point(f(1), f(1), red(f))
    p1g = Point(f(1), f(1), green(f))

    assert LineSegment(p1b, p0b).quadrance() == LineSegment(p0b, p1b).quadrance() == 2
    assert LineSegment(p1r, p0r).quadrance() == LineSegment(p0r, p1r).quadrance() == 0
    assert LineSegment(p1g, p0g).quadrance() == LineSegment(p0g, p1g).quadrance() == 2

    p1 = Point(f(0), f(1))
    p1b = Point(f(0), f(1), blue(f))
    p1r = Point(f(0), f(1), red(f))
    p1g = Point(f(0), f(1), green(f))

    assert LineSegment(p1b, p0b).quadrance() == LineSegment(p0b, p1b).quadrance() == 1
    assert LineSegment(p1r, p0r).quadrance() == LineSegment(p0r, p1r).quadrance() == -1
    assert LineSegment(p1g, p0g).quadrance() == LineSegment(p0g, p1g).quadrance() == 0


def test_midpoint():
    f = FiniteField
    f.base = 11
    X0 = Point(f(0), f(0), blue(f))
    X1 = Point(f(2), f(2), blue(f))
    X2 = Point(f(10), f(0), blue(f))

    for (x0, x1) in [(X0, X1), (X1, X0),
                     (X0, X2), (X2, X0),
                     (X1, X2), (X2, X1)]:
        m = LineSegment(x0, x1).midpoint()
        assert LineSegment(x0, m).quadrance() == LineSegment(x1, m).quadrance()
        m = LineSegment(x1, x0).midpoint()
        assert LineSegment(x0, m).quadrance() == LineSegment(x1, m).quadrance()


    X0 = Point(Rational(1), Rational(7), red(Rational))
    X1 = Point(Rational(3), Rational(2), red(Rational))
    X2 = Point(Rational(10), Rational(1), red(Rational))

    for (x0, x1) in [(X0, X1), (X1, X0),
                     (X0, X2), (X2, X0),
                     (X1, X2), (X2, X1)]:
        m = LineSegment(x0, x1).midpoint()
        assert LineSegment(x0, m).quadrance() == LineSegment(x1, m).quadrance()
        m = LineSegment(x1, x0).midpoint()
        assert LineSegment(x0, m).quadrance() == LineSegment(x1, m).quadrance()

    X0 = Point(Rational(3), Rational(0), green(Rational))
    X1 = Point(Rational(2), Rational(5), green(Rational))
    X2 = Point(Rational(10), Rational(1), green(Rational))

    for (x0, x1) in [(X0, X1), (X1, X0),
                     (X0, X2), (X2, X0),
                     (X1, X2), (X2, X1)]:
        m = LineSegment(x0, x1).midpoint()
        assert LineSegment(x0, m).quadrance() == LineSegment(x1, m).quadrance()
        m = LineSegment(x1, x0).midpoint()
        assert LineSegment(x0, m).quadrance() == LineSegment(x1, m).quadrance()

        
def test_fuzz_midpoint():
    N = 20
    for data in generate_fuzz_data(N, points=2):
        X0, X1 = data.points
        l0 = LineSegment(X0, X1)
        l1 = LineSegment(X1, X0)
        if l0.line.null():
            assert l1.line.null()
            assert_raises(ValueError, l0.midpoint)
            assert_raises(ValueError, l1.midpoint)
            continue

        M0 = l0.midpoint()
        M1 = l1.midpoint()
        quadrance = LineSegment(X0, M0).quadrance()
        
        assert LineSegment(X0, M0).quadrance() == quadrance

        assert LineSegment(X1, M0).quadrance() == quadrance
        assert LineSegment(X0, M1).quadrance() == quadrance
        assert LineSegment(X1, M1).quadrance() == quadrance

