# Rush Hour
# Name: Nicol Heijtbrink (10580611), Nicole Silverio (10521933) & Sander de Wijs (10582134)
# Course: Heuristieken
# University of Amsterdam
# Time: November-December, 2016

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
#import visualize_rush_lepps
import pylab
import math
import Queue as QueueClass
import copy
import time

class PQueueItem(object):
    def __init__(self, priority, cars, grid):
        self.priority = priority
        self.cars = cars
        self.grid = grid
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

# make board instance, put that object in the set
# use__cmp__ for the priority queue

class Car(object):
    """
    An object which can move around the board.
    """
    def __init__(self, x, y, length, orientation, id):
        """
        Initializes a car with a position with coordinates [x, y] on a board, with a given orientation and id.
        :param x, y, length, orientation, id: All parameters are defined in a separate list.
        """
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = length
        self.id = id

class Game(object):
    """
    The state of the board (grid), which changes after each movement of a car.
    """
    def __init__(self, dimension, cars):
        """
        Initializes the given grid and creates an empty array, to be filled with cars.
        :param playboard: The given empty grid.
        """
        self.cars = cars
        self.dimension = dimension

        self.grid = np.zeros(shape=(dimension, dimension), dtype=np.int)

        for car in self.cars:
            self.addCarToGrid(car)

        self.queue = QueueClass.PriorityQueue()

        self.priority = 500

        queueItem = PQueueItem(self.priority, copy.deepcopy(self.cars), self.grid.copy())
        self.queue.put(queueItem)

        # create set to store board states
        self.stateSet = set()
        # create list to store single board state
        self.stateList = []

        # create key of starting grid state
        start = self.gridToString()

        # create dictionary of grid state (key) paired to
        # corresponding number of performed moves (value)
        self.moves = {}

        # set start key value
        self.moves[start] = 0

<<<<<<< HEAD
=======
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)
>>>>>>> 72d2778570452efab5013b6c60c386b59a37b7fd

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
                if self.grid[x,y] == 0:
                    self.grid[x,y] = car.id
                    x += 1
                else:
                    print car.id
                    print "Error, car cannot be placed on a tile that contains another car"

        elif car.orientation == "V":
            for i in range(0, car.length):
                if self.grid[x,y] == 0:
                    self.grid[x,y] = car.id
                    y += 1
                else:
                    print car.id
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

        # add 1 (move) to counter moves
        # self.moves += 1

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

<<<<<<< HEAD
    def calculateCost(self, car):
=======
    def calculateCost(self, car, gridstring):
