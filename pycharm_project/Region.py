__author__ = 'Edward'

import copy


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
        self.evalpoint = (0, 0, 0)

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

    def __str__(self):
        return "  " + str(self.id) + ": " + self.matid + ": " + self.str_rec() + ": " + self.comment

    def clone(self):
        c = RegionNode(self.left, self.type, self.right)
        c.matid = self.matid
        c.comment = self.comment
        return c

    def clonedeep(self):
        c = RegionNode(self.left, self.type, self.right)
        c.matid = self.matid
        c.comment = self.comment
        c.id = self.id
        RegionNode.nextid -= 1
        return c

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
