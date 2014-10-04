__author__ = 'Edward'

import util

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False


class Region:

    UNION = 0
    INTERSECT = 1
    SUBTRACT = 2
    BASE = 3

    OPERATORS = [UNION, INTERSECT, SUBTRACT, BASE]

    nextid = 1

    def __init__(self, left=None, itype=None, right=None):
        # self.up = None
        self.left = left
        self.type = itype
        self.right = right
        self.matid = "X"
        self.id = Region.nextid
        Region.nextid += 1
        self.comment = ""
        self.doeval = False
        self.drawevals = False
        self.evalpoints = []
        self.visualizer = None

        if left is None:
            return

        if right is None:
            if isinstance(left, Region):
                print("WARNING: region.py::RegionNode::init(): Useless node detected")
            #if isinstance(left, Region):
            #    self.left = left.node
            else:
                self.left = left
            self.type = Region.BASE

        if itype is not None and itype not in Region.OPERATORS:
            print("WARNING: unknown type")

        if itype is not None and itype is not Region.BASE and right is None:
            print("WARNING: type is specified by no right side is provided")

        if itype is None and right is not None:
            print("WARNING: type is not specified by two regions were specified")

    # TODO - Think about how union, get_unioned, | and |= should all work together
    def union(self, other):
        if not isinstance(other, Region):
            other = Region(other)
        return Region(self, Region.UNION, other)

    def intersect(self, other):
        if not isinstance(other, Region):
            other = Region(other)
        return Region(self, Region.INTERSECT, other)

    def subtract(self, other):
        if not isinstance(other, Region):
            other = Region(other)
        return Region(self, Region.SUBTRACT, other)

    def __add__(self, other):
        return self.intersect(other)

    def __iadd__(self, other):
        if not isinstance(other, Region):
            other = Region(other)
        self.left = self.clonedeep()
        #self.left = copy.deepcopy(self)
        self.type = Region.INTERSECT
        self.right = other
        return self

    def __sub__(self, other):
        return self.subtract(other)

    def __isub__(self, other):
        if not isinstance(other, Region):
            other = Region(other)
        self.left = self.clonedeep()
        #self.left = copy.deepcopy(self)
        self.type = Region.SUBTRACT
        self.right = other
        return self

    def __or__(self, other):
        return self.union(other)

    def __ior__(self, other):
        if not isinstance(other, Region):
            other = Region(other)
        self.left = self.clonedeep()
        #self.left = copy.deepcopy(self)
        self.type = Region.UNION
        self.right = other
        return self

    def __contains__(self, item):
        if self.type == Region.BASE:
            return item in self.left
        elif self.type == Region.INTERSECT:
            return item in self.left and item in self.right
        elif self.type == Region.UNION:
            return item in self.left or item in self.right
        elif self.type == Region.SUBTRACT:
            return item in self.left and not item in self.right
        else:
            raise Exception("Unknown region combination type: " + str(self.type))

    def __str__(self):
        return "  " + str(self.id) + ": " + self.matid + ": " + self.str_rec() + ": " + self.comment

    def clone(self):

        if self.type == Region.BASE:
            x = Region(self.left.clone(), self.type, None)
        else:
            x = Region(self.left.clone(), self.type, self.right.clone())

        x.matid = self.matid
        x.comment = self.comment
        x.doeval = self.doeval
        x.drawevals = self.drawevals
        x.evalpoints = [k for k in self.evalpoints]
        x.visualizer = self.visualizer

        return x

    def clonedeep(self):
        c = Region(self.left, self.type, self.right)
        c.matid = self.matid
        c.comment = self.comment
        c.id = self.id
        Region.nextid -= 1
        return c

    def get_rotated_about_2d(self, theta, aboutpt=(0, 0), is_radians=True):
        x = self.clone()
        return x.rotate_about_2d(theta, aboutpt, is_radians)

    def rotate_about_2d(self, theta, aboutpt=(0, 0), is_radians=True):
        if self.type == Region.BASE:
            self.left.rotate_about_2d(theta, aboutpt, is_radians)
        else:
            self.left.rotate_about_2d(theta, aboutpt, is_radians)
            self.right.rotate_about_2d(theta, aboutpt, is_radians)

        self.evalpoints = [util.get_rotated_about_2d(x, theta, aboutpt, is_radians) for x in self.evalpoints]

        return self

    def get_all_bodies(self):
        if self.type == Region.BASE:
            return {[self.left]}
        else:
            return self.left.get_all_bodies() | (self.right.get_all_bodies())

    #def evalpt(self):
    #    return (0, 0, 0)

    def str_rec(self):
        if self.type == Region.BASE:
            return str(self.left.id)
        if self.type == Region.UNION:
            return self.left.str_rec() + "|" + self.right.str_rec()
        if self.type == Region.INTERSECT:
            return self.left.str_rec() + "+" + self.right.str_rec()
        if self.type == Region.SUBTRACT:
            return self.left.str_rec() + "-" + self.right.str_rec()

    def draw2d(self):
        if not graphics or self.visualizer is None:
            return

        # TODO - Need to fix this
        # if self.type == RegionNode.BASE:
        #     self.left.draw2d()
        # else:
        #     self.left.draw2d()
        #     self.right.draw2d()

        if self.drawevals:
            for e in self.evalpoints:
                sx = int(e[0] * self.visualizer.scale + self.visualizer.gx)
                sy = int((400 - e[1] * self.visualizer.scale) + self.visualizer.gy)
                pygame.draw.circle(self.visualizer.screen, (255, 0, 255), [sx, sy], 3, 0)
