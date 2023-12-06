# AUTORovr
ECEN 403/404 Capstone: Self Navigating, Obstacle Avoiding Rover.
The repository contains all files and code for our subsystems.

# The subsystems are: 
Pathfinding, Navigation, Obstacle Avoidance (Arkadi Zhanov),
Hardware and Navigation (Nikolai Paderin),
Interface and Communication (Nathan Sommer).

# Overview: 
The self navigating, obstacle avoiding rover works by receiving a start location and target destination input from a user via a phone app. This information is relayed to the rover which runs a pathfinding algorithm to find a path between the points. The pathfinding algorithm sends the nodes to the navigation subsystem to generate a grid like structure populated by cells for the rover to follow. The navigation system communicates with the controls subsystem in order for the rover to follow the navigation path. The controls system sensors detect obstacles and if one is detected, then the pathfinder and navigation program is called again to reroute.

# Pathfinder and Navigation Subsystem: 
The pathfinding and navigation subsystem implements a pathfinding algorithm to dynamically plot a path between a start and target destination. Once the optimal path is determined the pathfinder program, it returns a list of nodes obtained from the path which is sent to the navigation subsystem to move through these nodes to the target destination node. While the rover moves through these nodes it actively detects for any potential obstacles in its path. If an obstacle is detected that exceeds a certain boundary threshold then the rover enters its obstacle avoidance procedure to navigate around the object until no further obstructions are detected by the rover. Once the obstacle avoidance procedure is complete, control is given back to the main navigation procedure. The rover course corrects to reacquire the next node it neeeds to get to and repeats the navigation and obstacle avoidance procedure as needed.

# Control, Communication, and Navigation Subsystem: 
This subsystem ustilizes serial communication to gather GPS information as well as control a sabertooth 2x25 motor controller. It also utilizes a 4G connection to transmit and recieve information such as current GPS location, and a list of nodes and commands sent to the rover from the client side APP. The main function of this folder is to allow the rover to traverse a list of nodes while avoiding obstacles in its path using sonic distance sensors. It seeks nodes using a haversine function that takes into accound the distances between GPS locations, as well as their angle from north in order to calculate the desired trajectory and any amendments that need to be made to the current one. It will dynamically alter its path in order to get to each individual node, using distance steps of 1 meter to gather any and all necessary information for it to arrive within 2 meters of the desired node before traverseing to the next node on its list. It requires the pathfinder and navigation subsystem as well as the App subsystems to function optimally.

# Interface and Communication Subsystem:
Interface and Communication: This subsystem is created for the user, as well as the communications for all subsytems. For the Interface subsystem, there is an app created with android studio that is able to update the user as to what is currently happening with the rover. The first page is a signin/login page that the user will enter in order to connect to the rover. Once this happens, the GPS of the rover will show. The user is able to choose a point, and send a request to create a route to the pathfinder. Once the route is created, the user will be able to see it. The user can then send commands to the rover, such as stop and go. There is also a help page for the user in the app. In order to establish communication, we decided to use a Virtual Private Network (VPN), so that communcation can happen. Once all subsystems are connected to the VPN, the system uses socket programming to send data back and forth. Through the use of multi-threading and sockets, all subsystems are able to send and recieve information simultaneously.

# How to use:
1) Turn on the rover and its Raspberry Pi
2) Download 'ObstacleAvoidanceV2.py' and 'UpdatedSocketPathfinder.py' and store them in the same directory
3) Remote into the Pi or through a display find and run the main program
4) Wait for the terminal/console on the Pi to print that it has connected to the server socket
5) Open and run 'UpdatedSocketPathfinder.py' on a seperate computer in an IDE of your choosing (we used PyCharm)
6) Wait for the terminal/console to print that it has connected to the server socket
7) Open the app on a phone and select a target destination from the map on the screen
8) Wait for the app to receive the GPS location of the rover (the location of the rover is used as the starting location)
9) The rover should begin moving to the destinaion set in the phone 
