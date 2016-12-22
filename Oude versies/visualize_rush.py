import math
import time

import Tkinter as tk

class RushVisualization:
    def __init__(self, game, size):
        "Initializes a visualization with the specified parameters."

        self.dimension = game.dimension
        self.tileSize = size / self.dimension
        self.margin = 5
        self.carSize = self.tileSize #- self.margin

        self.width = self.dimension
        self.height = self.dimension
        self.cars = game.cars

        # Initialize a drawing surface
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=size, height=size)
        self.canvas.pack()
        self.window.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(self.dimension, self.dimension)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Draw gridlines
        for i in range(self.dimension + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, self.dimension)
            self.canvas.create_line(x1, y1, x2, y2)
        for i in range(self.dimension + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(self.dimension, i)
            self.canvas.create_line(x1, y1, x2, y2)
        self.draw_cars()
        # self.master.update_idletasks()
        # mainloop()

    def _map_coords(self, x, y):
        xmapped = x * self.tileSize
        ymapped = y * self.tileSize
        return (xmapped, ymapped)
        "Maps grid positions to window positions (in pixels)."


    def draw_cars(self):
        colors = ['blue', 'red', 'green', 'purple', 'yellow', 'black']
        for car in self.cars:
            xStretch = 1
            yStretch = 1
            if car.orientation == "H":
                xStretch = car.length
            if car.orientation == "V":
                yStretch = car.length
            x1, y1 = (self._map_coords(car.x, car.y))
            x1 += self.margin
            y1 += self.margin
            # x1 = (car.x * self.tileSize + self.margin)
            x2 = (x1 + self.tileSize * xStretch)
            x2 = x2 - self.margin * 2
            # y1 = (car.y * self.tileSize + self.margin)
            y2 = (y1 + self.tileSize * yStretch)# - self.margin * 4)
            y2 = y2 - self.margin * 2
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[car.id%len(colors)])

    # def update(self, cars):
        # "Redraws the visualization with the specified board and car state."
        #
        # # Delete all existing cars.
        # if self.cars:
        #     for car in self.cars:
        #         self.canvas.delete(car)
        #         self.master.update_idletasks()
        #
        # # Draw new cars
        # self.cars = []
        # for car in self.cars:
        #     x, y = car.x, car.y
        #     x1, y1 = self._map_coords(x, y)
        #     if (car.orientation == "H"):
        #         x2, y2 = self._map_coords((x + 1), y)
        #     if (car.orientation == "V"):
        #         x2, y2 = self._map_coords(x, (y + 1))
        #     self.cars.append(self.w.create_rectangle(x1, y1, x2, y2, fill = "red"))
        #     self._draw_car(car)
        # self.cars = []
        # for car in self.cars:
        #     # x, y = car.getX(), car.getY()
        #     # self.cars.append(self.w.create_oval(x1, y1, x2, y2,
        #     #                                       fill = "black"))
        #     # self.cars.append(
        #     self._draw_car(car)

    def done(self):
        tk.mainloop()