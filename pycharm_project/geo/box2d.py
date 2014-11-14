__author__ = 'Edward'

import math
try:
    import pygame
    graphics = True
except ImportError:
    graphics = False

import util
from geo.combinatorialbody import CombinatorialBody2d
import visualizer.renderable


class Box2d(CombinatorialBody2d, visualizer.renderable.Renderable):

    def __init__(self, pos=(0, 0), vec1=(1, 0), vec2=(0, 1), provide_center=True, comment=None):
        super(Box2d, self).__init__()

        if provide_center:
            self.x = pos[0] - vec1[0] / 2 - vec2[0] / 2
            self.y = pos[1] - vec1[1] / 2 - vec2[1] / 2
            self.vec1 = vec1
            self.vec2 = vec2
        else:
            self.x, self.y = pos
            self.vec1 = vec1
            self.vec2 = vec2

        if comment is not None:
            self.comment = comment
        else:
            self.comment = "Arbitrary Box"

    def __contains__(self, item):
        c = self.get_corners()
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

    def center(self):
        return self.x + (self.vec1[0] + self.vec2[0])/2, self.y + (self.vec1[1] + self.vec2[1])/2

    def valid(self):
        return math.fabs(self.vec1[0] * self.vec2[0] + self.vec1[1] * self.vec2[1]) <= 1e-10

    def rotate_about_2d(self, theta, pt=(0, 0), is_radians=True):
        self.x, self.y = util.get_rotated_about_2d([self.x, self.y], theta, pt, is_radians)
        self.vec1 = util.get_rotated_about_2d(self.vec1, theta, pt, is_radians)
        self.vec2 = util.get_rotated_about_2d(self.vec2, theta, pt, is_radians)
        if not self.valid():
            print("WARNING: Box2d::rotate() invalid vectors after rotation")
        return self

    def get_rotated_about_2d(self, theta,  pt=(0, 0), is_radians=True):
        return self.clone().rotate_about_2d(theta, pt, is_radians)

    def set_pos(self, pos, set_center=True):
        if set_center:
            self.x = pos[0] - self.vec1[0] / 2 - self.vec2[0] / 2
            self.y = pos[1] - self.vec1[1] / 2 - self.vec2[1] / 2
        else:
            self.x, self.y = pos
        return self

    def translate(self, translation):
        self.x += translation[0]
        self.y += translation[1]
        return self

    def clone(self, other):
        super(Box2d, self).clone(other)
        self.x, self.y = other.x, other.y
        self.vec1, self.vec2 = other.vec1, other.vec2

    def get_corners(self):
        return [(self.x, self.y),
            (self.x + self.vec1[0], self.y + self.vec1[1]),
            (self.x + self.vec1[0] + self.vec2[0], self.y + self.vec1[1] + self.vec2[1]),
            (self.x + self.vec2[0], self.y + self.vec2[1])]

    def get_bounds(self):
        c = self.get_corners()
        return [min([cc[0] for cc in c]), max([cc[0] for cc in c]),
               min([cc[1] for cc in c]), max([cc[1] for cc in c]), 0, 1]

    def draw2d(self, screen=None):
        if not graphics or self.visualizer is None:
            return
        d = self.get_corners()

        d = [(q[0] * self.visualizer.scale + self.visualizer.gx, q[1] * self.visualizer.scale - self.visualizer.gy ) for q in d]

        if screen is None:
            pygame.draw.aalines(self.visualizer.screen, self.color, True,
                                [[int(k[0]), 400-int(k[1])] for k in d], True)
        else:
            pygame.draw.aalines(screen, self.color, True,
                                [[int(k[0]), 400-int(k[1])] for k in d], True)

    def __str__(self):
        pt = self.x, self.y
        v1 = self.vec1
        v2 = self.vec2
        return "  " + str(self.id) + ": BOX: " + \
               ", ".join(str(x) for x in [pt[0], pt[1], 0,
                                          v1[0], v1[1], 0,
                                          v2[0], v2[1], 0,
                                          0, 0, 1]) + " :: " + self.comment