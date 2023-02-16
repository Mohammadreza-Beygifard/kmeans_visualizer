import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y=y
    def EucDist(self, point):
        x = self.x - point.x
        y = self.y - point.y
        return np.sqrt(x**2 + y**2)



p1 = Point(1, 1)
p2 = Point(0, 0)

print(p2.EucDist(p1))