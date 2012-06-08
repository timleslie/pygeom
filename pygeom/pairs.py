"""
This module contains classes which represent pairs of core objects.
Using pairs of core objects we can then construct further objects.
"""

from pygeom.core import Point, Line, Conic
from pygeom.util import check_geometry, NullLineError, GeometryError, M

class LineSegment(object):
    """
    A linesegment represents a pair of points.
    """

    def __init__(self, point1, point2):
        """
        Create a new line segment from two points.

        Both points must be of the same geometry or else a GeometryError will
        be raised.
        """
        self.point1 = point1
        self.point2 = point2
        if point1.geometry != point2.geometry:
            raise GeometryError
        self.geometry = point1.geometry

        x1, y1 = point1.form()
        x2, y2 = point2.form()
        self.line = Line(y1 - y2, x2 - x1, x1*y2 - x2*y1, self.geometry)

    def __eq__(self, other):
        return (self.point1 in [other.point1, other.point2] and
                self.point2 in [other.point1, other.point2] and
                self.geometry == other.geometry)

    @check_geometry
    def midpoint(self):
        """
        Return the midpoint M of the two points of the line segments so
        that Q(M, point1) == Q(M, point2).
        """
        line0 = self.perp_bisector()

        # Find where the equidistant line intersects our line
        return Vertex(self.line, line0).point

    @check_geometry
    def perp_bisector(self):
        """
        Return the perpindicular bisector of the two points.
        """
        x1, y1 = self.point1.form()
        x2, y2 = self.point2.form()
        a, b, c = self.geometry.form

        # Calculate the line of equidistant points
        a0 = 2*(a*(x1 - x2) + b*(y1 - y2))
        b0 = 2*(b*(x1 - x2) + c*(y1 - y2))
        c0 = -(a*(x1*x1 - x2*x2) + 2*b*(x1*y1 - x2*y2) + c*(y1*y1 - y2*y2))

        line0 = Line(a0, b0, c0, self.geometry)

        if self.line.null():
            raise ValueError, \
                "The line between %s and %s is null," \
                "so the midpoint is not defined" % \
                (str(self.point1), str(self.point2))
        return line0

    @check_geometry
    def quadrance(self):
        """
        Calculate the quadrance between the two points of the line segment.
        """
        return (self.point1 - self.point2).norm()

    @check_geometry
    def quadrola(self, K):
        x1, y1 = self.point1.form()
        x2, y2 = self.point2.form()
        a, b, c = self.geometry.form

        X02 = self.point1.norm()
        X12 = self.point2.norm()

        aa, bb, cc = M(a*(x2 - x1) + b*(y2 - y1), b*(x2 - x1) + c*(y2 - y1))

        return Conic(4*(aa - K*a), 4*2*(bb - K*b), 4*(cc - K*c),
                     4*(X02 - X12)*(a*(x2 - x1) + b*(y2 - y1)) + \
                         4*K*(a*(x1 + x2) + b*(y1 + y2)),
                     4*(X02 - X12)*(b*(x2 - x1) + c*(y2 - y1)) + \
                         4*K*(b*(x1 + x2) + c*(y1 + y2)),
                     (K - X02 - X12)*(K - X02 - X12) - 4*X02*X12,
                     self.geometry)


