import numpy as np
import visualize_path
import sys

# ensures propper usage
if (len(sys.argv) != 3):
    print('Error, usage: Pathmaker.py pathfile.txt speed')

else:
    # opens a file that contains the path data
    path = open(sys.argv[1])

    # sets the second commandline argument to be the speed
    speed = float(sys.argv[2])

    lines = []

    # loops over all lines in the file
    for line in path:
        # removes end of line characters
        line = line.strip("\n")
        # splits each character on spaces
        line = line.split(" ")
        # appends all characters of the line to a list
        lines.append(line)

    boards = []

    y = 0

    # divides the amount of lines by the length of a line to get either 6x6 or 9x9 boards
    for j in range((len(lines)/len(line))):
        board = []
        # x is the line in which you start a new board
        x = len(line) * (j+1)
        # loops over all numbers that belong to one board
        for i in range(y, x):
            # appends each line for the board to a board list
            board.append(lines[i])

        # converts the list of lists back to an numpy array
        board = np.vstack(board)
        board = np.array(board, dtype=int)

        # adds the board to a list of boards
        boards.append(board)
        # sets the next new starting line
        y = x

    # calls the simulation with the board, dimension, canvas size and speed
    simulator = visualize_path.RushVisualization(boards, len(line), 500, speed)
    simulator.done()


