import numpy as np

path  = open('path_board3.txt')


boards = []

for line in path:
    line = line.strip("\n")
    board = []
    for i in range(6):
        board.append(line)
    board = np.vstack(board)
    boards.append(board)
print boards
    # item_split = item.split("\n")
    # #print item_split
    # for i in item_split:
    #     if i == " ":
    #         item_split.remove(i)
    # print item_split
    # item_row = []
    # for i in range(6):
    #     item_split = item.split("\n")
    #     item_row.append(item_split)
    # item_row = np.vstack(item_row)
    # item_row = np.array(item_row, dtype=int)
    # print item_row



