# AUTORovr
ECEN 403 Capstone: Self Navigating, Obstacle Avoiding Rover.
The repository contains all files and code for our subsystems.

The subsystems are: 
Pathfinding and Navigation (Arkadi Zhanov),
Controls (Nikolai Paderin),
Interface (Nathan Sommer).

Overview : The self navigating, obstacle avoiding rover works by receiving a start location and target destination input from a user via a phone app. This information is relayed to the rover which runs a pathfinding algorithm to find a path between the points. The pathfinding algorithm sends the nodes to the navigation subsystem to generate a grid like structure populated by cells for the rover to follow. The navigation system communicates with the controls subsystem in order for the rover to follow the navigation path. The controls system sensors detect obstacles and if one is detected, then the pathfinder and navigation program is called again to reroute.

The pathfinding and navigation subsystem implements a pathfinding algorithm to dynamically plot a path between a start and target destination. Once the optimal path is determined the pathfinder program, it returns a list of nodes obtained from the path which is sent to the navigation subsystem to be plotted onto a cell grid. The nodes are connected using Bresenhams Line Algorithm and the cells used to connect the nodes are the ones the rover will follow to traverse its environment from its current location to its target destination.
