__author__ = 'Edward'

class CombinatorialBody:

    nextid = 1

    def __init__(self):
        self.id = CombinatorialBody.nextid
        CombinatorialBody.nextid += 1
        self.comment = ""
        self.visualizer = None
