import numpy

class Queue:
    def __init__(self):
        self.length = 0
        self.attributes = []
    def insert(self, item):
        self.attributes.insert(0,item)
    def remove(self):
        if self.attributes == []:
            print "The queue is empty"
        else:
            print self.attributes.pop()


class Board(object):
    def __init__(self, wid_heigh):
        self.height = wid_heigh
        self.width = wid_heigh

        self.tiles = numpy.zeros(shape=(wid_heigh, wid_heigh))

    def isTileEmpty(self, m, n):
        if self.tiles[m,n] == 0:
            return True
        else:
            return False






