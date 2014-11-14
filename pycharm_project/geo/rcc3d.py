__author__ = 'Edward'

import math
import geo.rcc2d


class RccZaligned(geo.rcc2d.Rcc2d):

    def __init__(self, r=1.0, length=1.0, center=(0, 0, 0), comment=None):
        super(RccZaligned, self).__init__(r, center, comment)
        self.cz = center[2]
        self.l = length
        
    def __contains__(self, item):
        return math.sqrt((item[0]-self.cx)**2 + (item[1]-self.cy)**2) <= self.r and abs(item[2] - self.cz) <= self.l/2

    def clone(self, other):
        super(RccZaligned, self).clone(other)
        self.cz = other.cz
        self.l = other.l

    def get_bounds(self):
        return [self.cx - self.r, self.cx + self.r,
                self.cy - self.r, self.cy + self.r,
                self.cz - self.l/2, self.cz + self.l/2]

    def __str__(self):
        return "  " + str(self.id) + ": RCC: " + \
               ", ".join(str(x) for x in [self.cx, self.cy, self.cz-self.l/2,
                                          0, 0, self.l,
                                          self.r]) + " :: " + self.comment