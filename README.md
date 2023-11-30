# AUTORovr
ECEN 403/404 Capstone: Self Navigating, Obstacle Avoiding Rover.
The repository contains all files and code for our subsystems.

The subsystems are: 
Pathfinding and Navigation (Arkadi Zhanov),
Hardware and Navigation (Nikolai Paderin),
Interface and Communication (Nathan Sommer).

Overview : The self navigating, obstacle avoiding rover works by receiving a start location and target destination input from a user via a phone app. This information is relayed to the rover which runs a pathfinding algorithm to find a path between the points. The pathfinding algorithm sends the nodes to the navigation subsystem to generate a grid like structure populated by cells for the rover to follow. The navigation system communicates with the controls subsystem in order for the rover to follow the navigation path. The controls system sensors detect obstacles and if one is detected, then the pathfinder and navigation program is called again to reroute.

Pathfinder and Navigation Subsystem : the pathfinding and navigation subsystem implements a pathfinding algorithm to dynamically plot a path between a start and target destination. Once the optimal path is determined the pathfinder program, it returns a list of nodes obtained from the path which is sent to the navigation subsystem to move through these nodes to the target destination node. While the rover moves through these nodes it actively detects for any potential obstacles in its path. If an obstacle is detected that exceeds a certain boundary threshold then the rover enters its obstacle avoidance procedure to navigate around the object until no further obstructions are detected by the rover. Once the obstacle avoidance procedure is complete, control is given back to the main navigation procedure. The rover course corrects to reacquire the next node it neeeds to get to and repeats the navigation and obstacle avoidance procedure as needed.
