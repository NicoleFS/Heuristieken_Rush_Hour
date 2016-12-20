# Rush Hour
# Names (student id): Nicol Heijtbrink (10580611), Nicole Silverio (10521933) & Sander de Wijs (10582134)
# Course: Heuristieken
# University of Amsterdam
# Time: November-December, 2016
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import visualize_rush_lepps
import time
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
        Initializes the grid and creates an empty array with width and length the size of dimension,
        to be filled with given Car objects.
        """

        self.dimension = dimension
        self.cars = cars

        # create a 2D grid consisting of 0's, with type integer
        self.grid = np.zeros(shape=(dimension, dimension), dtype=np.int)

        # add every given car to the grid
        for car in self.cars:
            self.addCarToGrid(car)

        # create seperate queues for the grid states and cars
        self.gridQueue = QueueClass.Queue(maxsize=0)
        self.carsQueue = QueueClass.Queue(maxsize=0)

        # add the current grid and cars to the corresponding queue
        self.gridQueue.put(self.grid.copy())
        self.carsQueue.put(self.cars)

        # create set to store board states
        self.state_set = set()

        # create dictionaries for in order to follow the parents and children of those parents
        self.path = {}

        # create key of starting grid state
        start = self.gridToString()

        self.path_state = start

        self.start_state = self.gridToString()
        # create dictionary of grid state (key) paired to
        # corresponding number of performed moves (value)
        self.moves = {}

        # set start key value
        self.moves[start] = 0

        self.all_boards_path = []

    def addCarToGrid(self, car):

        """
        Fill the board with a given Car.
        Checks orientation and starting coordinates of Car,
        then fills in the rest of the Car according to the given length.
        :param car: Car object with given x, y, length, orientation and idcar
        :return: a filled grid.
        """

        # get coordinates of car
        x = car.x
        y = car.y

        # check orientation of car
        if car.orientation == "H":

            # replace 0 with idcar integer for length of car
            for i in range(0, car.length):
                if self.grid[x, y] == 0:
                    self.grid[x, y] = car.id
                    x += 1

                # if a non-zero value is present, print error statement
                else:
                    print "Error, car cannot be placed on a tile that contains another car."

        elif car.orientation == "V":
            for i in range(0, car.length):
                if self.grid[x, y] == 0:
                    self.grid[x, y] = car.id
                    y += 1
                else:
                    print "Error, car cannot be placed on a tile that contains another car."
        else:
            print "Orientation has incorrect value."

    def canMoveRight(self, car):

        """
        Checks if the location on the right of the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not horizontal, moving to the right is not possible
        if car.orientation == "V":
            return False

        # check if movement to the right would place Car outside of the grid
        if car.x < (self.dimension - car.length):

            # check if movement to the right would cause collision between Cars
            if self.grid[car.x + car.length, car.y] == 0:
                return True
        return False

    def canMoveLeft(self, car):

        """
        Checks if the location on the left of the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not horizontal, moving to the left is not possible
        if car.orientation == "V":
            return False

        # check if movement to the left would place Car outside of the grid
        if car.x > 0:

            # check if movement to the left would cause collision between Cars
            if self.grid[car.x - 1, car.y] == 0:
                return True
        return False

    def canMoveUp(self, car):

        """
        Checks if the location above the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not vertical, moving upwards is not possible
        if car.orientation == "H":
            return False

        # check if upward movement would place Car outside of the grid
        if car.y > 0:

            # check if upward movement would cause collision between Cars
            if self.grid[car.x, car.y - 1] == 0:
                return True
        return False

    def canMoveDown(self, car):

        """
        Checks if the location underneath the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not vertical, moving downwards is not possible
        if car.orientation == "H":
            return False

        # check if downward movement would place Car outside of the grid
        if car.y < (self.dimension - car.length):

            # check if downward movement would cause collision between Cars
            if self.grid[car.x, car.y + car.length] == 0:
                return True
        return False

    def moveRight(self, carId):

        """
        'Moves' a given Car one place to the right on the grid.
        Replaces the 0 on the right side next to the Car with integer idcar
        and replaces the left side of the Car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given car out of Car list
        car = self.cars[carId.id - 1]

        # replace right side next to the Car with integer idcar
        self.grid[car.x + car.length, car.y] = car.id

        # replace the left side of the Car with a 0 (empty)
        self.grid[car.x, car.y] = 0

        # update x coordinate
        car.x = car.x + 1

        # update the list of Cars with moved Car
        self.cars[car.id - 1] = car

    def moveLeft(self, carId):

        """
        'Moves' a given Car 1 place to the left on the grid.
        Replaces the 0 on the left side next to the Car with integer idcar
        and replaces the right side of the Car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given Car out of list of Cars
        car = self.cars[carId.id - 1]

        # replace left side next to the Car with integer idcar
        self.grid[car.x - 1, car.y] = car.id

        # replace the right side of the Car with a 0 (empty)
        self.grid[car.x + (car.length - 1), car.y] = 0

        # update x coordinate
        car.x = car.x - 1

        # update the list of Cars with moved Car
        self.cars[car.id - 1] = car

    def moveDown(self, carId):

        """
        'Moves' a given Car 1 place down on the grid.
        Replaces the 0 one place underneath the Car with integer idcar
        and replaces the top of the Car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given Car out of list of Cars
        car = self.cars[carId.id - 1]

        # replace one place underneath the Car with integer idcar
        self.grid[car.x, car.y + car.length] = car.id

        # replace the top of the Car with a 0 (empty)
        self.grid[car.x, car.y] = 0

        # update y coordinate
        car.y = car.y + 1

        # update the list of Cars with moved Car
        self.cars[car.id - 1] = car

    def moveUp(self, carId):

        """
        'Moves' a given Car 1 place up on the grid.
        Replaces the 0 one place above the Car with integer idcar
        and replaces the bottom of the Car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given Car out of list of Cars
        car = self.cars[carId.id - 1]

        # replace one place above the Car with integer idcar
        self.grid[car.x, car.y - 1] = car.id

        # replace the bottom of the Car with a 0 (empty)
        self.grid[car.x, car.y + (car.length - 1)] = 0

        # update y coordinate
        car.y = car.y - 1

        # update the list of Cars with moved Car
        self.cars[car.id - 1] = car

    def putinQueue(self):

        """
        Copies a grid and inserts it in a queue.
        Deepcopies the list of Cars and puts it in a (different) queue.
        """

        self.gridQueue.put(self.grid.copy())
        self.carsQueue.put(copy.deepcopy(self.cars))

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
                hash += ","
        return hash

    def checkMove(self):

        """
        Checks if a move can be made by trying to put the new state in a set.
        If the length of the set does not change it means there is a duplicate.
        :return: set length (after trying to put the board state in the set)
        """

        # create variable with string of current grid state
        gridString = self.gridToString()

        # add string to set (if string is unique in the set)
        self.state_set.add(gridString)

        # return length of the set
        return len(self.state_set)

    def setNewParent(self, parentString):

        """
        Links parent board with their child board in dictionaries children and path.
        Then inserts the current grid in the queue.
        Adds 1 to the value of moves with child_string as key.
        """

        # create and set variable to current state as string
        child_string = self.gridToString()

        # set value of child_string key to parentString in path dictionary
        self.path[child_string] = parentString

        # insert current grid in queue
        self.putinQueue()

        # set number of moves paired with child state to number of moves from parent state + 1
        self.moves[child_string] = 1 + self.moves[parentString]

    def queueAllPossibleMoves(self):

        """
        For every Car all four directions are checked. If a Car can move in a certain direction it is checked if the
        new state is already in the archive. If so, the move is reversed. If it is a unique board state after a move
        the cars and the grid are put in queues and the move is reversed to be able to check the opposite direction.
        """

        # create and set variable to string of current grid state
        parent_string = self.gridToString()

        # iterate through every car and check if a move is possible
        for car in self.cars:
            if self.canMoveUp(car):

                # create and set variable to length of set
                a = Game.checkMove(self)

                # move Car
                self.moveUp(car)

                # create and set variable to (possibly new) length of set
                b = Game.checkMove(self)

                # compare length of set
                if a != b:

                    # if set length has changed, insert new state in queue
                    self.setNewParent(parent_string)

                # reverse the movement of the Car
                self.moveDown(car)
            if self.canMoveDown(car):
                a = Game.checkMove(self)
                self.moveDown(car)
                b = Game.checkMove(self)
                if a != b:
                    self.setNewParent(parent_string)
                self.moveUp(car)
            if self.canMoveRight(car):
                a = Game.checkMove(self)
                self.moveRight(car)
                b = Game.checkMove(self)
                if a != b:
                    self.setNewParent(parent_string)

                    # check if winning position has been reached in this state
                    if self.grid[self.dimension - 1, self.cars[0].y] == 1:

                        # if winning state has been reached, exit the for loop
                        return False
                self.moveLeft(car)
            if Game.canMoveLeft(self, car):
                a = Game.checkMove(self)
                self.moveLeft(car)
                b = Game.checkMove(self)
                if a != b:
                    self.setNewParent(parent_string)
                self.moveRight(car)

    def deque(self):

        """
        Prints starting grid and initiates algorithm to solve the board.
        Prints end state of grid, number of moves, number of iterations and time needed to solve board.
        """

        # start clock
        start_time = time.clock()

        # start_state = self.gridToString()

        # print starting grid
        print "Starting grid:"
        print self.grid.T
        print "\n"

        # set starting number of iterations to 0
        iterations = 0

        # check if board has reached the winning state, if not, keep executing body
        while self.grid[self.dimension - 1, self.cars[0].y] != 1:

            # obtain first grid and Car in corresponding queues
            self.grid = self.gridQueue.get()
            self.cars = self.carsQueue.get()

            # add 1 iteration after each movement
            iterations += 1

            # start solving algorithm
            self.queueAllPossibleMoves()

        # calculate time needed to solve board
        time_duration = time.clock() - start_time
        print "Winning position:"
        print self.grid.T
        print "Number of moves needed to finish game: " + str(self.moves[self.gridToString()])
        print "Number of iterations: ", iterations
        print "Seconds needed to run program: ", time_duration

        # print the board states for the fastest path from start to finish
        self.makePath()

    def makePath(self):

        self.all_boards_path = []

        path_state = self.gridToString()
        fastest_path = []
        fastest_path.append(path_state)
        while path_state != self.start_state:
            path_next = self.path.get(path_state)
            fastest_path.append(path_next)
            path_state = path_next
        fastest_path.append(self.start_state)

        for path in reversed(fastest_path):
            board_path = []
            y = 0
            path_split = path.split(",")
            for i in range(1, self.dimension + 1):
                x = self.dimension * i
                path_row = path_split[y:x]
                board_path.append(path_row)
                y = x
            board_path = np.vstack(board_path)
            board_path = np.array(board_path, dtype=int)
            self.all_boards_path.append(board_path)



def runSimulation(game):

    # start animation
    anim = visualize_rush_lepps.RushVisualization(game, 500)

    # stop animation when done
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

game = Game(6, cars)
game.deque()
#runSimulation(game)