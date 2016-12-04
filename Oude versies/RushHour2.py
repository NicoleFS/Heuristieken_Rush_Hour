# Rush Hour
# Name: Nicol Heijtbrink (10580611), Nicole Silverio (10521933) & Sander de Wijs (10582134)
# Course: Heuristieken
# University of Amsterdam
# Time: November-December, 2016

import numpy as np
import math

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
    def __init__(self, x, y, length, orientation, idcar):
        """
        Initializes a car with a position with coordinates [x, y] on a board, with a given orientation and id.
        :param x, y, length, orientation, idcar: All parameters are defined in a separate list.
        """
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = length
        self.orientation = orientation
        self.idcar = idcar

    def getX(self):
        return self.x
    def getY(self):
        return self.y

class Grid(object):
    """
    The grid will represent the area where cars will be placed and moved on.
    """
    def __init__(self, dimension):
        """
        Initializes the grid.
        :param dimension: The width and height of the grid.
        """
        self.dimension = dimension

        # create grid, consisting of a 2D array filled with 0's.
        self.grid = np.zeros(shape=(dimension, dimension))

    def fillTiles(self, car):
        """
        Fill the board with a given car.
        Checks orientation and starting coordinates of car,
        then fills in the rest according to the given length.

        :param car: object with given x, y, length, orientation and idcar
        :return: a filled grid.
        """
        x = car.getX()
        y = car.getY()
        length = car.length
        orientation = car.orientation

        # first check orientation of car
        if orientation == "H":
            # then replace 0 with idcar integer for length of car
            for i in range(0, length):
                if self.grid[x,y] == 0:
                    self.grid[x,y] = car.idcar
                    x += 1
        elif orientation == "V":
            for i in range(0, length):
                if self.grid[x,y] == 0:
                    self.grid[x,y] = car.idcar
                    y += 1
        return self.grid

