__author__ = 'Edward'

class Renderable(object):

    def __init__(self):
        super(Renderable, self).__init__()
        self.visualizer = None
        self.color = (0, 0, 0)
        self.fillcolor = (0, 0, 0, 0)
        self.linecolor = (0, 0, 0)

    def clone(self):
        x = Renderable()
        x.visualizer = self.visualizer
        x.color = self.color
        x.fillcolor = self.fillcolor
        x.linecolor = self.linecolor
        return x