class Vertex(object):
    """
    A Vertex represents a pair of lines and their point of intersection.
    """

    def __init__(self, line1, line2):
        """
        Create a new vertex from two lines.

        Both lines must be of the same geometry or else a GeometryError will
        be raised.
        """
        self.line1 = line1
        self.line2 = line2
        if line1.geometry != line2.geometry:
            raise GeometryError
        self.geometry = line1.geometry

        a1, b1, c1 = line1.form()
        a2, b2, c2 = line2.form()
        den = a1*b2 - a2*b1
        if den == 0:
            self.point = None
        else:
            self.point = Point((b1*c2 - b2*c1)/den, (c1*a2 - c2*a1)/den,
                               self.geometry)

    def __eq__(self, other):
        return (self.line1 in [other.line1, other.line2] and
                self.line2 in [other.line1, other.line2] and
                self.geometry == other.geometry)


    def parallel(self):
        """
        Boolean function to determine if two lines are parallel.
        """
        a1, b1, _ = self.line1.form()
        a2, b2, _ = self.line2.form()        
        return a1*b2 - a2*b1 == 0

    @check_geometry
    def spread(self):
        """
        Calculate the spread between two lines, as defined by the forumla
        
        s = 1 - (U.V)^2/(|U||V|)
        """
        vec1 = self.line1.vector()
        vec2 = self.line2.vector()

        num = self.geometry.dot(vec1, vec2)
        den = vec1.norm() * vec2.norm()

        # If den is zero we must have num zero and the lines must be null so
        # the spread is not defined.
        if num == den == 0:
            raise NullLineError
        else:
            return 1 - num*num/den

    @check_geometry
    def perpendicular(self):
        """
        Boolean function to determine if two lines are perpendicular
        """
        return self.spread() == 1


    @check_geometry
    def bisect(self):
        """
        Calculate the bisectors of the vertex. This returns a new
        vertex, since there are two lines which satisfy the bisection
        property.
        """
        X = self.point
        V = self.line1.vector()
        U = self.line2.vector()

        mu = (U.norm()/V.norm()).sqrt()

        X1 = X + V*mu + U
        X2 = X - V*mu + U

        assert (V*mu).norm() == U.norm()

        assert PointLine(X + V*mu, self.line1).on()
        assert PointLine(X - V*mu, self.line1).on()

        l1 = LineSegment(X, X1).line
        l2 = LineSegment(X, X2).line

        spread = Vertex(l1, self.line1).spread()
        assert self.spread() == 4*spread*(1 - spread)

        return Vertex(l1, l2)

    @check_geometry
    def grammola(self, K):
        #pylint: disable-msg=R0914
        a1, b1, c1 = self.line1.form()
        a2, b2, c2 = self.line2.form()
        a, b, c = self.geometry.form
    
        d1 = self.line1.vector().norm()
        d2 = self.line2.vector().norm()

        conic = Conic(d1*a2*a2 + d2*a1*a1, 2*(d1*a2*b2 + d2*a1*b1),
                      d1*b2*b2 + d2*b1*b1,
                      2*(d2*c1*a1 + d1*c2*a2), 2*(d2*c1*b1 + d1*c2*b2),
                      c1*c1*d2 + c2*c2*d1 - K*d1*d2/self.geometry.det(),
                      self.geometry)
        A, B, C = conic.a, conic.b, conic.c
        assert a*C - b*B + c*A ==  2*d1*d2
        return conic


