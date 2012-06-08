class Polygon(object):
    
    def __init__(self, points):
        self.points = points

       
    def centroid(self):
        pass

    
    def altitudes(self):
        pass

    def perpindicular_bisectors(self):
        pass

    
    def angle_bisectors(self):
        pass

# A triangle has:
#  6 midpoints
#  4 centroids
#  6 medians [lines through 2 centroids, vertex, midpoint]
#  4 centrians [ lines through 3 midpoints]

# Orthocentre becomes the line through (a, a*), (b, b*), (c, c*)

# We have two midpoints per line, so 2 perpindicular bisectors!
# So we get 4 circumcenters!!!
# Each of these is the centre of a circle which goes through the three points of the triangle...

