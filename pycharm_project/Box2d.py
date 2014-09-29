__author__ = 'Edward'

import math
try:
    import pygame
    graphics = True
except ImportError:
    graphics = False

from CombinatorialBody import CombinatorialBody


class Box2d(CombinatorialBody):

    def __init__(self, center=(0, 0), vec1=(1, 0), vec2=(0, 1), provide_center=True):
        super(Box2d, self).__init__()

        if provide_center:
            self.x = center[0] - vec1[0] / 2 - vec2[0] / 2
            self.y = center[1] - vec1[1] / 2 - vec2[1] / 2
            self.vec1 = vec1
            self.vec2 = vec2
        else:
            self.x, self.y = center
            self.vec1 = [v/2 for v in vec1]
            self.vec2 = [v/2 for v in vec2]

        self.comment = "Arbitrary Box"

    def __contains__(self, item):
        # Based this off some code I found online by Jonas Elfstrom
        # http://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not
        corners = self.getcorners()
        ax, ay = corners[0]
        bx, by = corners[1]
        dx, dy = corners[2]

        bax = bx - ax
        bay = by - ay
        dax = dx - ax
        day = dy - ay

        if (item[0] - ax) * bax + (item[1] - ay) * bay < 0.0:  return False
        if (item[0] - bx) * bax + (item[1] - by) * bay > 0.0:  return False
        if (item[0] - ax) * dax + (item[1] - ay) * day < 0.0:  return False
        if (item[0] - dx) * dax + (item[1] - dy) * day > 0.0:  return False

        return True

    def center(self):
        return self.x + (self.vec1[0] + self.vec2[0])/2, self.y + (self.vec1[1] + self.vec2[1])/2

    def valid(self):
        return math.fabs(self.vec1[0] * self.vec2[0] + self.vec1[1] * self.vec2[1]) <= 1e-10

    def rotate(self, theta, is_radians=True, about_center=True):
        if about_center:
            self.rotate_about(theta, is_radians, self.center())
        else:
            self.rotate_about(theta, is_radians, (self.x, self.y))

        if not self.valid():
            print("WARNING: Box2d::rotate() invalid vectors after rotation")
        return self

    def rotate_about(self, theta, is_radians=True, pt=(0, 0)):
        #self.rotate(theta)
        if not is_radians:
            theta *= math.pi / 180

        self.vec1 = [self.vec1[0] * math.cos(theta) - self.vec1[1] * math.sin(theta),
                     self.vec1[0] * math.sin(theta) + self.vec1[1] * math.cos(theta)]
        self.vec2 = [self.vec2[0] * math.cos(theta) - self.vec2[1] * math.sin(theta),
                     self.vec2[0] * math.sin(theta) + self.vec2[1] * math.cos(theta)]
        posvec = [pt[0] - self.x, pt[1] - self.y]
        dx = posvec[0] * math.cos(theta) - posvec[1] * math.sin(theta)
        dy = posvec[0] * math.sin(theta) + posvec[1] * math.cos(theta)
        self.x += posvec[0] - dx
        self.y += posvec[1] - dy
        return self

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

    def clone(self):
        b = Box2d([self.x, self.y], self.vec1, self.vec2)
        b.color = self.color
        return b

    def getcorners(self):
        return [(self.x, self.y),
            (self.x + self.vec1[0], self.y + self.vec1[1]),
            (self.x + self.vec2[0], self.y + self.vec2[1]),
            (self.x + self.vec1[0] + self.vec2[0], self.y + self.vec1[1] + self.vec2[1])]
               #[(self.cx - self.vec1[0] - self.vec2[0], self.cy - self.vec1[1] - self.vec2[1]),
               #(self.cx + self.vec1[0] - self.vec2[0], self.cy + self.vec1[1] - self.vec2[1]),
               # (self.cx + self.vec1[0] + self.vec2[0], self.cy + self.vec1[1] + self.vec2[1]),
               # (self.cx - self.vec1[0] + self.vec2[0], self.cy - self.vec1[1] + self.vec2[1])]

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
        pt = self.x, self.y
        v1 = self.vec1
        v2 = self.vec2
        return "  " + str(self.id) + ": BOX: " + \
               ", ".join(str(x) for x in [pt[0], pt[1], 0,
                                          v1[0], v1[1], 0,
                                          v2[0], v2[1], 0,
                                          0, 0, 1]) + " :: " + self.comment