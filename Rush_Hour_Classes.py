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

class Queue:
    """
    This will contain all possible moves from grid state X.
    From there, if a move has been executed, the matching state will be removed from the queue.
    The new state will allow new moves to done; these will be added to the queue.
    """
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def insert(self, item):
        self.items.insert(0,item)
        # self.items.append(x)

    def remove(self):
        # return self.remove(self[0])
        return self.items.pop()

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
        self.dimension = dimension
        self.grid = np.zeros(shape=(dimension, dimension), dtype=np.int)
        self.cars = cars
        # self.savedGrid = self.grid.T.copy()

        for car in self.cars:
            self.addCarToGrid(car)

        # print self.grid.T

        # create counter to count total number of moves needed to win the game.
        self.moves = 0
        # create set to store board states
        self.stateSet = set()
        # create list to store single board state
        self.stateList = []

        self.queue = QueueClass.Queue(maxsize=0)

    def copyGrid(self):
        self.savedGrid = self.grid.T.copy()

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

    def moveRight(self, car):
        """
        'Moves' a given car 1 place to the right on the grid.
        Replaces the 0 on the right side next to the car with integer idcar
        and replaces the left side of the car with a 0.

        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # replace right side next to the car with integer idcar
        self.grid[car.x + car.length, car.y] = car.id
        # replace the left side of the car with a 0 (empty)
        self.grid[car.x, car.y] = 0
        self.grid[car.x, car.y] = 0
        # update x coordinate
        car.x = car.x + 1
        # add 1 (move) to counter moves
        # self.moves += 1

    def moveLeft(self, car):
        """
        'Moves' a given car 1 place to the left on the grid.
        Replaces the 0 on the left side next to the car with integer idcar
        and replaces the right side of the car with a 0.

        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # replace left side next to the car with integer idcar
        self.grid[car.x - 1, car.y] = car.id
        # replace the right side of the car with a 0 (empty)
        self.grid[car.x + (car.length - 1), car.y] = 0
        # update x coordinate
        car.x = car.x - 1
        # add 1 (move) to counter moves
        # self.moves += 1

    def moveDown(self, car):
        """
        'Moves' a given car 1 place down on the grid.
        Replaces the 0 one place underneath the car with integer idcar
        and replaces the top of the car with a 0.

        :return: grid (with 1 moved car compared to previous state of grid).
        """
        # replace one place underneath the car with integer idcar
        self.grid[car.x, car.y + car.length] = car.id
        # replace the top of the car with a 0 (empty)
        self.grid[car.x, car.y] = 0
        # update y coordinate
        car.y = car.y + 1
        # add 1 (move) to counter moves
        # self.moves += 1

    def moveUp(self, car):
        """
        'Moves' a given car 1 place up on the grid.
        Replaces the 0 one place above the car with integer idcar
        and replaces the bottom of the car with a 0.

        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # replace one place above the car with integer idcar
        self.grid[car.x, car.y - 1] = car.id
        # replace the bottom of the car with a 0 (empty)
        self.grid[car.x, car.y + (car.length - 1)] = 0
        # update y coordinate
        car.y = car.y - 1
        # add 1 (move) to counter moves
        # self.moves += 1

    def isEmptyAndMove(self, car):
        """
        Checks whether a place on the grid is empty, if so, move the car.
        :return: function corresponding with a certain movement.
        """
        # obtain current coordinates of car
        x = car.x
        y = car.y

        self.copyGrid()
        self.queue.put(self.savedGrid)

        # determine orientation of car (either horizontal ("H") or vertical ("V"))
        if car.orientation == "H":
            if car.id == 1:
                # make sure movement will not place car out of bounds right side of grid
                if car.x < (self.dimension - car.length):
                    # check if right side next to the car is empty
                    if self.grid[x + car.length, y] == 0:
                        a = Game.checkMove(self)
                        Game.moveRight(self, car)
                        self.moves += 1
                        b = Game.checkMove(self)
                        if a == b:
                            Game.moveLeft(self, car)
                            self.moves -= 1
                        else:
                            self.copyGrid()
                            self.queue.put(self.savedGrid)

                # make sure movement will not place car out of bounds, left side of grid
                if x > 0:
                    # check if left side next to the car is empty
                    if self.grid[x - 1, y] == 0:
                        a = Game.checkMove(self)
                        Game.moveLeft(self, car)
                        self.moves += 1
                        b = Game.checkMove(self)
                        if a == b:
                            Game.moveRight(self, car)
                            self.moves -= 1
                        else:
                            self.copyGrid()
                            self.queue.put(self.savedGrid)

            else:
                # make sure movement will not place car out of bounds, left side of grid
                if x > 0:
                    # check if left side next to the car is empty
                    if self.grid[x - 1, y] == 0:
                        a = Game.checkMove(self)
                        Game.moveLeft(self, car)
                        self.moves += 1
                        b = Game.checkMove(self)
                        if a == b:
                            Game.moveRight(self, car)
                            self.moves -= 1
                        else:
                            self.copyGrid()
                            self.queue.put(self.savedGrid)

                # make sure movement will not place car out of bounds, right side of grid
                if x < (self.dimension - car.length):
                    # check if right side next to the car is empty
                    if self.grid[x + car.length, y] == 0:
                        a = Game.checkMove(self)
                        Game.moveRight(self, car)
                        self.moves += 1
                        b = Game.checkMove(self)
                        if a == b:
                            Game.moveLeft(self, car)
                            self.moves -= 1
                        else:
                            self.copyGrid()
                            self.queue.put(self.savedGrid)

        elif car.orientation == "V":
            # make sure movement will not place car out of bounds, above the grid
            if y < (self.dimension - car.length):
                # check if place above the car is empty
                if self.grid[x, y + car.length] == 0:
                    a = Game.checkMove(self)
                    Game.moveDown(self, car)
                    self.moves += 1
                    b = Game.checkMove(self)
                    if a == b:
                        Game.moveUp(self, car)
                        self.moves -= 1
                    else:
                        self.copyGrid()
                        self.queue.put(self.savedGrid)

            # make sure movement will not place car out of bounds, underneath the grid
            if y > 0:
                # check if place underneath the car is empty
                if self.grid[x, y - 1] == 0:
                    a = Game.checkMove(self)
                    Game.moveUp(self, car)
                    self.moves += 1
                    b = Game.checkMove(self)
                    if a == b:
                        Game.moveDown(self, car)
                        self.moves -= 1
                    else:
                        self.copyGrid()
                        self.queue.put(self.savedGrid)

    def checkMove(self):
        self.stateList = []
        for i in self.grid.T:
            for j in i:
                x = int(j)
                self.stateList.append(x)
        num = int(''.join(map(str,self.stateList)))
        # num = "%036d" % (num) #36 komt van 2x dimension
        self.stateSet.add(num)
        #print self.setStates
        return len(self.stateSet)

    def isMovable(self):
        """
        Moves a car in a random direction if possible.
        Checks if the red car (always the first car in the given list) is on the winning position.
        If red car is on the winning position, print congratulatory message and stop function.

        Works it way down from the list of cars.
        So first car in the list is the first car to be checked.

        :return: grid with a chosen car that is moved.
        """
        # check if winning position is occupied by red car
        winningPosition = self.dimension - 1, int(self.dimension / 2 - 1)

        while self.grid[winningPosition] != 1:
            for i in range(0, len(self.cars)):
                current = self.cars[i]
                if self.grid[winningPosition] != 1:
                    game.isEmptyAndMove(current)
                    # num in queue/stack zetten
                    # in geval van queue, move ongedaan maken
                    # eerste item uit queue, laatste uit stack halen
                    # daar weer children van maken, aka num in queue zetten
                    # nieuwe parent als game instellen
                    #
                    print self.grid.T
                    print self.moves
                else:
                    break

        # print transposed state of grid
        print self.grid.T
        print self.moves
        print "Congrats!"
        print self.queue.get()

def runSimulation(game):
    
    # Starts animation.
    anim = visualize_rush_lepps.RushVisualization(game, 500)
    # anim.update(cars)
            
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

cars = [car1, car2, car3, car4, car5]

game = Game(6, cars)
game.isMovable()
print game.queue.queue

#runSimulation(game)
