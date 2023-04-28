# AUTORovr
ECEN 403 Capstone: Self Navigating, Obstacle Avoiding Rover.
The repository contains all files and code for our subsystems.

The subsystems are: 
Pathfinding and Navigation (Arkadi Zhanov),
Controls (Nikolai Paderin),
Interface (Nathan Sommer).

The pathfinding and navigation subsystem implements a pathfinding algorithm to dynamically plot a path between a start and target destination. Once the optimal path is determined the pathfinder program, it returns a list of nodes obtained from the path which is sent to the navigation subsystem to be plotted onto a cell grid. The nodes are connected using Bresenhams Line Algorithm and the cells used to connect the nodes are the ones the rover will follow to traverse its environment from its current location to its target destination.
