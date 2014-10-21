__author__ = 'Edward'


class Boundary(object):

    def __init__(self, xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, zmin=0.0, zmax=1.0):
        self.xmin, self.xmax = xmin, xmax
        self.ymin, self.ymax = ymin, ymax
        self.zmin, self.zmax = zmin, zmax

    def intersections_polygon2d(self, corners):
        #intersects = []
        intersect_count = 0

        segs = self.build_segments(corners)

        for s in segs:
            if s.intersect_x2d(self.xmin):
                intersect_count += 1
            if intersect_count < 2 and s.intersect_x2d(self.xmax):
                intersect_count += 1
            if intersect_count < 2 and s.intersect_y2d(self.ymin):
                intersect_count += 1
            if intersect_count < 2 and s.intersect_y2d(self.ymax):
                intersect_count += 1
            if intersect_count >= 2:
                break

        return intersect_count >= 2

    def intersections_circle2d(self, cx, cy, r):
        return False

    def build_segments(self, corners):
        segs = []
        for i in range(len(corners)-1):
            segs.append(LineSegment(corners[i], corners[i+1]))
        segs.append(LineSegment(corners[-1], corners[0]))
        return segs

    def __contains__(self, item):
        if len(item) == 2:
            x, y = item[0], item[1]
            return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

        x, y, z = item[0], item[1], item[2]
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax and self.zmin <= z <= self.zmax


class LineSegment(object):

    def __init__(self, pt1, pt2):
        if len(pt1) == 2:
            self.dx, self.dy, self.dz = pt2[0]-pt1[0], pt2[1]-pt1[1], 0
        else:
            self.dx, self.dy, self.dz = pt2[0]-pt1[0], pt2[1]-pt1[1], pt2[2]-pt1[2]

        self.p = pt1

    def intersect_x2d(self, x):
        if self.dx < 1e-10:
            return self.p[0] - x < 1e-10

        t = (x - self.p[0])/self.dx
        return 0 <= t <= 1

    def intersect_y2d(self, y):
        if self.dy < 1e-10:
            return self.p[1] - y < 1e-10

        t = (y - self.p[1])/self.dy
        return 0 <= t <= 1