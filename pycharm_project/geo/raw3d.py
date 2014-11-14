__author__ = 'Edward'

import geo.raw2d


class RawZaligned(geo.raw2d.Raw2d):

    def __init__(self, refpoint=(0, 0, 0), v1=(1, 0), v2=(0, 1), height=1.0, comment=None):
        super(RawZaligned, self).__init__((refpoint[0], refpoint[1]), v1, v2, comment)

        self.pz = refpoint[2]
        self.l = height

    def __contains__(self, item):
        return self.pz <= item[2] <= self.pz + self.l and super(RawZaligned, self).__contains__(item)

    def clone(self, other):
        super(RawZaligned, self).clone(other)
        self.pz = other.pz
        self.l = other.l

    def get_bounds(self):
        c = self.get_corners()
        return [min([cc[0] for cc in c]), max([cc[0] for cc in c]),
                min([cc[1] for cc in c]), max([cc[1] for cc in c]),
                self.pz, self.pz + self.l]

    def __str__(self):
        pt = (self.px, self.py, self.pz)
        v1 = self.vec1
        v2 = self.vec2
        return "  " + str(self.id) + ": RAW: " + \
               ", ".join(str(x) for x in [pt[0], pt[1], pt[2],
                                          v1[0], v1[1], 0,
                                          v2[0], v2[1], 0,
                                          0, 0, self.l]) + " :: " + self.comment