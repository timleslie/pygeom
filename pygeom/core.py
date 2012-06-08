"""
This module provides the core objects in the pygeom library, namely Points,
Lines and Conics
"""

from pygeom.util import check_geometry, all_equal

class Core(object):
    """
    Base class to provide an interface and perform some common checks on
    the core objects.
    """
    def __init__(self, geometry):
        self.geometry = geometry
        if geometry is None:
            geom_form = []
        else:
            geom_form = list(geometry.form)
        form = list(self.form()) + geom_form
        if not all_equal([type(number) for number in form]):
            raise TypeError

    def form(self):
        """
        Return a tuple representation of the object.
        """
        raise NotImplementedError
        
    def eval(self, x, y):
        """
        Evaluate whether the given x, y coordinates "match this object".
        """
        raise NotImplementedError

    def __eq__(self, other):
        """
        For two objects to be equal they must have the same form
        and also reside in the same geometry.
        """
        return bool(self.__class__ == other.__class__ and
                    self.form() == other.form() and
                    self.geometry == other.geometry)

    def __ne__(self, other):
        return not self == other

class Point(Core):
    """
    A point is defined as pair of values, [x, y] taken from a particular field.
    A point exists within the context of a geometry over the same field.

    Points can also be used to represent vectors, and are used interchangably
    in this implementation, despite their subtle semantic differences.
    """

    def __init__(self, x, y, geometry=None):
        """
        Create a point [x, y] in the given geometry.

        If no geometry is specified then none of the metric functionality of
        the library will be available for this point.
        """
        self.x = x
        self.y = y
        Core.__init__(self, geometry)

    def form(self):
        """
        Return a tuple representation of the object.
        """
        return self.x, self.y

    def eval(self, x, y):
        """
        Evaluate whether the given x, y coordinates "match this object".

        In this case, check if they are equal to the point.
        """
        if x == self.x and y == self.y:
            return 0
        else:
            return 1

    def __repr__(self):
        return "[%s, %s]" % (str(self.x), str(self.y))

    def __sub__(self, other):
        """
        Vector substraction.
        """
        return Point(self.x - other.x, self.y - other.y, self.geometry)

    def __mul__(self, other):
        """
        Scalar multiplcation.
        """
        return Point(self.x * other, self.y * other, self.geometry)

    def __rmul__(self, other):
        """
        Scalar multiplcation.
        """
        return self * other

    def __add__(self, other):
        """
        Vector addition.
        """
        return Point(self.x + other.x, self.y + other.y, self.geometry)

    def __div__(self, other):
        """
        Scalar division.
        """
        return Point(self.x / other, self.y / other, self.geometry)

    @check_geometry
    def null(self):
        """
        Boolean method to check if this is a null point.

        A null point is one whose quadrance from the origin is zero.
        """
        return self.norm() == 0

    @check_geometry
    def norm(self):
        """
        The norm of the vector from the origin to this point.
        """
        return self.geometry.norm(self)

    def circle(self, quadrance):
        """
        Create a circle with a given quadrance centred at this point.
        """
        x, y = self.form()
        a, b, c = self.geometry.form
        return Conic(a, 2*b, c, -2*(a*x + b*y), -2*(b*x + c*y), 
                     self.norm() - quadrance, self.geometry)


class Line(Core):

    def __init__(self, a, b, c, geometry=None):
        a, b, c = a.reduce([b, c])
        self.a = a
        self.b = b
        self.c = c
        Core.__init__(self, geometry)

    def form(self):
        """
        Return a tuple representation of the object.
        """
        return self.a, self.b, self.c

    def eval(self, x, y):
        """
        Evaluate whether the given x, y coordinates "match this object".

        In this case check whether the point is on the line.
        """
        return self.a*x + self.b*y + self.c

    def __repr__(self):
        return "<%s:%s:%s>" % (str(self.a), str(self.b), str(self.c))


    def vector(self):
        """
        Return a Point which represents a vector parallel to this line.
        """
        return Point(-self.b, self.a, self.geometry)

    @check_geometry
    def null(self):
        """
        Boolean method to check if this is a null line.

        A line is a null line of all points on it are null points.
        """
        return self.vector().null()


