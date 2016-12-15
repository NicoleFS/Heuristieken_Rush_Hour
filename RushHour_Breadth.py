# Rush Hour
# Names (student id): Nicol Heijtbrink (10580611), Nicole Silverio (10521933) & Sander de Wijs (10582134)
# Course: Heuristieken
# University of Amsterdam
# Time: November-December, 2016
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import visualize_rush_lepps
import pylab
import math
import Queue as QueueClass
import copy
class Car(object):
    """
    A Car represents an object with length 2 or 3 and a certain orientation (horizontal or vertical),
    which can move around the board.
    """
    def __init__(self, x, y, length, orientation, id):
        """
        Initializes a car with a position with coordinates [x, y] on a board with a given length,
        orientation and id.
        :param x, y, length, orientation, id: All parameters are defined in a separate list.
        """
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = length
        self.id = id
class Game(object):
    """
    A Game represents a board (grid), on which Car objects can move around on.
    The grid is a 2D array of 0's and has a width and length (given by dimension parameter).
    A 0 indicates that position to be empty, while any non-zero value indicates the
    presence of a Car object (where the number indicates which Car).
    """
    def __init__(self, dimension, cars):
        """
        Initializes the given grid and creates an empty array, to be filled with Car objects.
        :param playboard: The given empty grid.
        """
        self.dimension = dimension
        self.grid = np.zeros(shape=(dimension, dimension), dtype=np.int)
        self.cars = cars
        for car in self.cars:
            self.addCarToGrid(car)
        self.gridQueue = QueueClass.Queue(maxsize=0)
        self.carsQueue = QueueClass.Queue(maxsize=0)
        self.gridQueue.put(self.grid.copy())
        self.carsQueue.put(self.cars)
        # create set to store board states
        self.stateSet = set()
        # create list to store single board state
        self.stateList = []
        self.path = {}
        self.children = {}
        start = self.gridToString()
        self.moves = {}
        self.moves[start] = 0
    def addCarToGrid(self, car):
        """
        Fill the board with a given car.
        Checks orientation and starting coordinates of car,
        then fills in the rest according to the given length.
        :param car: object with given x, y, length, orientation and idcar
        :return: a filled grid.
        """
        x = car.x
        y = car.y
        # first check orientation of car
        if car.orientation == "H":
            # then replace 0 with idcar integer for length of car
            for i in range(0, car.length):
                if self.grid[x, y] == 0:
                    self.grid[x, y] = car.id
                    x += 1
                else:
                    print "Error, car cannot be placed on a tile that contains another car"
        elif car.orientation == "V":
            for i in range(0, car.length):
                if self.grid[x, y] == 0:
                    self.grid[x, y] = car.id
                    y += 1
                else:
                    print "Error, car cannot be placed on a tile that contains another car"
                    # return self.grid
    def canMoveRight(self, car):
        if car.orientation == "V":
            return False
        if car.x < (self.dimension - car.length):
            if self.grid[car.x + car.length, car.y] == 0:
                return True
        return False
    def canMoveLeft(self, car):
        if car.orientation == "V":
            return False
        if car.x > 0:
            if self.grid[car.x - 1, car.y] == 0:
                return True
        return False
    def canMoveUp(self, car):
        if car.orientation == "H":
            return False
        if car.y > 0:
            if self.grid[car.x, car.y - 1] == 0:
                return True
        return False
    def canMoveDown(self, car):
        if car.orientation == "H":
            return False
        if car.y < (self.dimension - car.length):
            if self.grid[car.x, car.y + car.length] == 0:
                return True
        return False
    def moveRight(self, carId):
        """
        'Moves' a given car 1 place to the right on the grid.
        Replaces the 0 on the right side next to the car with integer idcar
        and replaces the left side of the car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """
        car = self.cars[carId.id - 1]
        # replace right side next to the car with integer idcar
        self.grid[car.x + car.length, car.y] = car.id
        # replace the left side of the car with a 0 (empty)
        self.grid[car.x, car.y] = 0
        # update x coordinate
        car.x = car.x + 1
        self.cars[car.id - 1] = car
        # add 1 (move) to counter moves
        # self.moves += 1
    def moveLeft(self, carId):
        """
        'Moves' a given car 1 place to the left on the grid.
        Replaces the 0 on the left side next to the car with integer idcar
        and replaces the right side of the car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """
        car = self.cars[carId.id - 1]
        # replace left side next to the car with integer idcar
        self.grid[car.x - 1, car.y] = car.id
        # replace the right side of the car with a 0 (empty)
        self.grid[car.x + (car.length - 1), car.y] = 0
        # update x coordinate
        car.x = car.x - 1
        self.cars[car.id - 1] = car
        # add 1 (move) to counter moves
        # self.moves += 1
    def moveDown(self, carId):
        """
        'Moves' a given car 1 place down on the grid.
        Replaces the 0 one place underneath the car with integer idcar
        and replaces the top of the car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """
        car = self.cars[carId.id - 1]
        # replace one place underneath the car with integer idcar
        self.grid[car.x, car.y + car.length] = car.id
        # replace the top of the car with a 0 (empty)
        self.grid[car.x, car.y] = 0
        # update y coordinate
        car.y = car.y + 1
        self.cars[car.id - 1] = car
    def moveUp(self, carId):
        """
        'Moves' a given car 1 place up on the grid.
        Replaces the 0 one place above the car with integer idcar
        and replaces the bottom of the car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """
        car = self.cars[carId.id - 1]
        # replace one place above the car with integer idcar
        self.grid[car.x, car.y - 1] = car.id
        # replace the bottom of the car with a 0 (empty)
        self.grid[car.x, car.y + (car.length - 1)] = 0
        # update y coordinate
        car.y = car.y - 1
        self.cars[car.id - 1] = car
    def putinQueue(self):
        self.gridQueue.put(self.grid.copy())
        self.carsQueue.put(copy.deepcopy(self.cars))
    def gridToString(self):
        hash = ""
        for i in range(len(self.grid.T)):
            for j in range(len(self.grid[i])):
                hash += str(self.grid[i][j])
        return hash
    def checkMove(self):
        """Checks if a move can be made by trying to put in a set. If the length of the set does not change it means
        there is a duplicate. Retruns the length of the set after trying to put the board state in the set"""
        gridString = self.gridToString()
        self.stateSet.add(gridString)
        return len(self.stateSet)
    # def setNewParent(self):
    #     """
    #
    #     :return:
    #     """
    #     parentString = self.gridToString()
    #     childString = self.gridToString()
    #     self.children[parentString] = childString
    #     self.path[childString] = parentString
    #     self.putinQueue()
    #     self.moves[childString] = 1 + self.moves[parentString]
    def queueAllPossibleMoves(self):
        """
        For every car all directions are checked. If a car can move in a certain direction it is checked if it is
        already in the archive, if so the move is undone. If it a new unique board state after a move the cars and the
        grid are put in queues and the move is undone to be able to check the opposite direction
        """
        parentString = self.gridToString()
        for car in self.cars:
            if self.canMoveUp(car):
                a = Game.checkMove(self)
                self.moveUp(car)
                b = Game.checkMove(self)
                if a != b:
                    #self.setNewParent()
                    childString = self.gridToString()
                    self.children[parentString] = childString
                    self.path[childString] = parentString
                    self.putinQueue()
                    self.moves[childString] = 1 + self.moves[parentString]
                self.moveDown(car)
            if self.canMoveDown(car):
                a = Game.checkMove(self)
                self.moveDown(car)
                b = Game.checkMove(self)
                if a != b:
                    #self.setNewParent()
                    childString = self.gridToString()
                    self.children[parentString] = childString
                    self.path[childString] = parentString
                    self.putinQueue()
                    self.moves[childString] = 1 + self.moves[parentString]
                self.moveUp(car)
            if self.canMoveRight(car):
                a = Game.checkMove(self)
                self.moveRight(car)
                b = Game.checkMove(self)
                if a != b:
                    #self.setNewParent()
                    childString = self.gridToString()
                    self.children[parentString] = childString
                    self.path[childString] = parentString
                    self.putinQueue()
                    self.moves[childString] = 1 + self.moves[parentString]
                    if self.grid[self.dimension - 1, self.cars[0].y] == 1:
                         return False
                self.moveLeft(car)
            if Game.canMoveLeft(self, car):
                a = Game.checkMove(self)
                self.moveLeft(car)
                b = Game.checkMove(self)
                if a != b:
                    #self.setNewParent()
                    childString = self.gridToString()
                    self.children[parentString] = childString
                    self.path[childString] = parentString
                    self.putinQueue()
                    self.moves[childString] = 1 + self.moves[parentString]
                self.moveRight(car)
    def deque(self):
        print "Starting grid:\n"
        print self.grid.T
        print "\n"
        moves = 0
        while self.grid[self.dimension - 1, self.cars[0].y] != 1:
            self.grid = self.gridQueue.get()
            self.cars = self.carsQueue.get()
            moves += 1
            self.queueAllPossibleMoves()
        print "End of loop"
        print self.grid.T
        print "Finished in " + str(self.moves[self.gridToString()]) + " moves."
        print "Number of iterations: " + str(moves)
def runSimulation(game):
    # Starts animation.
    anim = visualize_rush_lepps.RushVisualization(game, 500)
    # Stop animation when done.
    anim.done()
car1 = Car(2, 2, 2, "H", 1)
car2 = Car(2, 0, 2, "H", 2)
car3 = Car(4, 0, 2, "H", 3)
car4 = Car(1, 1, 2, "H", 4)
car5 = Car(3, 1, 2, "H", 5)
car6 = Car(4, 2, 2, "V", 6)
car7 = Car(0, 3, 2, "H", 7)
car8 = Car(2, 3, 2, "H", 8)
car9 = Car(0, 4, 2, "V", 9)
car10 = Car(3, 4, 2, "V", 10)
car11 = Car(4, 4, 2, "H", 11)
car12 = Car(4, 5, 2, "H", 12)
car13 = Car(5, 1, 3, "V", 13)
cars = [car1, car2, car3, car4, car5, car6, car7, car8, car9, car10, car11, car12, car13]
print "Starting"
game = Game(6, cars)
game.deque()
runSimulation(game)