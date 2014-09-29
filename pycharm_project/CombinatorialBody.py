__author__ = 'Edward'


class CombinatorialBody(object):

    nextid = 1

    def __init__(self):
        self.id = CombinatorialBody.nextid
        CombinatorialBody.nextid += 1
        self.comment = ""
        self.visualizer = None
        self.color = (0, 0, 0)

    def __contains__(self, item):
        raise Exception("Operator __contains__ not overloaded for this body (" + str(self.__class__.__name__) + ")")
