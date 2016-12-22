import numpy as np
import visualize_path
import csv
import sys

if (len(sys.argv) != 2):
    print('Error, usage: Pathmaker.py pathfile.txt')
else:

    path = open(sys.argv[1])

    lines = []

    for line in path:
        line = line.strip("\n")
        line = line.split(" ")
        lines.append(line)

    boards = []

    y = 0

    for j in range((len(lines)/len(line))):
        board = []
        x = len(line) * (j+1)
        for i in range(y, x):
            board.append(lines[i])
        board = np.vstack(board)
        board = np.array(board, dtype=int)
        boards.append(board)
        print board
        y = x

    simulator = visualize_path.RushVisualization(boards, 6, 500, 0.3)
    simulator.done()


