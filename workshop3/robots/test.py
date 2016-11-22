import numpy as np

class Car (object):
    def __init__(self, x, y, length, orientation, idcar):
        self.x = x
        self.y = y
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
        Initializes the grid and immediately fills it with cars, which are given in an array.
        :param dimension: The width and height of the grid.
        """
        self.dimension = dimension

        #create grid, starting with zeros
        self.grid = np.zeros(shape=(dimension, dimension))



    def fillTiles(self, car):

        x = car.getX()
        y = car.getY()
        length = car.length
        orientation = car.orientation

        if orientation == "H":
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
    def __init__(self, playboard, listCar):
        self.playboard = playboard
        self.listOfCar = []

    def add_car(self, car):
        self.listOfCar.append(car)

    def isMovable(self):
        moves = 0
        while self.playboard.grid[5, 2] != 1:
            for j in range(0, len(self.listOfCar)):
                current = self.listOfCar[j]
                x = current.getX()
                y = current.getY()
                if current.orientation == "H":
                    if current.length == 2:
                        if x < 4:
                            if self.playboard.grid[x + 2, y] == 0:
                                self.playboard.grid[x + 2, y] = current.idcar
                                self.playboard.grid[x,y] = 0
                                current.x = x + 1
                                moves += 1
                        elif x > 0:
                            if self.playboard.grid[x - 1, y] == 0:
                                self.playboard.grid[x - 1, y] = current.idcar
                                self.playboard.grid[x + 1, y] = 0
                                current.x = x - 1
                                moves += 1
                    elif current.length == 3:
                        if x < 3:
                            if self.playboard.grid[x + 3, y] == 0:
                                self.playboard.grid[x + 3, y] = current.idcar
                                self.playboard.grid[x,y] = 0
                                current.x = x + 1
                                moves += 1
                        elif x > 0:
                            if self.playboard.grid[x - 1, y] == 0:
                                self.playboard.grid[x - 1, y] = current.idcar
                                self.playboard.grid[x + 2, y] = 0
                                current.x = x - 1
                                moves += 1
                elif current.orientation == "V":
                    if current.length == 2:
                        if y < 4:
                            if self.playboard.grid[x, y + 2] == 0:
                                self.playboard.grid[x, y + 2] = current.idcar
                                self.playboard.grid[x,y] = 0
                                current.y = y + 1
                                moves += 1
                        elif y > 0:
                            if self.playboard.grid[x, y - 1] == 0:
                                self.playboard.grid[x, y - 1] = current.idcar
                                self.playboard.grid[x, y + 1] = 0
                                current.y = y - 1
                                moves += 1
                    elif current.length == 3:
                        if y < 3:
                            if self.playboard.grid[x, y + 3] == 0:
                                self.playboard.grid[x, y + 3] = current.idcar
                                self.playboard.grid[x,y] = 0
                                current.y = y + 1
                                moves += 1
                        elif y > 0:
                            if self.playboard.grid[x, y - 1] == 0:
                                self.playboard.grid[x, y - 1] = current.idcar
                                self.playboard.grid[x,y + 2] = 0
                                current.y = y - 1
                                moves += 1
                print self.playboard.grid.T
                print moves
                print "\n"
                # if self.playboard.grid[5,2] == 1:
                #     print "Congrats!"
                #     break
        print self.playboard.grid.T
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
print board.grid.T
print "\n"
game = Game(board, listcar)
for i in listcar:
    game.add_car(i)
game.isMovable()