import time
import serial
import requests
import numpy as np
import RPi.GPIO as GPIO


####setup of all needed ports + connection configuration
ser = serial.Serial('/dev/ttyS0', 9600)
GPIO.setmode(GPIO.BOARD)

# Trigger (Out)
GPIO.setup(3,  GPIO.OUT)# L2
GPIO.setup(11, GPIO.OUT)# L1
GPIO.setup(19, GPIO.OUT)# M
GPIO.setup(29, GPIO.OUT)# R1
GPIO.setup(33, GPIO.OUT)# R2

# Echo (In)
GPIO.setup(5,  GPIO.IN)# L2
GPIO.setup(13, GPIO.IN)# L1
GPIO.setup(21, GPIO.IN)# M
GPIO.setup(31, GPIO.IN)# R1
GPIO.setup(35, GPIO.IN)# R2

def execute_command(direction, duration, ser):
    #speed is 120 meters a minute or 2 meters per second
    if direction == "fwd":
        print("moving forward")
        val = int(31)
        command = bytes([val+64])
        command2 = bytes([(val+127+64)])
        #print(command, command2)
        ser.write(command)
        ser.write(command2)
        duration*=(0.5*(100/93)*(3/2.7))
        print("moving forward")
        while(duration >= 0):
            time.sleep(0.01)
            duration -= 0.01

        ser.write(b'\x00')
    elif direction == "back":
        val = int((25/100)*127)
        command = bytes([val])
        command2 = bytes([val+127])
        ser.write(command)
        ser.write(command2)
        while(duration >= 0):
            time.sleep(0.1)
            duration -= 0.1
        ser.write(b'\x00')
    elif direction == "right":
        print("turning right")
        val = int((25/100)*127)
        command = bytes([val+1])
        command2 = bytes([val+127+64])
        ser.write(command)
        ser.write(command2)
        duration = duration*3 *0.0088*(90/106.7)*(90/96.6)
        while(duration >= 0):
            time.sleep(0.01)
            duration -= 0.01
    elif direction == "left":
        print("turning left")
        val = int((25/100)*127)
        command = bytes([val+64])
        command2 = bytes([val+127+1])
        ser.write(command)
        ser.write(command2)
        duration = duration*3*0.0088*(90/106.7)*(90/96.6)
        while(duration >= 0):
            time.sleep(0.01)
            duration -= 0.01
    else:
        print("Invalid direction command: {}".format(direction))
    ser.write(b'\x00')

def measure_distance(TRIG_PIN, ECHO_PIN):
    # send a pulse to the sensor
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # measure the time it takes for the pulse to bounce back
    start_time = time.time()
    pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        if time.time() - start_time > 0.1:
            return -1
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        if time.time() - start_time > 0.1:
            return -1
        pulse_end = time.time()

    # calculate distance in inches
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 16880.486
    distance = round(distance, 2)

    return distance


def get_sensor_readings():
    """Acquire the sensor distance data and return as a list"""
    # sensor readings were at 0.1, trying larger value
    sleep_time = 0.1
    # this wont take parameters since the sensor readings will be done by actual hardware and corresponding func calls
    L2 = measure_distance(33, 35)  # was L2 (3, 5)
    time.sleep(sleep_time)

    L1 = measure_distance(11, 13)
    time.sleep(sleep_time)

    M = measure_distance(19, 21)
    time.sleep(sleep_time)

    R1 = measure_distance(29, 31)
    time.sleep(sleep_time)

    R2 = measure_distance(3, 5)  # was R2 (33, 35)
    time.sleep(sleep_time)
    print(f"L2: {L2}, L1: {L1}, M: {M}, R1: {R1}, R2: {R2}")
    return np.array([L2, L1, M, R1, R2])

def find_min_max_dist():
    """Returns a list of indices for min and max distances seen by sensors"""
    distance_arr = get_sensor_readings()  # actual func call wont have parameters
    # find the shortest distance from the sensor readings and get idx
    min_idx = np.argmin(distance_arr)  # the closer distance is of immediate concern
    # find the longest distance from the sensor readings and get idx
    max_idx = np.argmax(distance_arr)
    # dictionary for the sensors based on idx
    casename_dictionary = {0: 'L2', 1: 'L1', 2: 'M', 3: 'R1', 4: 'R2'}
    min_dist_sensor = casename_dictionary[min_idx]
    max_dist_sensor = casename_dictionary[max_idx]

    return [min_dist_sensor, max_dist_sensor]


def direction_determination():
    """Identify and return the direction the rover needs to turn to based on sensor readings"""
    # actual function wont have parameters, this is for testing
    # unpack min and max distances
    min_max_dist = find_min_max_dist()
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


def obstacle_avoidance():
    """Sub routine triggered by nearby obstacle(s), determines navigation for obstacle avoidance and returns movement"""
    return direction_determination() 


def oa_threshold(threshold_dist = 50):
    sensor_check = get_sensor_readings()
    print(type(sensor_check))
    #threshold = 100 # threshold distance to initiate OA procedure
    print('DEBUG:', np.any(sensor_check < threshold_dist))
    return np.any(sensor_check < threshold_dist)

# def obstacle_avoidance():
#     """Sub routine triggered by nearby obstacle(s), determines navigation for obstacle avoidance and returns movement"""
#     case_class = case_classification()  # actual func call wont have parameters
#     return case_class
def avoidance():
    checker = False
    array = get_sensor_readings()
    for element in array:
        if element <= 100:
            checker = True
    if checker == True:
        direction = obstacle_avoidance()
    else:
        direction = "straight"
    time.sleep(1)
    print(direction)
    return direction

# while True:
#     obj = oa_threshold()
#     print(obj)
    #while obj != 'straight':
    #    if(obj == 'left'):
    #        #execute_command('left',15, ser)
    #        print("left")
    #    elif obj =='hard left':
    #        #execute_command('left', 15, ser)
    #        print("left")
    ##    elif obj =='right':
    #        #execute_command('right', 15, ser)
    #        print("right")
    #    elif obj =='hard right':
    #        #execute_command('right', 15, ser)
    #        print("hard right")
    #    elif obj =='mid hard left':
    #        #execute_command('left', 15, ser)
    #        print("mid hard left")
    #    elif obj == 'mid hard right':
    #        print("mid hard right")
    #        #execute_command('right', 15, ser)
    #    obj = avoidance()
    ##execute_command('fwd', 1, ser)
    #print("going forward")

direction_degree_dict = {'hard left': -18, 'left': -13, 'right': 13, 'hard right': 18,
                         'mid hard left': -22, 'mid left': -20, 'mid right': 20, 'mid hard right': 22}
#mid hard variables too large, turns too far

while True:
    
    if oa_threshold():
        direction = obstacle_avoidance()
        print(direction)
        angle = direction_degree_dict[direction]
        print('The angle to turn based on direction:', angle)
        #if(angle > 0):
            #execute_command('right', angle, ser)
        #elif(angle < 0):
            #execute_command('left', angle*-1, ser)
    else:
        print('CANNOT SEE OBSTACLES IN PATH)
    time.sleep(0.1)

ser.close()