class Conic(Core):
    def __init__(self, a, b, c, d, e, f, geometry=None):
        #pylint: disable-msg=R0913
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        Core.__init__(self, geometry)
    
    def form(self):
        """
        Return a tuple representation of the object.
        """
        return self.a, self.b, self.c, self.d, self.e, self.f

    def __repr__(self):
        return "<%s:%s:%s:%s:%s:%s>" % (str(self.a), str(self.b), str(self.c),
                                        str(self.d), str(self.e), str(self.f))

    def eval(self, x, y):
        """
        Evaluate whether the given x, y coordinates "match this object".

        In this case check whether the point is on the conic.
        """
        a, b, c, d, e, f = self.form()
        return a*x*x + b*x*y + c*y*y + d*x + e*y + f

    def through(self, point):
        """
        Check whether the conic passes through the point.
        """
        x, y = point.form()
        return self.eval(x, y) == 0

    def det(self):
        """
        The determinant of the matrix P [[a, b/2], [b/2, c]].
        """
        return self.a*self.c - self.b*self.b/4

    def _point_on(self):
        a, b, c, d, e, f = self.form()
        #y = (-(b + e) + ((b + e)*(b + e) - 4*c*(a + d + f)).sqrt())/(2*c)
        y = (-e + (e*e - 4*c*f).sqrt())/(2*c)
        x = y - y
        point = Point(x, y, self.geometry)
        assert self.through(point)
        return point

    def is_parabola(self):
        """
        Check whether this conic is a parabola.
        """
        return self.det() == 0

    @check_geometry
    def is_circle(self):
        """
        Boolean function to determine whether this conic is a circle.
        """
        a, b, c = self.geometry.form
        a1, b1, c1, _, _, _ = self.form()

        return (a1*2*b == b1*a and
                a1*c == c1*a and
                b1*c == c1*2*b)

    @check_geometry
    def centre_quadrance(self):
        """
        Return a point and a quadrance, representing the centre and radius
        quadrance of the circle.
        """
        # return a point and a quadrance        
        a, b, c = self.geometry.form
        d1, e1 = self.d, self.e

        x0 = -(c*d1 - b*e1)/(2*self.geometry.det())
        y0 = -(-b*d1 + a*e1)/(2*self.geometry.det())

        centre = Point(x0, y0, self.geometry)

        K = centre.norm() - self.f

        return centre, K

    @check_geometry
    def focus_directrix(self):
        """
        Calculate the two focus/directrix pairs for this conic as well as
        the corresponding ratio K.
        """
        #pylint: disable-msg=R0914
        from pygeom.pairs import PointLine
        a, b, c = self.geometry.form
        D, E, F = self.d, self.e, self.f
        a1 = a - self.a
        b1 = b - self.b/2
        
        AA = 4*(a*b1*b1 - 2*b*a1*b1 + c*a1*a1 - a1*self.geometry.det())
        BB = 4*a1*((a*E - b*D)*b1 + (- b*E + c*D)*a1)
        CC = a1*a1*(a*E*E - 2*b*E*D + c*D*D - 4*self.geometry.det()*F)

        c11 = (-BB + (BB*BB - 4*AA*CC).sqrt())/(2*AA)
        c12 = (-BB - (BB*BB - 4*AA*CC).sqrt())/(2*AA)

        direc1, direc2 = (Line(a1, b1, c11, self.geometry),
                          Line(a1, b1, c12, self.geometry))

        K = (a*b1*b1 - 2*b*a1*b1 + c*a1*a1)/(a1*self.geometry.det())

        x1 = -(c*(2*c11 + D) - b*(2*c11*b1/a1 + E))/(2*self.geometry.det())
        y1 = -(-b*(2*c11 + D) + a*(2*c11*b1/a1 + E))/(2*self.geometry.det())

        x2 = -(c*(2*c12 + D) - b*(2*c12*b1/a1 + E))/(2*self.geometry.det())
        y2 = -(-b*(2*c12 + D) + a*(2*c12*b1/a1 + E))/(2*self.geometry.det())

        focus1 = Point(x1, y1, self.geometry)
        focus2 = Point(x2, y2, self.geometry)

        focus_direc_1 = PointLine(focus1, direc1)
        focus_direc_2 = PointLine(focus2, direc2)

        return (focus_direc_1, focus_direc_2, K)


    @check_geometry
    def co_diagonal(self, line):
        """
        If this conic is a grammola, then return 
        the co-diagonal line as well as the grammola constant K.
        """

        A, B, C, D, E, F = self.form()
        a1, b1, _ = line.form()
        a, b, c = self.geometry.form

        alpha = (A*c - B*b + C*a)
        d1 = line.vector().norm()
        assert d1 == a*b1*b1 - 2*b*a1*b1 + c*a1*a1

        a2  = ((2*A*d1 - a1*a1*alpha)/(2*d1*d1)).sqrt()
        b22 = ((2*C*d1 - b1*b1*alpha)/(2*d1*d1)).sqrt()
        if a2 == 0:
            b2 = a2 + 1
        else:
            b2 = ((  B*d1 - a1*b1*alpha)/(2*d1*d1))/a2
            print b2, b22, -b22
    
        x = 2*A*d1 - alpha*a1*a1
        y =   B*d1 - alpha*a1*b1
        z = 2*C*d1 - alpha*b1*b1
        assert x*z == y*y

        d2 = a*b2*b2 - 2*b*a2*b2 + c*a2*a2
        assert a1*b2 - a2*b1 != 0

        c1 = ( b2*D - a2*E)/(2*d2*(a1*b2 - a2*b1))
        c2 = (-b1*D + a1*E)/(2*d1*(a1*b2 - a2*b1))

        assert c1 == line.c

        K = (a*c - b*b)*(c1*c1/d1 + c2*c2/d2  - F/(d1*d2))
        
        return Line(a2, b2, c2, self.geometry), K


    def tangent(self, point):
        """
        Calculate the tangent to the conic through the given point.

        If the point does not lie on the conic a ValueError is raised.
        """
        if not self.through(point):
            raise ValueError
        return self.polar(point)

    def is_tangent(self, line):
        """
        Check if the given line is tangent to this conic.
        """
        # (Bc + Db + Ea)^2 -4(ACc^2 + AFb^2 + CFa^2) + 4((AE - BD)bc + (CD - BE)ac  + (BF- DE)ab) = 0

        A, B, C, D, E, F = self.form()
        a, b, c = line.form()

        return (B*c + D*b + E*a)*(B*c + D*b + E*a) - 4*(A*C*c*c + A*F*b*b + C*F*a*a) + 4*((A*E - B*D)*b*c + (C*D - B*E)*a*c + (B*F - D*E)*a*b ) == 0


    def pole(self, polar):
        """
        Calculate the pole of the given polar.
        """
        #pylint: disable-msg=R0914
        a, b, c, d, e, f = self.form()
        det_p = self.det()
        a1, b1, c1 = polar.form()
        
        num = (d*(c*d  - b*e/2)  + e*(-b*d/2  + a*e ))/(2*det_p) - 2*f
        den = (d*(c*a1 - b*b1/2) + e*(-b*a1/2 + a*b1))/(2*det_p) - c1

        a2 = num*a1/den - d
        b2 = num*b1/den - e

        x = 1/(2*det_p)*(c*a2 - b*b2/2)
        y = 1/(2*det_p)*(-b*a2/2 + a*b2)

        return Point(x, y, self.geometry)

    def polar(self, pole):
        """
        Calculate the polar of the given pole.
        """
        x, y = pole.form()
        a, b, c, d, e, f = self.form()

        # (2PX_0 + q)X + (qX_0 + 2r)

        a1 = (2*(a*x + b*y/2) + d)
        b1 = (2*(b*x/2 + c*y) + e)

        c1 = d*x + e*y + 2*f
        return Line(a1, b1, c1, self.geometry)