class Game(object):
    """
    The state of the board (grid), which changes after each movement of a car.
    """
    def __init__(self, playboard):
        """
        Initializes the given grid and creates an empty array, to be filled with cars.
        :param playboard: The given empty grid.
        """
        self.playboard = playboard
        self.listOfCar = []
        # create counter to count total number of moves needed to win the game.
        self.moves = 0
        # create set to store board states
        self.setStates = set()
        # create list to store single board state
        self.listStates = []


    def addCar(self, car):
        """
        Appends a car into the (empty) array listOfCar.
        :param car: object with given x, y, length, orientation and idcar
        :return: Array (with appended car).
        """
        self.listOfCar.append(car)

    def moveRight(self, car):
        """
        'Moves' a given car 1 place to the right on the grid.
        Replaces the 0 on the right side next to the car with integer idcar
        and replaces the left side of the car with a 0.

        :return: grid (with 1 moved car compared to previous state of grid).
        """
        # obtain current coordinates of car
        x = car.getX()
        y = car.getY()

        # replace right side next to the car with integer idcar
        self.playboard.grid[x + car.length, y] = car.idcar
        # replace the left side of the car with a 0 (empty)
        self.playboard.grid[x, y] = 0
        # update x coordinate
        car.x = x + 1
        # add 1 (move) to counter moves
        # self.moves += 1



    def moveLeft(self, car):
        """
        'Moves' a given car 1 place to the left on the grid.
        Replaces the 0 on the left side next to the car with integer idcar
        and replaces the right side of the car with a 0.

        :return: grid (with 1 moved car compared to previous state of grid).
        """
        # obtain current coordinates of car
        x = car.getX()
        y = car.getY()

        # replace left side next to the car with integer idcar
        self.playboard.grid[x - 1, y] = car.idcar
        # replace the right side of the car with a 0 (empty)
        self.playboard.grid[x + (car.length - 1), y] = 0
        # update x coordinate
        car.x = x - 1
        # add 1 (move) to counter moves
        # self.moves += 1

    def moveDown(self, car):
        """
        'Moves' a given car 1 place down on the grid.
        Replaces the 0 one place underneath the car with integer idcar
        and replaces the top of the car with a 0.

        :return: grid (with 1 moved car compared to previous state of grid).
        """
        # obtain current coordinates of car
        x = car.getX()
        y = car.getY()

        # replace one place underneath the car with integer idcar
        self.playboard.grid[x, y + car.length] = car.idcar
        # replace the top of the car with a 0 (empty)
        self.playboard.grid[x, y] = 0
        # update y coordinate
        car.y = y + 1
        # add 1 (move) to counter moves
        # self.moves += 1

    def moveUp(self, car):
        """
        'Moves' a given car 1 place up on the grid.
        Replaces the 0 one place above the car with integer idcar
        and replaces the bottom of the car with a 0.

        :return: grid (with 1 moved car compared to previous state of grid).
        """
        # obtain current coordinates of car
        x = car.getX()
        y = car.getY()

        # replace one place above the car with integer idcar
        self.playboard.grid[x, y - 1] = car.idcar
        # replace the bottom of the car with a 0 (empty)
        self.playboard.grid[x, y + (car.length - 1)] = 0
        # update y coordinate
        car.y = y - 1
        # add 1 (move) to counter moves
        # self.moves += 1

    def isEmptyAndMove(self, car):
        """
        Checks wether a place on the grid is empty, if so, move the car.

        :return: function corresponding with a certain movement.
        """
        # obtain current coordinates of car
        x = car.getX()
        y = car.getY()

        # determine orientation of car (either horizontal ("H") or vertical ("V"))
        if car.orientation == "H":
            if car.idcar == 1:
                # make sure movement will not place car out of bounds right side of grid
                if x < (self.playboard.dimension - car.length):
                    # check if right side next to the car is empty
                    if self.playboard.grid[x + car.length, y] == 0:
                        a = Game.checkMove(self)
                        Game.moveRight(self, car)
                        self.moves += 1
                        b = Game.checkMove(self)
                        if a == b:
                            Game.moveLeft(self, car)
                            self.moves -= 1

                # make sure movement will not place car out of bounds, left side of grid
                elif x > 0:
                    # check if left side next to the car is empty
                    if self.playboard.grid[x - 1, y] == 0:
                        a = Game.checkMove(self)
                        Game.moveLeft(self, car)
                        self.moves += 1
                        b = Game.checkMove(self)
                        if a == b:
                            Game.moveRight(self, car)
                            self.moves -= 1

            else:
                # make sure movement will not place car out of bounds, left side of grid
                if x > 0:
                    # check if left side next to the car is empty
                    if self.playboard.grid[x - 1, y] == 0:
                        a = Game.checkMove(self)
                        Game.moveLeft(self, car)
                        self.moves += 1
                        b = Game.checkMove(self)
                        if a == b:
                            Game.moveRight(self, car)
                            self.moves -= 1

                # make sure movement will not place car out of bounds, right side of grid
                if x < (self.playboard.dimension - car.length):
                    # check if right side next to the car is empty
                    if self.playboard.grid[x + car.length, y] == 0:
                        a = Game.checkMove(self)
                        Game.moveRight(self, car)
                        self.moves += 1
                        b = Game.checkMove(self)
                        if a == b:
                            Game.moveLeft(self, car)
                            self.moves -= 1

        elif car.orientation == "V":
            # make sure movement will not place car out of bounds, above the grid
            if y < (self.playboard.dimension - car.length):
                # check if place above the car is empty
                if self.playboard.grid[x, y + car.length] == 0:
                    a = Game.checkMove(self)
                    Game.moveDown(self, car)
                    self.moves += 1
                    b = Game.checkMove(self)
                    if a == b:
                        Game.moveUp(self, car)
                        self.moves -= 1

            # make sure movement will not place car out of bounds, underneath the grid
            if y > 0:
                # check if place underneath the car is empty
                if self.playboard.grid[x, y - 1] == 0:
                    a = Game.checkMove(self)
                    Game.moveUp(self, car)
                    self.moves += 1
                    b = Game.checkMove(self)
                    if a == b:
                        Game.moveDown(self, car)
                        self.moves -= 1

    def checkMove(self):

        self.listStates = []
        for i in self.playboard.grid.T:
            for j in i:
                x = int(j)
                self.listStates.append(x)
        num = int(''.join(map(str,self.listStates)))
        # num = "%036d" % (num) #36 komt van 2x dimension
        self.setStates.add(num)
        #print self.setStates
        return len(self.setStates)



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
        while self.playboard.grid[self.playboard.dimension - 1, math.ceil(self.playboard.dimension / 2 - 1)] != 1:
            #
            for i in range(0, len(self.listOfCar)):
                current = self.listOfCar[i]
                if self.playboard.grid[self.playboard.dimension - 1, math.ceil(self.playboard.dimension / 2 - 1)] != 1:
                    game.isEmptyAndMove(current)
                    print self.playboard.grid.T
                    print self.moves
                else:
                    break

        # print transposed state of grid
        print self.playboard.grid.T
        print self.moves
        print "Congrats!"


car1 = Car(3, 2, 2, "H", 1)
car2 = Car(2, 0, 3, "V", 2)
car3 = Car(3, 0, 2, "H", 3)
car4 = Car(5, 0, 3, "V", 4)
car5 = Car(3, 3, 3, "V", 5)
car6 = Car(4, 3, 2, "H", 6)
car7 = Car(0, 4, 2, "V", 7)
car8 = Car(1, 4, 2, "H", 8)
car9 = Car(4, 5, 2, "H", 9)

listcar = [car1, car2, car3, car4, car5]
board = Grid(6)
for i in listcar:
    board.fillTiles(i)

# transpose board
print board.grid.T
print "\n"
game = Game(board)
for i in listcar:
    game.addCar(i)
game.isMovable()
