from geo import combinatorialbody

__author__ = 'Edward'

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False

import visualizer.renderable


class Rpp2d(combinatorialbody.CombinatorialBody2d, visualizer.renderable.Renderable):
    def __init__(self, loc=(0, 0), dims=(1, 1), provide_center=True):
        super(Rpp2d, self).__init__()
        self.w = dims[0]
        self.h = dims[1]
        if provide_center:
            self.cx = loc[0]
            self.cy = loc[1]
            self.left = self.cx - self.w / 2.0
            self.right = self.cx + self.w / 2.0
            self.top = self.cy + self.h / 2.0
            self.bottom = self.cy - self.h / 2.0
        else:
            self.left = loc[0]
            self.bottom = loc[1]
            self.cx = self.left + self.w / 2.0
            self.cy = self.bottom + self.h / 2.0
            self.right = self.left + self.w
            self.top = self.bottom + self.h
        self.color = (0, 0, 0)

        self.comment = "Axis-aligned Right Parallelpiped"

    def clone_down(self):
        r = Rpp2d([self.cx, self.cy - self.h], [self.w, self.h])
        r.color = self.color
        return r

    def clone_up(self):
        r = Rpp2d([self.cx, self.cy + self.h], [self.w, self.h])
        r.color = self.color
        return r

    def clone_right(self):
        r = Rpp2d([self.cx + self.w, self.cy], [self.w, self.h])
        r.color = self.color
        return r

    def clone_left(self):
        r = Rpp2d([self.cx - self.w, self.cy], [self.w, self.h])
        r.color = self.color
        return r

    def get_corners(self):
        return [(self.cx - self.w/2, self.cy - self.h/2),
                (self.cx + self.w/2, self.cy - self.h/2),
                (self.cx + self.w/2, self.cy + self.h/2),
                (self.cx - self.w/2, self.cy + self.h/2)]

    def get_edges(self):
        return self.cx + self.w/2, self.cy + self.h/2, self.cx - self.w/2, self.cy - self.h/2

    def set_center(self, pt):
        self.cx = pt[0]
        self.cy = pt[1]
        self.left = self.cx - self.w / 2.0
        self.right = self.cx + self.w / 2.0
        self.top = self.cy + self.h / 2.0
        self.bottom = self.cy - self.h / 2.0

    def set_dims(self, dims, preserve_center=True):
        self.w = dims[0]
        self.h = dims[1]
        if preserve_center:
            self.left = self.cx - self.w / 2
            self.top = self.cy + self.h / 2
            self.right = self.cx + self.w / 2
            self.bottom = self.cy - self.h / 2
        else:
            self.cx = self.left + self.w / 2
            self.cy = self.bottom + self.h / 2
            self.right = self.left + self.w
            self.top = self.bottom + self.h

    def draw2d(self):
        if not graphics or self.visualizer is None:
            return
        left = int(self.left * self.visualizer.scale + self.visualizer.gx)
        top = int(400 - self.top * self.visualizer.scale + self.visualizer.gy)
        width = int(self.w * self.visualizer.scale)
        height = int(self.h * self.visualizer.scale)

        if self.fillcolor[3] != 0:
            pygame.draw.rect(self.visualizer.screen, self.fillcolor,
                             [left, top, width, height], 0)
        pygame.draw.rect(self.visualizer.screen, self.color,
                         [left, top, width, height], 1)

    def __contains__(self, pt):
        if self.left <= pt[0] <= self.right and self.bottom <= pt[1] <= self.top:
            return True
        return False

    #def evalpt(self):
    #    return (self.cx, self.cy, 0.5)

    def __str__(self):
        return "  " + str(self.id) + ": RPP: " + \
               ", ".join(str(x) for x in [self.left, self.right, self.bottom, self.top, 0, 1]) + " :: " + self.comment