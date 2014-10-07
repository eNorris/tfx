from geo import combinatorialbody

__author__ = 'Edward'

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False
import math
import util


class Rcc2d(combinatorialbody.CombinatorialBody2d):
    def __init__(self, r=1, center=(0, 0)):
        super(Rcc2d, self).__init__()
        self.cx = center[0]
        self.cy = center[1]
        self.r = r

        self.comment = "Right Circular Cylinder"

    def __contains__(self, item):
        return math.sqrt((item[0]-self.cx)**2 + (item[1]-self.cy)**2) <= self.r

    def clone(self):
        c = Rcc2d(self.r, [self.cx, self.cy])
        c.comment = self.comment
        c.visualizer = self.visualizer

        return c

    def rotate_about_2d(self, theta, pt=(0, 0), is_radians=True):
        self.cx, self.cy = util.get_rotated_about_2d([self.cx, self.cy], theta, pt, is_radians)
        return self

    def get_rotated_about_2d(self, theta,  pt=(0, 0), is_radians=True):
        return self.clone().rotate_about_2d(theta, pt, is_radians)

    def draw2d(self):
        if not graphics or self.visualizer is None:
            return
        centerx = int(self.cx * self.visualizer.scale + self.visualizer.gx)
        centery = int((400 - self.cy * self.visualizer.scale) + self.visualizer.gy)
        radius = int(self.r * self.visualizer.scale)
        if radius >= 2:
            #pygame.draw.circle(self.visualizer.screen, (150, 150, 150), [centerx, centery], radius, 0)
            pygame.draw.circle(self.visualizer.screen, self.color, [centerx, centery], radius, 2)

    def __str__(self):
        return "  " + str(self.id) + ": RCC: " + \
               ", ".join(str(x) for x in [self.cx, self.cy, 0, 0, 0, 1, self.r]) + " :: " + self.comment