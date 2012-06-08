from pylab import imshow, show, grid, pcolor
import pylab
from numpy import zeros

from pygeom.field import FiniteField
from pygeom.point import Line

f = FiniteField
f.base = 13

l1 = Line(f(1), f(1), f(0))

image = zeros((f.base, f.base))

for x in range(f.base):
    for y in range(f.base):
        image[x, y] = (l1.a*x + l1.b*y + l1.c).value != 0

print image

pcolor(image, cmap=pylab.cm.gray)
grid()
show()


