from pygeom.core import Point, Line, Conic
from pygeom.pairs import Vertex, LineSegment, PointLine
from pygeom.geometry import Geometry, blue, red, green
from pygeom.field import Rational, FiniteField

def random_point(field, geometry):
    x, y = field.random(), field.random()
    return Point(x, y, geometry)

def random_line(field, geometry):
    a, b, c = field.random(), field.random(), field.random()
    return Line(a, b, c, geometry)

def random_conic(field, geometry):
    a, b, c, d, e, f = field.random(), field.random(), field.random(), field.random(), field.random(), field.random()
    return Conic(a, b, c, d, e, f, geometry)

def random_vertex(field, geometry):
    return Vertex(random_line(field, geometry),
                  random_line(field, geometry))

def random_linesegment(field, geometry):
    return LineSegment(random_point(field, geometry),
                       random_point(field, geometry))

def random_pointline(field, geometry):
    return PointLine(random_point(field, geometry),
                     random_line(field, geometry))

def random_geometry(field):
    while True:
        a, b, c = field.random(), field.random(), field.random()
        try:
            return Geometry(a, b, c)
        except ValueError:
            pass

class FuzzData(object):
    
    def __init__(self, field, geom, lines, points, vertices, line_segments, pointlines, spreads, conics, geoms):
        self.field = field
        self.geom = geom
        self.lines = lines
        self.points = points
        self.vertices = vertices
        self.line_segments = line_segments
        self.pointlines = pointlines
        self.spreads = spreads
        self.conics = conics
        self.geoms = geoms

    def __repr__(self):
        return "".join(map(str, [self.field, self.geom, self.pointlines, self.spreads]))

def random_finite_fields(N):
    yield Rational
    FiniteField.base = 37
    for base in N*[3, 7, 37, 101]:
        FiniteField.base = base
        yield FiniteField
        

def generate_fuzz_data(N, lines=0, points=0, vertices=0, line_segments=0, pointlines=0, spreads=0, conics=0, geoms=0):

    # Iterate over a bunch of fields
    for field in random_finite_fields(3):

        # then over a bunch of geometries
        for geom in [blue, red, green] + [random_geometry for _ in range(6)]:
            geom = geom(field)

            # then over the N data sets
            for _ in range(N):
                yield FuzzData(field, geom,
                               [random_line(field, geom) for _ in range(lines)],
                               [random_point(field, geom) for _ in range(points)],
                               [random_vertex(field, geom) for _ in range(vertices)],
                               [random_linesegment(field, geom) for _ in range(line_segments)],
                               [random_pointline(field, geom) for _ in range(pointlines)],   
                               [field.random() for _ in range(spreads)],
                               [random_conic(field, geom) for _ in range(conics)],
                               [random_geometry(field) for _ in range(geoms)]
                               )

        
