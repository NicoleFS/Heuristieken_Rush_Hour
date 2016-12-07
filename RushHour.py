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
        self.canMove = False
        self.nextMove = ""

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

        self.queue = QueueClass.Queue(maxsize=0)
        # self.queue.put(self.grid.copy())

        # create counter to count total number of moves needed to win the game
        self.moves = 0
        # create set to store board states
        self.stateSet = set()
        # create list to store single board state
        self.stateList = []

        self.movableCars = []

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

    # def canMoveRight(self, car):


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

    def invalidMove(self):
        #print "invalid move"
        self.moves -= 1
        return False

    def validMove(self):
        #print "valid move"
        self.moves += 1
        self.queue.put(self.grid.copy())
        return True

    def canMoveCar(self, car):
        """
        Checks whether a place on the grid is empty, if so, moves the car and moves it back.
        Then checks if the move has already been made, if so it returns false.
        Otherwise returns true and adds the move to the queue
        """

        # determine orientation of car (either horizontal ("H") or vertical ("V"))
        if car.orientation == "H":
            # check if the car can move to the right
            if car.x < (self.dimension - car.length):
                if self.grid[car.x + car.length, car.y] == 0:
                    a = Game.checkMove(self)
                    Game.moveRight(self, car)
                    b = Game.checkMove(self)
                    #Game.moveLeft(self, car)
                    # ga door met 2e if loop (out of bounds)
                    if a != b:
                        self.validMove()
                        Game.moveLeft(self, car)
                        car.nextMove = "Right"
                        return True #wat gebeurd er met deze True?
                    else:
                        Game.moveLeft(self, car)
                        if car.x > 0:
                            if self.grid[car.x - 1, car.y] == 0:
                                Game.moveLeft(self, car)
                                c = Game.checkMove(self)
                                # Game.moveRight(self, car)
                                if a != c:
                                    self.validMove()
                                    Game.moveRight(self, car)
                                    car.nextMove = "Left"
                                    return True
                                else:
                                    Game.moveRight(self, car)
                                    return self.invalidMove()
                            else:
                                return self.invalidMove()
                        else:
                            return self.invalidMove()

            # check if the car can move to the left
            if car.x > 0:
                if self.grid[car.x - 1, car.y] == 0:
                    a = Game.checkMove(self)
                    Game.moveLeft(self, car)
                    b = Game.checkMove(self)
                    # Game.moveRight(self, car)
                    if a != b:
                        self.validMove()
                        Game.moveRight(self, car)
                        car.nextMove = "Left"
                        return True
                    else:
                        Game.moveRight(self, car)
                        return self.invalidMove()
                        # if car.x < (self.dimension - car.length):
                        #     if self.grid[car.x + car.length, car.y] == 0:
                        #         Game.moveRight(self, car)
                        #         c = Game.checkMove(self)
                        #         Game.moveLeft(self, car)
                        #         if a != c:
                        #             self.validMove()
                        #             car.nextMove = "Right"
                        #             return True
                        #         else:
                        #             return self.invalidMove()
                        #     else:
                        #         return self.invalidMove()
                        # else:
                        #     return self.invalidMove()

            #else:
                #print "Car can not be moved"
             #   return False

        elif car.orientation == "V":
            # check if the car can move down
            if car.y < (self.dimension - car.length):
                if self.grid[car.x, car.y + car.length] == 0:
                    a = Game.checkMove(self)
                    Game.moveDown(self, car)
                    b = Game.checkMove(self)
                    # Game.moveUp(self, car)
                    if a != b:
                        self.validMove()
                        Game.moveUp(self, car)
                        car.nextMove = "Down"
                        return True
                    else:
                        Game.moveUp(self, car)
                        if car.y > 0:
                            if self.grid[car.x, car.y - 1] == 0:
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
                                    return self.invalidMove()
                            else:
                                return self.invalidMove()
                        else:
                            return self.invalidMove()

            # check if the car can move up
            if car.y > 0:
                if self.grid[car.x, car.y - 1] == 0:
                    # check if place underneath the car is empty
                    a = Game.checkMove(self)
                    Game.moveUp(self, car)
                    b = Game.checkMove(self)
                    # Game.moveDown(self, car)
                    if a != b:
                        self.validMove()
                        Game.moveDown(self, car)
                        car.nextMove = "Up"
                        return True
                    else:
                        Game.moveDown(self, car)
                        return self.invalidMove()
                        # if car.y < (self.dimension - car.length):
                        #     if self.grid[car.x, car.y + car.length] == 0:
                        #         Game.moveDown(self, car)
                        #         c = Game.checkMove(self)
                        #         Game.moveUp(self, car)
                        #         if a != c:
                        #             self.validMove()
                        #             car.nextMove = "Down"
                        #             return True
                        #         else:
                        #             return self.invalidMove()
                        #     else:
                        #         return self.invalidMove()
                        # else:
                        #     return self.invalidMove()
                #else:
                 #   return False
            #else:
            #    return False
        else:
           print "No car orientation was found"

    def checkMove(self):
        self.stateList = []
        for i in self.grid.T:
            for j in i:
                x = int(j)
                self.stateList.append(x)
        num = int(''.join(map(str,self.stateList)))
        self.stateSet.add(num)
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

        print "- - - - - - - - - - - - - - - -"
        print self.grid.T

        for i in range(len(self.cars)):
            movable = self.canMoveCar(self.cars[i])
            if movable != False:
                self.cars[i].canMove = True
                print self.cars[i].id, self.cars[i].canMove, self.cars[i].nextMove
                self.movableCars.append(self.cars[i])

    def dequeue (self):
        while self.grid[self.dimension - 1, int(self.dimension / 2 - 1)] != 1:
            self.isMovable()
            self.grid = self.queue.get()
            print "########"
            print self.grid.T
            print "########"
            for i in range(len(self.movableCars)):
                if self.movableCars[i].nextMove == "Right" and self.movableCars[i].canMove == True:
                    self.moveRight(self.movableCars[i])
                    self.queue.put(self.grid.copy())
                    print "////"
                    print self.queue.queue
                    print "////"
                    self.moveLeft(self.movableCars[i])
                    self.movableCars[i].canMove = False
                    self.movableCars[i].nextMove = ""
                    print "moved", self.movableCars[i].id, self.movableCars[i].canMove, "right"
                    self.movableCars.pop(0)
                    self.dequeue()

                if self.movableCars[i].nextMove == "Left" and self.movableCars[i].canMove == True:
                    self.moveLeft(self.movableCars[i])
                    self.queue.put(self.grid.copy())
                    print "////"
                    print self.queue.queue
                    print "////"
                    self.moveRight(self.movableCars[i])
                    self.movableCars[i].canMove = False
                    self.movableCars[i].nextMove = ""
                    print "moved", self.movableCars[i].id, self.movableCars[i].canMove, "left"
                    self.movableCars.pop(0)
                    self.dequeue()

                if self.movableCars[i].nextMove == "Up" and self.movableCars[i].canMove == True:
                    self.moveUp(self.movableCars[i])
                    self.queue.put(self.grid.copy())
                    print "////"
                    print self.queue.queue
                    print "////"
                    self.moveDown(self.movableCars[i])
                    self.movableCars[i].canMove = False
                    self.movableCars[i].nextMove = ""
                    print "moved", self.movableCars[i].id, self.movableCars[i].canMove, "up"
                    self.movableCars.pop(0)
                    self.dequeue()

                if self.movableCars[i].nextMove == "Down" and self.movableCars[i].canMove == True:
                    self.moveDown(self.movableCars[i])
                    self.queue.put(self.grid.copy())
                    print "////"
                    print self.queue.queue
                    print "////"
                    self.moveUp(self.movableCars[i])
                    self.movableCars[i].canMove = False
                    self.movableCars[i].nextMove = ""
                    print "moved", self.movableCars[i].id, self.movableCars[i].canMove, "down"
                    self.movableCars.pop(0)
                    self.dequeue()

                print"________________"
                print self.queue.queue

        # check if winning position is occupied by red car

        # winningPosition = self.dimension - 1, int(self.dimension / 2 - 1)
        #
        # self.grid = self.grid
        # while self.grid[winningPosition] != 1:
        #     for i in range(2):
        #         for i in range(0, len(self.cars)):
        #             current = self.cars[i]
        #             if self.grid[winningPosition] != 1:
        #                 game.isEmptyAndMove(current)
        #             else:
        #                 break

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

game = Game(6, cars)
game.dequeue()

# runSimulation(game)
