import math
import time

import Tkinter as tk

class RushVisualization:
    def __init__(self, boards, dimension, size, speed):
        "Initializes a visualization with the specified parameters."

        self.boards = boards
        self.speed = speed
        print boards
        self.dimension = dimension
        self.tileSize = size / self.dimension

        self.width = self.dimension
        self.height = self.dimension

        # Initialize a drawing surface
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=size, height=size)
        self.canvas.pack()
        self.window.update()
        
        # Draw gridlines
        for i in range(self.dimension + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, self.dimension)
            self.canvas.create_line(x1, y1, x2, y2)
        for i in range(self.dimension + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(self.dimension, i)
            self.canvas.create_line(x1, y1, x2, y2)

        self.runBoardsSimulation(self.boards)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        xmapped = x * self.tileSize
        ymapped = y * self.tileSize
        return (xmapped, ymapped)

    def runBoardsSimulation(self, boards):
        colors = ['blue', 'pink', 'green', 'purple', 'yellow', 'black']
        for board in boards:
            self.canvas.delete(tk.ALL)
            for y in range (len(board)):
                for x in range (len(board[y])):

                    #switch x and y to get right orientation
                    boardValue = board[y][x]
                    tileColor = 'white'
                    if boardValue == 1:
                        tileColor = 'red'
                    elif boardValue > 1:
                        tileColor = colors[boardValue%len(colors)]
                    x1, y1 = self._map_coords(x, y)
                    x2, y2 = self._map_coords(x + self.tileSize, y + self.tileSize)

                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=tileColor)
            self.canvas.update()
            time.sleep(self.speed)


    def done(self):
        tk.mainloop()