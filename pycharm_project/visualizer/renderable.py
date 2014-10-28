__author__ = 'Edward'

import random


class Renderable(object):

    def __init__(self):
        super(Renderable, self).__init__()
        self.visualizer = None
        self.color = (0, 0, 0)
        self.fillcolor = self.rand_hue()
        self.linecolor = (0, 0, 0)

    def clone(self, other):
        self.visualizer = other.visualizer
        self.color = other.color
        self.fillcolor = other.fillcolor
        self.linecolor = other.linecolor

    def get_cloned(self):
        x = Renderable()
        x.clone(self)
        return x

    def rand_color(self):
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255

    def rand_hue(self):
        x = random.randint(0,2)
        c = random.randint(0, 255)
        if x == 0:
            return 0, c, 255-c, 255
        elif x == 1:
            return c, 0, 255-c, 255
        else:
            return 255-c, c, 0, 255