>>>>>>> 72d2778570452efab5013b6c60c386b59a37b7fd

        # initial cost for all cars
        cost = 500

        moves = self.moves[gridstring]
        cost += moves * 10

        # checks if any part of a vertical car is in line and in front of the red car
        if car.orientation == "V" and car.x > self.cars[0].x:
            if car.y == self.cars[0].y:
                cost -= 100
            if car.y - 1 == self.cars[0].y:
                cost -= 100
            if car.length == 3:
                if car.y - 2 == self.cars[0].y:
                    cost -= 100

        # checks for the red car
        if car.id == 1:
            cost -= 200

        # gives trucks priority
        if car.length == 3:
            cost -= 200

        # gives cars at the left of the board lower priority
        if car.x < self.dimension/2:
            cost += 100

        # gives the state with the red car at the winning position huge priority
        if  self.grid[self.dimension - 1, self.cars[0].y] == 1:
            cost -= 400

        return cost

    def putinQueue(self, car, gridstring):
        self.priority = self.calculateCost(car, gridstring)
        queueItem = PQueueItem(self.priority, copy.deepcopy(self.cars), self.grid.copy())
        self.queue.put(queueItem)

    def checkMove(self):
        """Checks if a move can be made by trying to put in a set. If the length of the set does not change it means
        there is a duplicate. Retruns the length of the set after trying to put the board state in the set"""
        grid_string = self.gridToString()
        self.stateSet.add(grid_string)
        return len(self.stateSet)

    def gridToString(self):
        """
        Transforms the grid into a string of numbers, representing the state of the board.
        :return: String representing state of board.
        """

        # create variable to store string in
        hash = ""

        # iterate through the grid and place every integer in the hash as a char, creating a string
        for i in range(len(self.grid.T)):
            for j in range(len(self.grid[i])):
                hash += str(self.grid.T[i][j])
        return hash

    def queueAllPossibleMoves(self):
            """ for every car all directions are checked. If a car can move in a certain direction it is checked if it is
            already in the archive, if so the move is undone. If it a new unique board state after a move the cars and the
            grid are put in queues and the move is undone to be able to check the oposite direction"""

            parent_string = self.gridToString()

            for car in self.cars:
                if self.canMoveUp(car):
                    a = Game.checkMove(self)
                    self.moveUp(car)
                    b = Game.checkMove(self)
                    if a != b:
                        # create and set variable to current state as string
                        child_string = self.gridToString()
                        # set number of moves paired with child state to number of moves from parent state + 1
                        self.moves[child_string] = 1 + self.moves[parent_string]

                        self.putinQueue(car, child_string)


                    self.moveDown(car)

                if self.canMoveDown(car):
                    a = Game.checkMove(self)
                    self.moveDown(car)
                    b = Game.checkMove(self)
                    if a != b:
                        # create and set variable to current state as string
                        child_string = self.gridToString()
                        # set number of moves paired with child state to number of moves from parent state + 1
                        self.moves[child_string] = 1 + self.moves[parent_string]

                        self.putinQueue(car, child_string)


                    self.moveUp(car)

                if self.canMoveRight(car):
                    a = Game.checkMove(self)
                    self.moveRight(car)
                    b = Game.checkMove(self)
                    if a != b:
                        # create and set variable to current state as string
                        child_string = self.gridToString()
                        # set number of moves paired with child state to number of moves from parent state + 1
                        self.moves[child_string] = 1 + self.moves[parent_string]

                        self.putinQueue(car, child_string)


                    self.moveLeft(car)

                if Game.canMoveLeft(self, car):
                    a = Game.checkMove(self)
                    self.moveLeft(car)
                    b = Game.checkMove(self)
                    if a != b:
                        # create and set variable to current state as string
                        child_string = self.gridToString()
                        # set number of moves paired with child state to number of moves from parent state + 1
                        self.moves[child_string] = 1 + self.moves[parent_string]

                        self.putinQueue(car, child_string)


                    self.moveRight(car)

    def deque(self):

        startTime = time.clock()
        print "Starting grid:\n"
        print self.grid.T
        print "\n"

        iteratrions = 0
        while self.grid[self.dimension - 1, self.cars[0].y] != 1:
            queueItem = self.queue.get()
            self.grid = queueItem.grid
            self.cars = queueItem.cars
            self.queueAllPossibleMoves()
            iteratrions += 1

        timeDuration = time.clock() - startTime
        print "End of loop"
        print self.grid.T
        print "Number of moves needed to finish game: ", self.moves[self.gridToString()]
        print "finished in", iteratrions, "iterations"
        print timeDuration

#def runSimulation(game):

    # Starts animation.
    #anim = visualize_rush_lepps.RushVisualization(game, 500)

    # Stop animation when done.
    #anim.done()

car1 = Car(0, 2, 2, "H", 1)
car2 = Car(1, 0, 2, "H", 2)
car3 = Car(1, 1, 2, "H", 3)
car4 = Car(3, 1, 2, "V", 4)
car5 = Car(4, 1, 2, "H", 5)
car6 = Car(2, 2, 2, "V", 6)
car7 = Car(5, 2, 2, "V", 7)
car8 = Car(0, 3, 2, "H", 8)
car9 = Car(3, 3, 2, "H", 9)
car10 = Car(0, 4, 2, "V", 10)
car11 = Car(2, 4, 2, "V", 11)
car12 = Car(4, 4, 2, "H", 12)
car13 = Car(3, 0, 3, "H", 13)

cars = [car1, car2, car3, car4, car5, car6, car7, car8, car9, car10, car11, car12, car13]

print "Starting"
game = Game(6, cars)
game.deque()

#runSimulation(game)
