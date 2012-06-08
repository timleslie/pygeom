import matplotlib.pyplot as plt
from matplotlib.ticker import IndexLocator, NullFormatter, ScalarFormatter

from pygeom.geometry import blue, red, green, Geometry

from field import FiniteField
from core import Line
from conic import Conic

class Plot(object):
    def __init__(self):
        self.objects = []

    def plot(self):
        raise NotImplementedError

    def add_object(self, object, name, marker):
        self.objects.append((object, name, marker))
        


class FinitePlot(Plot):

    def __init__(self):
        Plot.__init__(self)
    
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        handles = []
        labels = []
        for object, name, marker in self.objects:
            xs = []
            ys = []
            l = object
            for x in range(59):
                for y in range(59):
                    if object.eval(x, y) == 0:
                        xs.append(x)
                        ys.append(y)
            print object, name, marker
            print zip(xs, ys)
            handles.append(ax.scatter(xs, ys, marker=marker, s=100))
            labels.append(name)
        

        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(-0.5, 10.5)

        ax.xaxis.set_major_locator( IndexLocator(-0.5, 1) )
        ax.xaxis.set_minor_locator( IndexLocator(0, 1) )
        ax.yaxis.set_major_locator( IndexLocator(-0.5, 1) )
        ax.yaxis.set_minor_locator( IndexLocator(0, 1) )
        
        ax.xaxis.set_major_formatter( NullFormatter() )
        ax.xaxis.set_minor_formatter( ScalarFormatter() )
        ax.yaxis.set_major_formatter( NullFormatter() )
        ax.yaxis.set_minor_formatter( ScalarFormatter() )


        ax.set_xticks(range(0, 59), minor=True)
        ax.set_yticks(range(0, 59), minor=True)

        ax.set_xticks([x + 0.5 for x in range(0, 59)])
        ax.set_yticks([x + 0.5 for x in range(0, 59)])

        ax.grid(True)
        plt.figlegend(handles, labels, scatterpoints=1, loc=1)

        plt.show()

    
if __name__ == '__main__':
    fp = FinitePlot()

    f = FiniteField
    f.base = 59
    
    l1 = Line(f(1), f(2), f(3))
    l2 = Line(f(1), f(4), f(4))
    c1 = Conic(f(1), f(0), f(-1), f(0), f(0), f(4), blue(f))
    fp.add_object(l1, "foo", "s")
    fp.add_object(l2, "bar", "o")
    fp.add_object(c1, "baz", "x")

    print "====", c1.centre_quadrance()

    fp.plot()
