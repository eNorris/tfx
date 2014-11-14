__author__ = 'Edward'

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False
import util

import visualizer.renderable

from geo.combinatorialbody import CombinatorialBody2d

class Raw2d(CombinatorialBody2d, visualizer.renderable.Renderable):

    def __init__(self, refpoint=(0, 0), v1=(1, 0), v2=(0, 1), comment=None):
        super(Raw2d, self).__init__()
        self.px, self.py = refpoint
        self.vec1 = v1
        self.vec2 = v2

        if comment is not None:
            self.comment = comment
        else:
            self.comment = "Right Angle Wedge"
        self.validate()

    def __contains__(self, item):
        c = self.get_corners()
        if len(c) < 3:
            return False
        v1 = c[0][0] - c[-1][0], c[0][1] - c[-1][1]
        v2 = c[0][0] - item[0], c[0][1] - item[1]
        positive = v1[0] * v2[1] - v1[1] * v2[0] > 0
        for i in range(1, len(c)):
            v1 = c[i][0] - c[i-1][0], c[i][1] - c[i-1][1]
            v2 = c[i][0] - item[0], c[i][1] - item[1]
            if (v1[0] * v2[1] - v1[1] * v2[0] > 1e-10) != positive:
                return False
        return True

    def validate(self):
        if self.vec1[0] * self.vec2[0] + self.vec1[1] * self.vec2[1] >= 1e-10:
            raise Exception("Invalid Raw2d, vectors must be mutually perpendicualr")
        return True

    def rotate_about_2d(self, theta, pt=(0, 0), is_radians=True):
        self.px, self.py = util.get_rotated_about_2d((self.px, self.py), theta, pt, is_radians)
        self.vec1 = util.get_rotated_about_2d(self.vec1, theta, pt, is_radians)
        self.vec2 = util.get_rotated_about_2d(self.vec2, theta, pt, is_radians)
        return self

    def get_bounds(self):
        c = self.get_corners()
        return [min([cc[0] for cc in c]), max([cc[0] for cc in c]), min([cc[1] for cc in c]), max([cc[1] for cc in c]), 0, 1]

    def clone(self, other):
        super(Raw2d, self).clone(other)
        self.px, self.py = other.px, other.py
        self.vec1, self.vec2 = other.vec1, other.vec2

    def get_corners(self):
        return [(self.px, self.py), (self.px+self.vec1[0], self.py+self.vec1[1]), (self.px+self.vec2[0], self.py+self.vec2[1])]

    def centroid(self):
        c = self.get_corners()
        return (c[0][0] + c[1][0] + c[2][0])/3, (c[0][1] + c[1][1] + c[2][1])/3

    def draw2d(self, screen=None):
        if not graphics or self.visualizer is None:
            return

        raise Exception("Raw2d::draw2d is no longer used")

    def __str__(self):
        pt = (self.px, self.py)
        v1 = self.vec1
        v2 = self.vec2
        return "  " + str(self.id) + ": RAW: " + \
               ", ".join(str(x) for x in [pt[0], pt[1], 0,
                                          v1[0], v1[1], 0,
                                          v2[0], v2[1], 0,
                                          0, 0, 1]) + " :: " + self.comment