# identify the best distance, while in OA, check that the threshold distance isnt breached
# if breached, reacquire direction
# handle the middle case by reading which direction on the left or right is farther or better to turn into

# the distance for turning needs to be sufficient such that the rover can easily make wide turns in the same spot
# without hitting anything
import numpy as np


def get_sensor_readings(L2, L1, M, R1, R2):
    """Acquire the sensor distance data and return as a list"""
    # this wont take parameters since the sensor readings will be done by actual hardware and corresponding func calls
    # L2 = readL2
    # L1 = readL1
    # M = readM
    # R1 = readR1
    # R2 = readR2
    return np.array([L2, L1, M, R1, R2])


def find_min_max_dist(L2, L1, M, R1, R2):
    """Returns a list of indices for min and max distances seen by sensors"""
    distance_arr = get_sensor_readings(L2, L1, M, R1, R2)  # actual func call wont have parameters
    # find the shortest distance from the sensor readings and get idx
    min_idx = np.argmin(distance_arr)  # the closer distance is of immediate concern
    # find the longest distance from the sensor readings and get idx
    max_idx = np.argmax(distance_arr)
    # dictionary for the sensors based on idx
    casename_dictionary = {0: 'L2', 1: 'L1', 2: 'M', 3: 'R1', 4: 'R2'}
    min_dist_sensor = casename_dictionary[min_idx]
    max_dist_sensor = casename_dictionary[max_idx]

    return [min_dist_sensor, max_dist_sensor]


def direction_determination(L2, L1, M, R1, R2):
    """Identify and return the direction the rover needs to turn to based on sensor readings"""
    # actual function wont have parameters, this is for testing
    # unpack min and max distances
    min_max_dist = find_min_max_dist(L2, L1, M, R1, R2)
    min_dist_sensor = min_max_dist[0]  # sensor seeing min distance
    max_dist_sensor = min_max_dist[1]  # sensor seeing max distance
    print('min dist:', min_dist_sensor, 'max dist:', max_dist_sensor)

    # determining direction
    if min_dist_sensor == 'M':  # middle cases, higher priority, check first
        if max_dist_sensor == 'L2':
            print('mid hard left')
            direction = 'mid hard left'
        if max_dist_sensor == 'L1':
            print('mid left')
            direction = 'mid left'
        if max_dist_sensor == 'R1':
            print('mid right')
            direction = 'mid right'
        if max_dist_sensor == 'R2':
            print('mid hard right')
            direction = 'mid hard right'
    elif min_dist_sensor == 'L2':
        print('right')
        direction = 'right'
    elif min_dist_sensor == 'L1':
        print('hard right')
        direction = 'hard right'
    elif min_dist_sensor == 'R1':
        print('hard left')
        direction = 'hard left'
    elif min_dist_sensor == 'R2':
        print('left')
        direction = 'left'

    return direction


def obstacle_avoidance(L2, L1, M, R1, R2):
    """Sub routine triggered by nearby obstacle(s), determines navigation for obstacle avoidance and returns movement"""
    return direction_determination(L2, L1, M, R1, R2)  # actual func call wont have parameters


# Testbenching

# Single Sensor Detection #########################################
# Case 1 : Hard Left Case
print('Hard Left Case')
case = [10, 8, 6, 1, 10]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 2 : Left Case
print('Left Case')
case = [4, 10, 10, 10, 1]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 3 : Middle Case
print('Middle Case')
case = [8, 3, 1, 8, 10]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 4 : Right
print('Right Case')
case = [1, 10, 10, 10, 10]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 5 : Hard Right Case
print('Hard Right Case')
case = [10, 1, 10, 10, 10]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 6 : Hard Left Case
print('Hard Left Case')
case = [10, 10, 10, 1, 1]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 7 : Middle Case
print('Middle Case')
case = [8, 10, 1, 5, 3]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 8 : Hard Right Case
print('Hard Right Case')
case = [1, 1, 10, 10, 10]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# More complicated cases

# Case 9 : Hard Left Case
print('Hard Left Case')
case = [100, 100, 10, 1, 5]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 10 : Left Case
print('Left Case')
case = [50, 100, 10, 10, 1]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 11 : Middle Case
print('Middle Case')
case = [10, 2, 1, 4, 4]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 12 : Right
print('Right Case')
case = [1, 10, 10, 10, 10]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 13 : Hard Right Case
print('Hard Right Case')
case = [10, 1, 10, 10, 10]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')

# Case 14 : Middle Case
print('Middle Case')
case = [2, 4, 1, 10, 4]
print('Scenario:', case)
obstacle_avoidance(case[0], case[1], case[2], case[3], case[4])
print('')