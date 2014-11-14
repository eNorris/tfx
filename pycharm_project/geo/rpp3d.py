__author__ = 'Edward'

import geo.rpp2d


class RppZaligned(geo.rpp2d.Rpp2d):

    def __init__(self, loc=(0, 0, 0), dims=(1, 1, 1), provide_center=True, comment=None):

        super(RppZaligned, self).__init__((loc[0], loc[1]), (dims[0], dims[1]), provide_center, comment)

        self.l = dims[2]

        if provide_center:
            self.cz = loc[2]
            self.zmin = loc[2] - dims[2]/2
            self.zmax = loc[2] + dims[2]/2
        else:
            self.zmin = loc[2]
            self.zmax = loc[2] + dims[2]
            self.cz = (self.zmin + self.zmax)/2

    def clone(self, other):
        super(RppZaligned, self).clone(other)
        self.cz = other.cz
        self.l = other.left
        self.zmin, self.zmax = other.zmin, other.zmax

    def get_bounds(self):
        return [self.left, self.right, self.bottom, self.top, self.zmin, self.zmax]

    def __contains__(self, pt):
        return self.zmin <= pt[2] <= self.zmax and super(RppZaligned, self).__contains__(pt)

    def __str__(self):
        return "  " + str(self.id) + ": RPP: " + \
               ", ".join(str(x) for x in [self.left, self.right, self.bottom, self.top, self.zmin, self.zmax]) + \
               " :: " + self.comment