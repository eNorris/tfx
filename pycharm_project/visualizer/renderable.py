__author__ = 'Edward'

class Renderable(object):

    def __init__(self):
        super(Renderable, self).__init__()
        self.visualizer = None
        self.color = (0, 0, 0)
        self.fillcolor = (0, 0, 0, 0)
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