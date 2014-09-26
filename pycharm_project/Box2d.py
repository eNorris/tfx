__author__ = 'Edward'

import math
try:
    import pygame
    graphics = True
except ImportError:
    graphics = False

from CombinatorialBody import CombinatorialBody


class Box2d(CombinatorialBody):

    def __init__(self, center=(0, 0), vec1=(1, 0), vec2=(0, 1)):
        super(Box2d, self).__init__()

        self.cx, self.cy = center
        self.vec1 = vec1
        self.vec2 = vec2

        self.comment = "Arbitrary Box"

    def valid(self):
        return math.fabs(self.vec1[0] * self.vec2[0] + self.vec1[1] * self.vec2[1]) <= 1e-10

    def rotate(self, theta):
        self.vec1 = [self.vec1[0] * math.cos(theta) - self.vec1[1] * math.sin(theta),
                     self.vec1[0] * math.sin(theta) + self.vec1[1] * math.cos(theta)]
        self.vec2 = [self.vec2[0] * math.cos(theta) - self.vec2[1] * math.sin(theta),
                     self.vec2[0] * math.sin(theta) + self.vec2[1] * math.cos(theta)]
        if not self.valid():
            print("WARNING: Box2d::rotate() invalid vectors after rotation")
        return self

    def rotate_about(self, theta, pt=(0, 0)):
        self.rotate(theta)
        posvec = [pt[0] - self.cx, pt[1] - self.cy]
        dx = posvec[0] * math.cos(theta) - posvec[1] * math.sin(theta)
        dy = posvec[0] * math.sin(theta) + posvec[1] * math.cos(theta)
        self.cx += posvec[0] - dx
        self.cy += posvec[1] - dy
        return self

    def set_pos(self, pos):
        self.cx, self.cy = pos
        return self

    def translate(self, translation):
        self.cx += translation[0]
        self.cy += translation[1]
        return self

    def clone(self):
        b = Box2d([self.cx, self.cy], self.vec1, self.vec2)
        b.color = self.color
        return b

    def getcorners(self):
        return [(self.cx - self.vec1[0] - self.vec2[0], self.cy - self.vec1[1] - self.vec2[1]),
                (self.cx + self.vec1[0] - self.vec2[0], self.cy + self.vec1[1] - self.vec2[1]),
                (self.cx + self.vec1[0] + self.vec2[0], self.cy + self.vec1[1] + self.vec2[1]),
                (self.cx - self.vec1[0] + self.vec2[0], self.cy - self.vec1[1] + self.vec2[1])]

    def draw2d(self):
        if not graphics or self.visualizer is None:
            return
        d = self.getcorners()

        d = [(q[0] * self.visualizer.scale + self.visualizer.gx, q[1] * self.visualizer.scale - self.visualizer.gy ) for q in d]

        #pygame.draw.rect(self.visualizer.screen, self.color,
        #                 [int(self.left), 400-int(self.top), int(self.w), int(self.h)], 1)
        pygame.draw.aalines(self.visualizer.screen, self.color, True,
                            [[int(k[0]), 400-int(k[1])] for k in d], True)

    def __str__(self):
        pt = self.getcorners()[0]
        v1 = self.vec1
        v2 = self.vec2
        return "  " + str(self.id) + ": BOX: " + \
               ", ".join(str(x) for x in [pt[0], pt[1], 0,
                                          v1[0], v1[1], 0,
                                          v2[0], v2[1], 0,
                                          0, 0, 1]) + " :: " + self.comment