import numpy as np

# this obstacle avoidance code is meant to test


def get_sensor_readings(L2, L1, M, R1, R2):
    """Acquire the sensor distance data and return as a list"""
    # this wont take parameters since the sensor readings will be done by actual hardware and corresponding func calls
    # L2 = readL2
    # L1 = readL1
    # M = readM
    # R1 = readR1
    # R2 = readR2
    return np.array([L2, L1, M, R1, R2])


def case_processing(L2, L1, M, R1, R2):
    """Perform weight multiplication and summation for each case (c1, c2, ...) and return as a list"""
    # actual function wont have parameters, this is for testing
    distance_arr = get_sensor_readings(L2, L1, M, R1, R2)  # actual func call wont have parameters

    # weight coefficients
    # w1, w2, w3, w4, w5 = 1, 2, 3, 4, 5  # weights are lightest to heaviest
    w1, w2, w3, w4, w5 = 100, 50, 20, 10, 1  # weights are heaviest to lightest

    # the comment by each weight is the order of sensors from most to least impactful for each case
    # the most impactful will have the most effect and will most likely have the smallest distance measurement
    # the idea is that the minimum of the cases is chosen as the current case

    # Original weight format
    #            L2  L1  M   R1  R2
    # c1weights = [w4, w5, w2, w1, w3]  # R1, M, R2, L1, L2
    # c2weights = [w5, w4, w3, w2, w1]  # R2, R1, M, L1, L2
    # c3weights = [w4, w3, w1, w3, w4]  # M, (L1/R1), (L2/R2)  ; was 3, 2, 1, 2, 3
    # c4weights = [w1, w2, w3, w4, w5]  # L2, L1, M, R1, R2
    # c5weights = [w3, w1, w2, w4, w5]  # L1, M, L2, R1, R2
    # New weights format
    # c1weights = [w4, w2, w5, w1, w3]  # R1, R2, M, L1, L2
    # c2weights = [w5, w4, w3, w2, w1]  # R2, R1, M, L1, L2
    # c3weights = [w4, w3, w1, w3, w4]  # M, (L1/R1), (L2/R2)  ; was 3, 2, 1, 2, 3
    # c4weights = [w1, w2, w3, w4, w5]  # L2, L1, M, R1, R2
    # c5weights = [w3, w2, w1, w4, w5]  # L1, L2, M, R1, R2
    # New weights format
    #            L2  L1  M   R1  R2
    # c1weights = [w5, w4, w2, w1, w3]  # R1, M, R2, L1, L2
    # c2weights = [w5, w4, w3, w2, w1]  # R2, R1, M, L1, L2
    # c3weights = [w2, w4, w5, w4, w2]  # M, (L1/R1), (L2/R2)  ; was 3, 2, 1, 2, 3
    # c4weights = [w1, w2, w3, w4, w5]  # L2, L1, M, R1, R2
    # c5weights = [w2, w1, w3, w4, w5]  # L1, M, L2, R1, R2
    # New weights format (SEEMS TO WORK)
    #            L2  L1  M   R1  R2
    c1weights = [w5, w5, w3, w1, w2]  # R1, M, R2, L1, L2 ; GOOD
    c2weights = [w5, w4, w3, w3, w1]  # R2, R1, M, L1, L2
    c3weights = [w2, w4, w5, w4, w2]  # M, (L1/R1), (L2/R2)
    c4weights = [w1, w3, w3, w4, w5]  # L2, L1, M, R1, R2
    c5weights = [w2, w1, w3, w5, w5]  # L1, M, L2, R1, R2 ; GOOD

    # weight vector multiplication
    c1 = np.sum(np.multiply(distance_arr, c1weights))  # hard left
    c2 = np.sum(np.multiply(distance_arr, c2weights))  # left
    c3 = np.sum(np.multiply(distance_arr, c3weights))  # straight
    c4 = np.sum(np.multiply(distance_arr, c4weights))  # right
    c5 = np.sum(np.multiply(distance_arr, c5weights))  # hard right

    print('The cases values are:', [c1, c2, c3, c4, c5])
    return [c1, c2, c3, c4, c5]


