__author__ = 'Edward'


class CombinatorialBody(object):

    nextid = 1

    def __init__(self):
        self.id = CombinatorialBody.nextid
        CombinatorialBody.nextid += 1
        self.comment = ""
        self.visualizer = None
        self.color = (0, 0, 0)
        self.fillcolor = (0, 0, 0, 0)

    def __contains__(self, item):
        raise Exception("Operator __contains__ not overloaded for this body (" + str(self.__class__.__name__) + ")")

    def clone(self):
        raise Exception("clone() not overloaded for this body (" + str(self.__class__.__name__) + ")")


class CombinatorialBody2d(CombinatorialBody):

    def __init__(self):
        super(CombinatorialBody2d, self).__init__()

    def get_rotated_about_2d(self, theta, about_point, is_radians):
        raise Exception("get_rotated_about_2d() not overloaded for this body (" + str(self.__class__.__name__) + ")")

    def rotate_about_2d(self, theta, about_point, is_radians):
        raise Exception("rotate_about_2d() not overloaded for this body (" + str(self.__class__.__name__) + ")")

