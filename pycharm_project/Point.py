__author__ = 'Edward'

# THIS CLASS IS NO LONGER USED

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False


class Point2d:

    def __init__(self, pos=(0, 0), color=(0, 0, 0)):
        self.x, self.y = pos
        self.visualizer = None
        self.color = color
        self.dodraw = False
        self.radius = 1

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise Exception("Only elements 0 and 1 and be indexed into for 2-D Point objects")

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def clone(self):
        p = Point2d([self.x, self.y], self.color)
        p.visualizer = self.visualizer
        p.dodraw = self.dodraw
        p.radius = self.radius
        return p

    def draw2d(self):
        if not self.dodraw or not graphics or self.visualizer is None:
            return
        sx = int(self.x * self.visualizer.scale + self.visualizer.gx)
        sy = int((400 - self.y * self.visualizer.scale) + self.visualizer.gy)
        pygame.draw.circle(self.visualizer.screen, self.color, [sx, sy], self.radius, 0)

