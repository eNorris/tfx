__author__ = 'Edward'

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False
import math

from CombinatorialBody import CombinatorialBody

class Raw2d(CombinatorialBody):

    def __init__(self, refpoint, v1, v2):
        super(Raw2d, self).__init__()
        self.px, self.py = refpoint
        self.vec1 = v1
        self.vec2 = v2
        self.comment = "Right Angle Wedge"

    def __contains__(self, item):
        c = self.getcorners()
        if len(c) < 3:
            return False
        v1 = c[0][0] - c[-1][0], c[0][1] - c[-1][1]
        v2 = c[0][0] - item[0], c[0][1] - item[1]
        positive = v1[0] * v2[1] - v1[1] * v2[0] >= 0
        for i in range(1, len(c)):
            v1 = c[i][0] - c[i-1][0], c[i][1] - c[i-1][1]
            v2 = c[i][0] - item[0], c[i][1] - item[1]
            if (v1[0] * v2[1] - v1[1] * v2[0] >= 0) != positive:
                return False
        return True

    def rotate(self, theta):
        self.vec1 = [self.vec1[0] * math.cos(theta) - self.vec1[1] * math.sin(theta),
                     self.vec1[0] * math.sin(theta) + self.vec1[1] * math.cos(theta)]
        self.vec2 = [self.vec2[0] * math.cos(theta) - self.vec2[1] * math.sin(theta),
                     self.vec2[0] * math.sin(theta) + self.vec2[1] * math.cos(theta)]
        return self

    def rotate_about(self, theta, pt=(0, 0)):

        self.rotate(theta)
        posvec = [pt[0] - self.px, pt[1] - self.py]
        dx = posvec[0] * math.cos(theta) - posvec[1] * math.sin(theta)
        dy = posvec[0] * math.sin(theta) + posvec[1] * math.cos(theta)
        self.px += posvec[0] - dx
        self.py += posvec[1] - dy
        return self

    def clone(self):
        b = Raw2d((self.px, self.py), self.vec1, self.vec2)
        b.color = self.color
        return b

    def getcorners(self):
        return [(self.px, self.py), (self.px+self.vec1[0], self.py+self.vec1[1]), (self.px+self.vec2[0], self.py+self.vec2[1])]

    def draw2d(self):
        if not graphics or self.visualizer is None:
            return
        d = self.getcorners()

        d = [(q[0] * self.visualizer.scale + self.visualizer.gx, q[1] * self.visualizer.scale - self.visualizer.gy) for q in d]

        #pygame.draw.rect(self.visualizer.screen, self.color,
        #                 [int(self.left), 400-int(self.top), int(self.w), int(self.h)], 1)
        pygame.draw.aalines(self.visualizer.screen, self.color, True,
                            [[int(k[0]), 400-int(k[1])] for k in d], True)

    def __str__(self):
        pt = (self.px, self.py)
        v1 = self.vec1
        v2 = self.vec2
        return "  " + str(self.id) + ": RAW: " + \
               ", ".join(str(x) for x in [pt[0], pt[1], 0,
                                          v1[0], v1[1], 0,
                                          v2[0], v2[1], 0,
                                          0, 0, 1]) + " :: " + self.comment