README

In this github folder there are different python programs that can solve a set of given Rush Rour boards.

There are 7 boards provided in csv in the boards folder, these can be loaded in the different algorithms as a command line argument.

4 different algorithms are provided: a Breadth first search (RushHour_Breadth.py), an A* algorithm (RushHour_AStar.py) and two Beam search algorithms with different pruning settings.
The first pruning algorithm discards 50% of the worst options after 100 iterations of dequeing (RushHour_Pruned_100it_50proc.py) and the second pruning algorithm discards 50% of the worst options after 250 iterations of dequeing (RushHour_Pruned_250it_50proc.py)  All algorithms can be executed via the terminal and take 2 or optionally 3 command line arguments. The first command line argument should be the desired algorithm, the second command line argument should be the board you would like to solve using that algorithm. If a third command line argument is provided an output file will be created which saves the path; this can be usefull for the animation. 

USAGE: 
python algorithm.py boards/desiredBoard (optional: filename_for_path_outputfile.txt)

The animation can be run using a .txt file that stores the path as integers as imput for Pathmaker.py. This program converts these integers back to boards and passes these boards to visualize_path.py which then handles the visualisation.

USAGE:
python Pathmaker.py path_file.txt speed

The third command line argument defines the animation speed, this must be a float.