class PointLine(object):

    def __init__(self, point, line):
        """
        Create a new PointLine from a point and a line.

        The point and line must be of the same geometry or else a GeometryError
        will be raised.
        """
        self.point = point
        self.line = line
        if line.geometry != point.geometry:
            raise GeometryError
        self.geometry = self.point.geometry

    def __eq__(self, other):
        return (self.point == other.point and
                self.line == other.line and
                self.geometry == other.geometry)

    def on(self):
        """
        Boolean function to determine whether the point lies on the line.
        """
        x, y = self.point.form()
        return self.line.eval(x, y) == 0

    @check_geometry
    def reflection(self):
        """
        Return the reflection of this point in the given line.
        """
        foot = self.altitude().point
        return PointLine(foot - (self.point - foot), self.line)

    @check_geometry
    def altitude(self):
        """
        Construct an altitude from the point to the line.
        This is a line which goes through the point and is perpendicular to
        the line.
        """
        altitude_vertex = self.construct_spread(1)
        assert altitude_vertex.line1 == altitude_vertex.line2
        return PointLine(Vertex(self.line, altitude_vertex.line1).point, altitude_vertex.line1)

    @check_geometry
    def quadrance(self):
        return LineSegment(self.altitude().point, self.point).quadrance()

    def parallel(self):
        """
        Construct a new line, parallel to the line and through the point.
        """
        a, b, _ = self.line.form()
        x, y = self.point.form()
        c = -(a*x + b*y)
        return Line(a, b, c, self.geometry)

    @check_geometry
    def construct_quadrance(self, quadrance):
        """
        Calculate the line segment whose points lie on this line
        and are a given quadrance from this point.
        """
        #pylint: disable-msg=R0914

        # unpack all the variables
        a, b, c, = self.geometry.form
        x0, y0 = self.point.form()
        a1, b1, c1 = self.line.form()

        if a1 == 0:
            # set up the parameters to solve
            # alpha * x^2 + beta * x + gamma = 0
            alpha = a*b1*b1 - 2*b*a1*b1 + c*a1*a1 
            beta  = (2*(a*(a1*c1 + b1*a1*y0) + \
                        b*b1*(a1*x0 - b1*y0 - c1) - 
                        c*b1*b1*x0))
            beta = 2*(-a*b1*b1*x0 + b*a1*b1*x0 - b*b1*b1*y0 - b*b1*c1 + 
                       c*a1*b1*y0 + c*a1*c1)
            gamma = (a*b1*b1*x0*x0 - b1*b1*quadrance + 2*b*b1*b1*x0*y0 + 
                     2*b*b1*c1*x0 + c*b1*b1*y0*y0 + c*c1*c1 + 2*c*b1*c1*y0)
            if alpha == 0:
                # Only one solution, taken from
                # solving b*x + g = 0, x = (-g/b, 0)
                if beta == 0:
                    raise ValueError
                x1 = x2 = -gamma/beta
            else:
                # solve for x, y
                det = beta*beta - 4*alpha*gamma
                
                x1 = (-beta + det.sqrt())/(2*alpha)
                x2 = (-beta - det.sqrt())/(2*alpha)

            y1 = -(a1*x1 + c1)/b1
            y2 = -(a1*x2 + c1)/b1
        else:
            # set up the parameters to solve
            # alpha * y^2 + beta * y + gamma = 0
            alpha = a*b1*b1 - 2*b*a1*b1 + c*a1*a1 
            beta  = (2*(a*(b1*c1 + a1*b1*x0) + \
                        b*a1*(b1*y0 - a1*x0 - c1) - 
                        c*a1*a1*y0))
            gamma = (a*(c1 + a1*x0)*(c1 + a1*x0) + 2*b*a1*y0*(a1*x0 + c1) +  
                     a1*a1*(c*y0*y0 - quadrance))

            if alpha == 0:
                # Only one solution, taken from
                # solving b*y + g = 0, y = (-g/b, 0)
                if beta == 0:
                    raise ValueError
                y1 = y2 = -gamma/beta
            else:
                # solve for x, y
                det = beta*beta - 4*alpha*gamma
                
                y1 = (-beta + det.sqrt())/(2*alpha)
                y2 = (-beta - det.sqrt())/(2*alpha)
        
            x1 = -(b1*y1 + c1)/a1
            x2 = -(b1*y2 + c1)/a1
        
        point1 = Point(x1, y1, self.geometry)
        point2 = Point(x2, y2, self.geometry)

        assert PointLine(point1, self.line).on()
        assert PointLine(point2, self.line).on()

        assert LineSegment(point1, self.point).quadrance() == quadrance
        assert LineSegment(point2, self.point).quadrance() == quadrance
        
        return LineSegment(point1, point2)
        

    @check_geometry
    def construct_spread(self, spread):
        """
        Calculate the Vertex which meets this point and which creates a given
        spread with this line from both of its lines.
        """
        #pylint: disable-msg=R0914
        if self.line.null():
            raise NullLineError

        if spread == 0:
            par = self.parallel()
            return Vertex(par, par)

        a, b, c = self.geometry.form
        x0, y0 = self.point.form()
        a1, b1, _ = self.line.form()

        U = self.line.vector()
        k = (1 - spread)*U.norm()

        # set up the parameters to solve
        # alpha * x^2 + beta * x * y + gamma * y^2 = 0
        # if alpha == 0:
        #  => b * x * y + gamma * y * y == 0
        #     y(b * x + gamma * y) == 0
        #     x/y == -gamma/beta
        alpha =    (a*b1 - b*a1)*(a*b1 - b*a1) - k*a
        beta  = 2*((a*b1 - b*a1)*(b*b1 - c*a1) - b*k)
        gamma =    (b*b1 - c*a1)*(b*b1 - c*a1) - k*c

        if alpha == 0:
            a2 = alpha     # = 0; We use alpha like this
            b2 = alpha + 1 # = 1; to maintain the field

            a3 = beta
            b3 = gamma
        else:
            det = beta*beta - 4*alpha*gamma
            
            a2 = a3 = 2*alpha
            b2 = beta + det.sqrt()
            b3 = beta - det.sqrt()
            
        c2 = -(a2*x0 + b2*y0)
        c3 = -(a3*x0 + b3*y0)
            
        l2 = Line(a2, b2, c2, self.geometry)
        l3 = Line(a3, b3, c3, self.geometry)

        assert PointLine(self.point, l2).on()
        assert PointLine(self.point, l3).on()

        assert Vertex(l2, l3).point == self.point or (l2 == l3 and spread == 1)

        assert Vertex(self.line, l2).spread() == spread or l2.null()
        assert Vertex(self.line, l3).spread() == spread or l3.null()

        return Vertex(l2, l3)

    @check_geometry
    def parabola(self):
        """
        Create a parabola using this PointLine as the focus and directrix.
        """
        return self.conic(1)

    @check_geometry
    def conic(self, K):
        """
        Create a conic, using thie PointLine as the focus and directrix, and
        having a ratio of K.        
        """
        if self.line.null():
            raise NullLineError

        a, b, c = self.geometry.form
        a1, b1, c1 = self.line.form()
        x0, y0, = self.point.form()

        alpha = self.geometry.det()/self.line.vector().norm()
    
        return Conic(a - K*alpha*a1*a1, 2*(b - K*alpha*a1*b1),
                     c - K*alpha*b1*b1,
                     -2*(a*x0 + b*y0 + a1*c1*K*alpha),
                     -2*(b*x0 + c*y0 + b1*c1*K*alpha),
                     self.point.norm() - K*alpha*c1*c1,
                     self.geometry)