def case_classification(L2, L1, M, R1, R2):
    """Case classifier to determine which direction is best based on "path of least resistance" or minimum case value"""
    case_list = case_processing(L2, L1, M, R1, R2)  # actual func call wont have parameters. returns c list

    casename_dictionary = {0: 'c1', 1: 'c2', 2: 'c3', 3: 'c4', 4: 'c5'}
    min_val = min(case_list)  # find the min in case list, was min switched to max
    idx_of_min_val = case_list.index(min_val)
    casename = casename_dictionary[idx_of_min_val]
    print('the case determined is:', casename)

    casetype_dictionary = {'c1': 'hard left', 'c2': 'left', 'c3': 'straight', 'c4': 'right', 'c5': 'hard right'}
    casetype = casetype_dictionary[casename]
    print('the case type is:', casetype)

    return casetype

def obstacle_avoidance(L2, L1, M, R1, R2):
    """Sub routine triggered by nearby obstacle(s), determines navigation for obstacle avoidance and returns movement"""
    return case_classification(L2, L1, M, R1, R2)  # actual func call wont have parameters

# Testbenching

# Single Sensor Detection #########################################
# Case 1 : Hard Left Case
print('Hard Left Case')
case1 = [10, 10, 10, 1, 10]
obstacle_avoidance(case1[0], case1[1], case1[2], case1[3], case1[4])
print('')

# Case 6 : Hard Left Case
print('Hard Left Case')
case6 = [10, 10, 10, 1, 1]
obstacle_avoidance(case6[0], case6[1], case6[2], case6[3], case6[4])
print('')

# Case 2 : Left Case
print('Left Case')
case2 = [10, 10, 10, 10, 1]
obstacle_avoidance(case2[0], case2[1], case2[2], case2[3], case2[4])
print('')

# Case 3 : Straight Case
print('Straight Case')
case3 = [1, 10, 10, 10, 1]
obstacle_avoidance(case3[0], case3[1], case3[2], case3[3], case3[4])
print('')

# Case 7 : Straight Case
print('Straight Case')
case7 = [1, 1, 10, 1, 1]
obstacle_avoidance(case7[0], case7[1], case7[2], case7[3], case7[4])
print('')

# Case 4 : Right
print('Right Case')
case4 = [1, 10, 10, 10, 10]
obstacle_avoidance(case4[0], case4[1], case4[2], case4[3], case4[4])
print('')

# Case 5 : Hard Right Case
print('Hard Right Case')
case5 = [10, 1, 10, 10, 10]
obstacle_avoidance(case5[0], case5[1], case5[2], case5[3], case5[4])
print('')

# Case 8 : Hard Right Case
print('Hard Right Case')
case8 = [1, 1, 10, 10, 10]
obstacle_avoidance(case8[0], case8[1], case8[2], case8[3], case8[4])
print('')


# More complicated cases
# Case 9 : Hard Left Case
print('Hard Left Case')
case9 = [100, 100, 10, 1, 5]
print('Scenario:', case9)
obstacle_avoidance(case9[0], case9[1], case9[2], case9[3], case9[4])
print('')

# Case 10 : Left Case
print('Left Case')
case10 = [50, 100, 10, 10, 1]
print('Scenario:', case10)
obstacle_avoidance(case10[0], case10[1], case10[2], case10[3], case10[4])
print('')

# Case 3 : Straight Case
print('Straight Case')
case3 = [1, 10, 10, 10, 1]
print('Scenario:', case3)
obstacle_avoidance(case3[0], case3[1], case3[2], case3[3], case3[4])
print('')

# Case 4 : Right
print('Right Case')
case4 = [1, 10, 10, 10, 10]
print('Scenario:', case4)
obstacle_avoidance(case4[0], case4[1], case4[2], case4[3], case4[4])
print('')

# Case 5 : Hard Right Case
print('Hard Right Case')
case5 = [10, 1, 10, 10, 10]
print('Scenario:', case5)
obstacle_avoidance(case5[0], case5[1], case5[2], case5[3], case5[4])
print('')

# need to determine the minimum threshold voltage