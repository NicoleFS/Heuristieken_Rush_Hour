import math
import time

from Tkinter import *

class RushVisualization:
    def __init__(self, cars, dimension):
        "Initializes a visualization with the specified parameters."

        self.max_dim = max(dimension, dimension)
        self.width = dimension
        self.height = dimension
        self.cars = cars

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(dimension, dimension)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Draw gridlines
        for i in range(dimension + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, dimension)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(dimension + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(dimension, i)
            self.w.create_line(x1, y1, x2, y2)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_car(self, car):
        "Returns a rectangle representing a car with the specified parameters."
        x, y = car.getX(), car.getY()
        x1, y1 = self._map_coords(x, y)
        if (car.orientation == "H"):
            x2, y2 = self._map_coords((x + 1), y)
        if (car.orientation == "V"):
            x2, y2 = self._map_coords(x, (y + 1))
        return self.w.create_rectangle(x1, y1, x2, y2, fill = "red")

    def update(self, cars):
        "Redraws the visualization with the specified board and car state."

        # Delete all existing cars.
        if self.cars:
            for car in self.cars:
                self.w.delete(car)
                self.master.update_idletasks()

        # Draw new cars
        self.cars = []
        for car in self.cars:
            x, y = car.getX(), car.getY()
            x1, y1 = self._map_coords(x, y)
            if (car.orientation == "H"):
                x2, y2 = self._map_coords((x + 1), y)
            if (car.orientation == "V"):
                x2, y2 = self._map_coords(x, (y + 1))
            self.cars.append(self.w.create_rectangle(x1, y1, x2, y2, fill = "red"))
            self._draw_car(car)
        # self.cars = []
        # for car in self.cars:
        #     # x, y = car.getX(), car.getY()
        #     # self.cars.append(self.w.create_oval(x1, y1, x2, y2,
        #     #                                       fill = "black"))
        #     # self.cars.append(
        #     self._draw_car(car)

    def done(self):
        mainloop()
    #
    # def done(self):
    #     "Indicate that the animation is done so that we allow the user to close the window."
    #     mainloop()