__author__ = 'Edward'

import util

class RegionNode:

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
        self.id = RegionNode.nextid
        RegionNode.nextid += 1
        self.comment = ""
        self.doeval = False
        self.evalpoints = []

        if left is None:
            return

        if right is None:
            if isinstance(left, RegionNode):
                print("WARNING: Region.py::RegionNode::init(): Useless node detected")
            #if isinstance(left, Region):
            #    self.left = left.node
            else:
                self.left = left
            self.type = RegionNode.BASE

        if itype is not None and itype not in RegionNode.OPERATORS:
            print("WARNING: unknown type")

        if itype is not None and itype is not RegionNode.BASE and right is None:
            print("WARNING: type is specified by no right side is provided")

        if itype is None and right is not None:
            print("WARNING: type is not specified by two regions were specified")

    def union(self, other):
        if not isinstance(other, RegionNode):
            other = RegionNode(other)
        return RegionNode(self, RegionNode.UNION, other)

    def intersect(self, other):
        if not isinstance(other, RegionNode):
            other = RegionNode(other)
        return RegionNode(self, RegionNode.INTERSECT, other)

    def subtract(self, other):
        if not isinstance(other, RegionNode):
            other = RegionNode(other)
        return RegionNode(self, RegionNode.SUBTRACT, other)

    def __add__(self, other):
        return self.intersect(other)

    def __iadd__(self, other):
        if not isinstance(other, RegionNode):
            other = RegionNode(other)
        self.left = self.clonedeep()
        #self.left = copy.deepcopy(self)
        self.type = RegionNode.INTERSECT
        self.right = other
        return self

    def __sub__(self, other):
        return self.subtract(other)

    def __isub__(self, other):
        if not isinstance(other, RegionNode):
            other = RegionNode(other)
        self.left = self.clonedeep()
        #self.left = copy.deepcopy(self)
        self.type = RegionNode.SUBTRACT
        self.right = other
        return self

    def __or__(self, other):
        return self.union(other)

    def __ior__(self, other):
        if not isinstance(other, RegionNode):
            other = RegionNode(other)
        self.left = self.clonedeep()
        #self.left = copy.deepcopy(self)
        self.type = RegionNode.UNION
        self.right = other
        return self

    def __contains__(self, item):
        if self.type == RegionNode.BASE:
            return item in self.left
        elif self.type == RegionNode.INTERSECT:
            return item in self.left and item in self.right
        elif self.type == RegionNode.UNION:
            return item in self.left or item in self.right
        elif self.type == RegionNode.SUBTRACT:
            return item in self.left and not item in self.right
        else:
            raise Exception("Unknown region combination type: " + str(self.type))

    def __str__(self):
        return "  " + str(self.id) + ": " + self.matid + ": " + self.str_rec() + ": " + self.comment

    def clone(self):

        if self.type == RegionNode.BASE:
            x = RegionNode(self.left.clone(), self.type, None)
        else:
            x = RegionNode(self.left.clone(), self.type, self.right.clone())

        x.matid = self.matid
        x.comment = self.comment
        x.doeval = self.doeval
        self.evalpoints = [k for k in self.evalpoints]

        return x

    def clonedeep(self):
        c = RegionNode(self.left, self.type, self.right)
        c.matid = self.matid
        c.comment = self.comment
        c.id = self.id
        RegionNode.nextid -= 1
        return c

    def get_rotated_about_2d(self, theta, aboutpt=(0, 0), is_radians=True):
        x = self.clone()
        return x.rotate_about_2d(theta, aboutpt, is_radians)

    def rotate_about_2d(self, theta, aboutpt=(0, 0), is_radians=True):
        if self.type == RegionNode.BASE:
            self.left.rotate_about(theta, aboutpt, is_radians)
        else:
            self.right.rotate_about(theta, aboutpt, is_radians)
            self.right.rotate_about(theta, aboutpt, is_radians)

        self.evalpoints = [util.get_rotated_about_2d(x, theta, aboutpt, is_radians) for x in self.evalpoints]

        return self

    def get_all_bodies(self):
        if self.type == RegionNode.BASE:
            return set([self.left])
        else:
            return self.left.get_all_bodies() | (self.right.get_all_bodies())

    #def evalpt(self):
    #    return (0, 0, 0)

    def str_rec(self):
        if self.type == RegionNode.BASE:
            return str(self.left.id)
        if self.type == RegionNode.UNION:
            return self.left.str_rec() + "|" + self.right.str_rec()
        if self.type == RegionNode.INTERSECT:
            return self.left.str_rec() + "+" + self.right.str_rec()
        if self.type == RegionNode.SUBTRACT:
            return self.left.str_rec() + "-" + self.right.str_rec()


class Region:

    nextid = 1

    def __init__(self, left, itype=None, right=None):
        #self.left = left
        #self.type = type
        #self.right = right
        self.node = None
        self.matid = "X"
        self.id = -1
        self.comment = ""

        if left is None:
            return

        if itype is None:
            self.node = RegionNode(left)
        else:
            self.node = RegionNode(left, itype, right)

    def realize(self):
        self.id = Region.nextid
        Region.nextid += 1

    def union(self, other):
        return Region(self, RegionNode.UNION, other)

    def intersect(self, other):
        return Region(self, RegionNode.INTERSECT, other)

    def subtract(self, other):
        return RegionNode(self, RegionNode.SUBTRACT, other)

    def __add__(self, other):
        return self.intersect(other)

    def __iadd__(self, other):
        self.node = Region(self).intersect(other).node
        return self

    def __sub__(self, other):
        return self.subtract(other)

    def __isub__(self, other):
        #self.left = copy.deepcopy(self)
        #self.type = RegionNode.SUBTRACT
        #self.right = other
        return self

    def __or__(self, other):
        return self.union(other)

    def __ior__(self, other):
        #self.left = copy.deepcopy(self)
        #self.type = RegionNode.UNION
        #self.right = other
        return self

    def __str__(self):
        print("  " + str() + ": " + self.matid + ": " + str(self.node) + ": " + self.comment)
