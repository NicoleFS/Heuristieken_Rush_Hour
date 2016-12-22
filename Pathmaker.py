import numpy as np
import visualize_path
import sys

if (len(sys.argv) != 3):
    print('Error, usage: Pathmaker.py pathfile.txt speed')
else:

    path = open(sys.argv[1])
    speed = float(sys.argv[2])

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
        y = x

    simulator = visualize_path.RushVisualization(boards, len(line), 500, speed)
    simulator.done()


