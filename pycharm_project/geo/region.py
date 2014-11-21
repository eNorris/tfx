__author__ = 'Edward'

import util

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False

import visualizer.renderable


class GhostRegion(object):
    def __init__(self):
        self.type = -1
        self.left = self.right = None

class Region(visualizer.renderable.Renderable):

    UNION = 0
    INTERSECT = 1
    SUBTRACT = 2
    BASE = 3

    OPERATORS = [UNION, INTERSECT, SUBTRACT, BASE]

    nextid = 1

    def __init__(self, left=None, itype=None, right=None):

        super(Region, self).__init__()

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

        # If there is no data to add, do nothing further
        if left is None:
            return

        if right is None:
            if isinstance(left, Region):
                print("WARNING: region.py::Region::init(): Useless node detected")
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
        return "  " + str(self.id) + ": " + self.matid + ": " + self.str_transware() + ": " + self.comment

    def clone(self, other):

        raise Exception("Region cloning logic  hangs sometimes for no reason. So fix it or don't use it.")

        #print("cloning... id = " + str(other.id) + ", type = " + str(other.__class__.__name__))
        #
        #k = other.id
        #
        #left = other.left
        #right = other.right
        #
        #if other.type == Region.BASE:
        #    self.left = left.__class__()  #Region()
        #    self.left.clone(left)
        #else:
        #    self.left = Region()
        #    self.right = Region()
        #    self.left.clone(left)
        #    self.right.clone(right)
        #
        #self.type = other.type
        #self.matid = other.matid
        #self.comment = other.comment
        #self.doeval = other.doeval
        #self.drawevals = other.drawevals
        #self.evalpoints = [x for x in other.evalpoints]


    def clonedeep(self):
        c = Region(self.left, self.type, self.right)
        c.matid = self.matid
        c.comment = self.comment
        c.id = self.id
        Region.nextid -= 1
        return c

    def ghostcopy(self):
        r = GhostRegion()
        r.type = self.type
        if r.type == Region.BASE:
            r.left = self.left
        else:
            r.left = self.left.ghostcopy()
            r.right = self.right.ghostcopy()
        return r

    def get_rotated_about_2d(self, theta, aboutpt=(0, 0), is_radians=True):
        x = Region()
        x.clone(self)
        return x.rotate_about_2d(theta, aboutpt, is_radians)

    def rotate_about_2d(self, theta, aboutpt=(0, 0), is_radians=True):
        #print("region.py::rotate_about_2d() [186]: rotating...")
        if self.type == Region.BASE:
            #print("base")
            print(self.left.__class__.__name__)
            self.left.rotate_about_2d(theta, aboutpt, is_radians)
            #print("returned from recursion")
        else:
            #print("branch")
            self.left.rotate_about_2d(theta, aboutpt, is_radians)
            self.right.rotate_about_2d(theta, aboutpt, is_radians)

        self.evalpoints = [util.get_rotated_about_2d(x, theta, aboutpt, is_radians) for x in self.evalpoints]
        #print("Going up...")

        return self

    def get_all_bodies(self):
        if self.type == Region.BASE:
            return set([self.left])
        else:
            return self.left.get_all_bodies() | (self.right.get_all_bodies())


    def get_bounds_old(self):
        bodies = self.get_all_bodies()
        bounds = bodies.pop().get_bounds()

        for b in bodies:
            newbounds = b.get_bounds()
            bounds[0] = min(newbounds[0], bounds[0])  # xmin
            bounds[1] = max(newbounds[1], bounds[1])  # xmax
            bounds[2] = min(newbounds[2], bounds[2])  # ymin
            bounds[3] = max(newbounds[3], bounds[3])  # ymax
            bounds[4] = min(newbounds[4], bounds[4])  # zmin
            bounds[5] = max(newbounds[5], bounds[5])  # zmax

        return bounds

    def get_bounds(self):
        if self.type == Region.BASE:
            return self.left.get_bounds()

        lxmin, lxmax, lymin, lymax, lzmin, lzmax = self.left.get_bounds()
        rxmin, rxmax, rymin, rymax, rzmin, rzmax = self.right.get_bounds()

        if self.type == Region.INTERSECT:
            #return [max(lxmin, rxmin), min(lxmax, rxmax),
            return [max(lxmin, rxmin), min(lxmax, rxmax),
                    max(lymin, rymin), min(lymax, rymax),
                    max(lzmin, rzmin), min(lzmax, rzmax)]
        elif self.type == Region.SUBTRACT:
            return [lxmin, lxmax,
                    lymin, lymax,
                    lzmin, lzmax]
        elif self.type == Region.UNION:
            return [min(lxmin, rxmin), max(lxmax, rxmax),
                    min(lymin, rymin), max(lymax, rymax),
                    min(lzmin, rzmin), max(lzmax, rzmax),]
        else:
            raise Exception("Region::get_bounds(): unknown type")

    def str_rec(self, parens=False):
        if parens:
            if self.type == Region.BASE:
                return str(self.left.id)
            if self.type == Region.UNION:
                return "(" + self.left.str_rec(parens) + "|" + self.right.str_rec(parens) + ")"
            if self.type == Region.INTERSECT:
                return "(" + self.left.str_rec(parens) + "+" + self.right.str_rec(parens) + ")"
            if self.type == Region.SUBTRACT:
                return "(" + self.left.str_rec(parens) + "-" + self.right.str_rec(parens) + ")"
        else:
            if self.type == Region.BASE:
                return str(self.left.id)
            if self.type == Region.UNION:
                return self.left.str_rec() + "|" + self.right.str_rec()
            if self.type == Region.INTERSECT:
                return self.left.str_rec() + "+" + self.right.str_rec()
            if self.type == Region.SUBTRACT:
                return self.left.str_rec() + "-" + self.right.str_rec()

    def str_transware(self):
        if not self.is_left_adjusted():
            self.left_adjust()
        if self.type == Region.BASE:
            return str(self.left.id)
        if self.type == Region.UNION:
            return self.left.str_rec() + "|" + self.right.str_rec()
        if self.type == Region.INTERSECT:
            return self.left.str_rec() + "+" + self.right.str_rec()
        if self.type == Region.SUBTRACT:
            return self.left.str_rec() + "-" + self.right.str_rec()


    def draw2d(self, surf=None):
        if not graphics or self.visualizer is None:
            return

        raise Exception("This function is no longer used.")

    def is_left_adjustable(self):

        # If the left isn't adjustable, the whole tree isn't
        if self.left is not None:
            if self.left.type != Region.BASE:
                if not self.left.is_left_adjustable():
                    return False

        # Same for the right
        if self.right is not None:
            if self.right.type != Region.BASE:
                if not self.right.is_left_adjustable():
                    return False

        # The only way _this_ node cannot be adjustable is if it is a subtraction operator and there is a
        # intersection or subtraction on the right
        if self.type == Region.SUBTRACT:
            return self.right.is_left_adjustable_safe()

        return True

    def is_left_adjustable_safe(self):
        # Look left and loo right
        if self.left is not None and self.left.type != Region.BASE:
            if not self.left.is_left_adjustable_safe():
                return False
        if self.right is not None and self.right.type != Region.BASE:
            if not self.right.is_left_adjustable_safe():
                return False

        # This node is only safe it it is either a base node or a union node
        if self.type != Region.BASE and self.type != Region.UNION:
            return False

        return True

    def is_left_adjusted(self):
        if self.right is not None and self.right.type != Region.BASE:
            return False

        if self.left is not None and isinstance(self.left, Region):
            return self.left.is_left_adjusted()

        return True

    def left_adjust(self):

        print("I don't know how to left adjust!" + self.str_rec(True))
