from nose.tools import assert_raises

from pygeom.core import Point, Line
from pygeom.pairs import LineSegment, Vertex, PointLine
from pygeom.field import FiniteField, Rational
from pygeom.geometry import blue, red, green, Geometry
from pygeom.util import GeometryError, NullLineError
from util import random_point, random_line, random_geometry, random_pointline, generate_fuzz_data

def test_fuzz_parabola():
    N = 50
    for data in generate_fuzz_data(N, pointlines=1):
        try:
            parabola = data.pointlines[0].parabola()
            assert parabola.is_parabola()
        except NullLineError:
            pass

def test_fuzz_grammola():
    N = 20
    for data in generate_fuzz_data(N, vertices=1, spreads=1):
        try:
            K = data.spreads[0]
            diags = data.vertices[0]
            if diags.parallel():
                continue

            grammola = diags.grammola(K)

            d1, d2 = diags.line1, diags.line2
            try:
                point = grammola._point_on()
            except ValueError:
                continue
            except ZeroDivisionError:
                continue
            
            assert PointLine(point, d1).quadrance() + PointLine(point, d2).quadrance() - K == 0
            
            d22, K22 = grammola.co_diagonal(d1)
            d11, K11 = grammola.co_diagonal(d2)
            assert d22 == d2
            assert d11 == d1
            assert K22 == K
            assert K11 == K
            d1.geometry = True
            assert_raises(GeometryError, grammola.co_diagonal, d1)

        except NullLineError:
            pass


def test_fuzz_quadrola():
    N = 20
    for data in generate_fuzz_data(N, line_segments=1, spreads=1):
        try:
            K = data.spreads[0]
            points = data.line_segments[0]

            quadrola = points.quadrola(K)

            try:
                point = quadrola._point_on()
            except ValueError:
                continue
            except ZeroDivisionError:
                continue

            assert quadrola.through(point)
            Q1 = LineSegment(point, points.point1).quadrance()
            Q2 = LineSegment(point, points.point2).quadrance()
            assert (Q1 + Q2 + K)*(Q1 + Q2 + K) - 2*(Q1*Q1 + Q2*Q2 + K*K) == 0

        except NullLineError:
            pass



def test_fuzz_conic():
    N = 50
    for data in generate_fuzz_data(N, pointlines=1, spreads=1):
        try:
            focus_direc = data.pointlines[0]
            K = data.spreads[0]
            conic = focus_direc.conic(K)

            v1, v2, KK = conic.focus_directrix()
            
            dir = focus_direc.line
            focus = focus_direc.point

            assert K == KK
            assert v1 == focus_direc or v2 == focus_direc
            assert Vertex(v1.line, v2.line).parallel()

        except NullLineError:
            pass
        except ZeroDivisionError:
            #FIXME
            pass



def test_fuzz_circle():
    N = 50
    for data in generate_fuzz_data(N, points=1, spreads=1):
        centre = data.points[0]
        K = data.spreads[0]
        
        circle = centre.circle(K)
        assert circle.is_circle()

        new_centre, new_K = circle.centre_quadrance()

        assert new_centre == centre
        assert new_K == K
        
def test_fuzz_pole_polar():
    N = 50
    for data in generate_fuzz_data(N, points=1, conics=1):
        conic = data.conics[0]
        pole = data.points[0]

        try:
            polar = conic.polar(pole)
            assert pole == conic.pole(polar)
        except ZeroDivisionError:
            pass

def test_fuzz_tangent():
    N = 50
    for data in generate_fuzz_data(N, points=1, conics=1):
        conic = data.conics[0]
        point = data.points[0]

        try:
            tangent = conic.tangent(point)
            assert conic.is_tangent(tangent)
        except ValueError:
            assert not conic.through(point)

        try:
            point = conic._point_on()
        except ValueError:
            continue
        except ZeroDivisionError:
            continue

        tangent = conic.tangent(point)
        assert conic.is_tangent(tangent)

