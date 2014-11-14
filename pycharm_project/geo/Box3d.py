__author__ = 'Edward'

import geo.box2d


class BoxZaligned(geo.box2d.Box2d):

    def __init__(self, pos=(0, 0, 0), vec1=(1, 0), vec2=(0, 1), height=1.0, provide_center=True, comment=None):
        super(BoxZaligned, self).__init__((pos[0], pos[1]), vec1, vec2, provide_center, comment)

        if provide_center:
            self.z = pos[2] - height/2
        else:
            self.z = pos[2]

        self.l = height

    def __contains__(self, item):
        return self.z <= item[2] <= self.z + self.l and super(BoxZaligned, self).__contains__(item)

    def clone(self, other):
        super(BoxZaligned, self).clone(other)
        self.z = other.z
        self.l = other.l

    def get_bounds(self):
        c = self.get_corners()
        return [min([cc[0] for cc in c]), max([cc[0] for cc in c]),
               min([cc[1] for cc in c]), max([cc[1] for cc in c]),
               self.z, self.z + self.l]

    def __str__(self):
        pt = self.x, self.y, self.z
        v1 = self.vec1
        v2 = self.vec2
        return "  " + str(self.id) + ": BOX: " + \
               ", ".join(str(x) for x in [pt[0], pt[1], pt[2],
                                          v1[0], v1[1], 0,
                                          v2[0], v2[1], 0,
                                          0, 0, self.l]) + " :: " + self.comment