import numpy as np

path = open('path_board1.txt')

lines = []

for line in path:
    line = line.strip("\n")
    line = line.split(" ")
    #print line
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

# for item in boards:
    # run the simulation




