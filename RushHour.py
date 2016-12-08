# Rush Hour
# Name: Nicol Heijtbrink (10580611), Nicole Silverio (10521933) & Sander de Wijs (10582134)
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
        # self.canMove = False
        # self.nextMove = ""

class Game(object):
    """
    The state of the board (grid), which changes after each movement of a car.
    """
    def __init__(self, dimension, cars):
        """
        Initializes the given grid and creates an empty array, to be filled with cars.
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

        # create counter to count total number of moves needed to win the game
        self.moves = 0
        # create set to store board states
        self.stateSet = set()
        # create list to store single board state
        self.stateList = []
        # self.movableCars = []

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
                    print "Error, car cannot be placed on a tile that contains another car"

        elif car.orientation == "V":
            for i in range(0, car.length):
                if self.grid[x,y] == 0:
                    self.grid[x,y] = car.id
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

    def canMoveCar(self, car):
        """
        Checks whether a place on the grid is empty, if so, moves the car and moves it back.
        Then checks if the move has already been made, if so it returns false.
        Otherwise returns true and adds the move to the queue
        """

        # determine orientation of car (either horizontal ("H") or vertical ("V"))
        # check if the car can move to the right
        if Game.canMoveRight(self, car):
            a = Game.checkMove(self)
            Game.moveRight(self, car)
            b = Game.checkMove(self)

            # ga door met 2e if loop (out of bounds)
            if a != b:
                Game.moveLeft(self, car)
                car.nextMove = "Right"
                return True  # wat gebeurd er met deze True?
            else:
                Game.moveLeft(self, car)
                if Game.canMoveLeft(self, car):
                    Game.moveLeft(self, car)
                    c = Game.checkMove(self)
                    if a != c:
                        Game.moveRight(self, car)
                        car.nextMove = "Left"
                        return True
                    else:
                        Game.moveRight(self, car)
                        return False

        # check if the car can move to the left
        if Game.canMoveLeft(self, car):
            a = Game.checkMove(self)
            Game.moveLeft(self, car)
            b = Game.checkMove(self)
            if a != b:
                Game.moveRight(self, car)
                car.nextMove = "Left"
                return True
            else:
                Game.moveRight(self, car)
                return False


                # check if the car can move down
        if Game.canMoveDown(self, car):
            a = Game.checkMove(self)
            Game.moveDown(self, car)
            b = Game.checkMove(self)
            if a != b:
                Game.moveUp(self, car)
                car.nextMove = "Down"
                return True
            else:
                Game.moveUp(self, car)
                if Game.canMoveUp(self, car):
                    Game.moveUp(self, car)
                    c = Game.checkMove(self)
                        # Game.moveDown(self, car)
                    if a != c:
                        self.validMove()
                        Game.moveDown(self, car)
                        car.nextMove = "Up"
                        return True
                    else:
                        Game.moveDown(self, car)
                        return False
                else:
                    return False


        # check if the car can move up
        if Game.canMoveUp(self, car):
            a = Game.checkMove(self)
            Game.moveUp(self, car)
            b = Game.checkMove(self)
            if a != b:
                Game.moveDown(self, car)
                car.nextMove = "Up"
                return True
            else:
                Game.moveDown(self, car)
                return False

    def putinQueue(self):
        self.gridQueue.put(self.grid.copy())
        self.carsQueue.put(copy.deepcopy(self.cars))

    def checkMove(self):
        """Checks if a move can be made by trying to put in a set. If the length of the set does not change it means
        there is a duplicate. Retruns the length of the set after trying to put the board state in the set"""
        hash = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                hash += str(self.grid[i][j])
        self.stateSet.add(hash)
        return len(self.stateSet)

    def queueAllPossibleMoves(self):
        """ for every car all directions are checked. If a car can move in a certain direction it is checked if it is
        already in the archive, if so the move is undone. If it a new unique board state after a move the cars and the
        grid are put in queues and the move is undone to be able to check the oposite direction"""
        for car in self.cars:
            # print car.id
            # print "Car coordinate ", car.x, car.y
            # print "Checking up"
            if self.canMoveUp(car):
                a = Game.checkMove(self)
                self.moveUp(car)
                b = Game.checkMove(self)
                if a != b:
                    # print "Putting grid in queue:"
                    # print self.grid.T
                    self.putinQueue()
                # else:
                    # print "This grid is already in the queue:"
                    # print self.grid.T
                self.moveDown(car)

            # print "Checking down"
            if self.canMoveDown(car):
                a = Game.checkMove(self)
                self.moveDown(car)
                b = Game.checkMove(self)
                if a != b:
                    # print "Putting grid in queue:"
                    # print self.grid.T
                    self.putinQueue()
                # else:
                    # print "This grid is already in the queue:"
                    # print self.grid.T
                self.moveUp(car)

            # print "Checking right"
            if self.canMoveRight(car):
                a = Game.checkMove(self)
                self.moveRight(car)
                b = Game.checkMove(self)
                if a != b:
                    # print "Putting grid in queue:"
                    # print self.grid.T
                    self.putinQueue()
                # else:
                    # print "This grid is already in the queue:"
                    # print self.grid.T
                self.moveLeft(car)

            # print "Checking left"
            if Game.canMoveLeft(self, car):
                a = Game.checkMove(self)
                self.moveLeft(car)
                b = Game.checkMove(self)
                if a != b:
                    # print "Putting grid in queue:"
                    # print self.grid.T
                    self.putinQueue()
                # else:
                    # print "This grid is already in the queue:"
                    # print self.grid.T
                self.moveRight(car)

    def deque(self):
        print "Starting grid:\n"
        print self.grid.T
        print "\n"

        # self.queue.put(self.grid.copy())
        moves = 0
        while self.grid[self.dimension - 1, int(self.dimension / 2 - 1)] != 1:
            self.grid = self.gridQueue.get()
            self.cars = self.carsQueue.get()
            # print "Removing grid from queue:"
            # print self.grid.T
            # print "Removing cars from queue"
            # for car in cars:
                # print car.id, car.x, car.y
            self.queueAllPossibleMoves()
            # print "______QUEUE________"
            # print self.queue.queue
            # print "___________________"
            moves += 1
        print "End of loop"
        print self.grid.T
        print "finished in", moves, "moves"

    def runSimulation(game):

        # Starts animation.
        anim = visualize_rush_lepps.RushVisualization(game, 500)

        # Stop animation when done.
        anim.done()

car1 = Car(3, 2, 2, "H", 1)
car2 = Car(2, 0, 3, "V", 2)
car3 = Car(3, 0, 2, "H", 3)
car4 = Car(5, 0, 3, "V", 4)
car5 = Car(3, 3, 3, "V", 5)
car6 = Car(4, 3, 2, "H", 6)
car7 = Car(0, 4, 2, "V", 7)
car8 = Car(1, 4, 2, "H", 8)
car9 = Car(4, 5, 2, "H", 9)

cars = [car1, car2, car3, car4, car5, car6, car7, car8, car9]

print "Starting"
game = Game(6, cars)
game.deque()

# runSimulation(game)
