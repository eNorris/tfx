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

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise Exception("Only elements 0 and 1 and be indexed into for 2-D Point objects")

    def draw2d(self):
        if not graphics or self.visualizer is None:
            return
        pygame.draw.circle(self.visualizer.screen, self.color, [self.x, self.y], 1, 0)

