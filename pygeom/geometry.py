# pylint: disable-msg=C0103

class Geometry(object):

    def __init__(self, a, b, c):
        self.form = a, b, c
        if self.det() == 0:
            raise ValueError, "Singular matrix cannot be used for a geometry."

    def dot(self, point1, point2):
        a, b, c = self.form
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y

        return x1*(a*x2 + b*y2) + y1*(b*x2 + c*y2)

    def det(self):
        a, b, c = self.form
        return a*c - b*b

    def norm(self, point):
        return self.dot(point, point)

    def __repr__(self):
        a, b, c = self.form
        return "[%s %s ; %s %s]" % (str(a), str(b), str(b), str(c))

    def __eq__(self, other):
        return bool(self.__class__ == other.__class__ and 
                    self.form == other.form)

    def __ne__(self, other):
        return not (self == other)

def blue(field):
    """
    The canonical "blue" geometry.
    """
    return Geometry(field(1), field(0), field(1))

def green(field):
    """
    The canonical "green" geometry.
    """
    return Geometry(field(0), field(1), field(0))

def red(field):
    """
    The canonical "red" geometry.
    """
    return Geometry(field(1), field(0), field(-1))

