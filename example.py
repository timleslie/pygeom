from pygeom.field import FiniteField
from pygeom.geometry import red
from pygeom.core import Point
from pygeom.pairs import LineSegment, PointLine, Vertex

# Set up the field
f = FiniteField
f.base = 13

geometry = red(f)

# Create the points
A = Point(f(3), f(7), geometry)
B = Point(f(4), f(12), geometry)
C = Point(f(9), f(2), geometry)

# Create the lines of the triangle
AB = LineSegment(A, B)
AC = LineSegment(A, C)
BC = LineSegment(B, C)

# Create the altitudes
alt_a = PointLine(A, BC.line).altitude().line
alt_b = PointLine(B, AC.line).altitude().line
alt_c = PointLine(C, AB.line).altitude().line

# Calculate the points of intersection of the altitudes
O_ab = Vertex(alt_a, alt_b).point
O_bc = Vertex(alt_b, alt_c).point
O_ca = Vertex(alt_c, alt_a).point

# Check that the points are indeed equal
assert O_ab == O_bc == O_ca
print "Orthocentre:", O_ab

# Find the circumcentre
C_a = BC.perp_bisector()
C_b = AC.perp_bisector()
C_0 = Vertex(C_a, C_b).point
print "Circumcentre:", C_0

# Check the quadrances
Q_a = LineSegment(A, C_0).quadrance()
Q_b = LineSegment(B, C_0).quadrance()
Q_c = LineSegment(C, C_0).quadrance()
assert Q_a == Q_b == Q_c
print "Circumquadrance:", Q_a
