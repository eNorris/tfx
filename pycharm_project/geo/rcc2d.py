from geo import combinatorialbody

__author__ = 'Edward'

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False
import math
import util
import visualizer.renderable


class Rcc2d(combinatorialbody.CombinatorialBody2d, visualizer.renderable.Renderable):
    def __init__(self, r=1.0, center=(0, 0)):

        try:
            radius = float(r)
        except ValueError as e:
            print(e)
            print("Error, cannot treat a " + r.__class__.__name__ + " as a float value, using zero radius")
            self.r = 0.0
        else:
            self.r = radius
        #if not isinstance(r, float.__class__):
        #    raise TypeError("Rcc2d radius must be of type float (" + r.__class__.__name__ + ")")

        super(Rcc2d, self).__init__()
        self.cx = center[0]
        self.cy = center[1]

        self.comment = "Right Circular Cylinder"

    def __contains__(self, item):
        return math.sqrt((item[0]-self.cx)**2 + (item[1]-self.cy)**2) <= self.r

    #def clone(self):
    #    c = Rcc2d(self.r, [self.cx, self.cy])
    #    c.comment = self.comment
    #    c.visualizer = self.visualizer
    #    return c

    def clone(self, other):
        super(Rcc2d, self).clone(other)
        self.cx, self.cy = other.cx, other.cy
        self.r = other.r

    def rotate_about_2d(self, theta, pt=(0, 0), is_radians=True):
        self.cx, self.cy = util.get_rotated_about_2d([self.cx, self.cy], theta, pt, is_radians)
        return self

    def get_rotated_about_2d(self, theta,  pt=(0, 0), is_radians=True):
        return self.clone().rotate_about_2d(theta, pt, is_radians)

    def get_bounds(self):
        return (self.cx - self.r), (self.cx + self.r), (self.cy - self.r), (self.cy + self.r), 0, 1

    def draw2d(self, screen=None):
        if not graphics or self.visualizer is None:
            return
        centerx = int(self.cx * self.visualizer.scale + self.visualizer.gx)
        centery = int((400 - self.cy * self.visualizer.scale) + self.visualizer.gy)
        radius = int(self.r * self.visualizer.scale)
        if radius >= 2:
            if screen is None:
                pygame.draw.circle(self.visualizer.screen, self.color, [centerx, centery], radius, 1)
            else:
                pygame.draw.circle(screen, self.color, [centerx, centery], radius, 1)

    def __str__(self):
        return "  " + str(self.id) + ": RCC: " + \
               ", ".join(str(x) for x in [self.cx, self.cy, 0, 0, 0, 1, self.r]) + " :: " + self.comment