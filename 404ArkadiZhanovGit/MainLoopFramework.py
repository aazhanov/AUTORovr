import haversine as havsin
import requests
import numpy as np
import RPi.GPIO as GPIO
#import movement as move
import time
import serial
import re

# MICROCONTROLLER SETUP ################################################################################################
# Setting pin read type
GPIO.setmode(GPIO.BOARD)

# Trigger (Out)
GPIO.setup(3, GPIO.OUT)   # L2
GPIO.setup(11, GPIO.OUT)  # L1
GPIO.setup(19, GPIO.OUT)  # M
GPIO.setup(29, GPIO.OUT)  # R1
GPIO.setup(33, GPIO.OUT)  # R2

# Echo (In)
GPIO.setup(5, GPIO.IN)   # L2
GPIO.setup(13, GPIO.IN)  # L1
GPIO.setup(21, GPIO.IN)  # M
GPIO.setup(31, GPIO.IN)  # R1
GPIO.setup(35, GPIO.IN)  # R2

# Serial Ports
gps = serial.Serial('/dev/ttyUSB2', 9600)
ser = serial.Serial('/dev/ttyS0', 9600)


# OBSTACLE AVOIDANCE PROCEDURES ########################################################################################
def measure_distance(TRIG_PIN, ECHO_PIN):
    """Returns distance measured by ultrasonic sensor"""
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
    # this wont take parameters since the sensor readings will be done by actual hardware and corresponding func calls
    L2 = measure_distance(33, 35)  # was L2 (3, 5)
    time.sleep(0.1)
    L1 = measure_distance(11, 13)
    time.sleep(0.1)
    M = measure_distance(19, 21)
    time.sleep(0.1)
    R1 = measure_distance(29, 31)
    time.sleep(0.1)
    R2 = measure_distance(3, 5)  # was R2 (33, 35)
    time.sleep(0.1)

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
        elif max_dist_sensor == 'L1':
            print('mid left')
            direction = 'mid left'
        elif max_dist_sensor == 'R1':
            print('mid right')
            direction = 'mid right'
        elif max_dist_sensor == 'R2':
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


def oa_threshold(threshold_dist=50):
    """A boolean check for whether an obstacle is in a threshold proximity of the rover"""
    sensor_check = get_sensor_readings()
    print(type(sensor_check))
    # threshold = 100 # threshold distance to initiate OA procedure

    return np.any(sensor_check < threshold_dist)


# END OF OBSTACLE AVOIDANCE PROCEDURES #################################################################################

# NAVIGATION PROCEDURES ################################################################################################
def get_GPS(gps):
    test = 0
    if (test == 1):
        print("GPS CALLED, SENDING BACK TEST VALUE")
        return 30.620655, -96.340033
    command = 'AT\r\n'
    gps.write(command.encode())
    time.sleep(0.1)
    command = 'AT+CGPS=1,1\r\n'
    gps.write(command.encode())
    check = 0
    command = 'AT+CGPSINFO\r\n'
    gps.write(command.encode())
    while check != 'N':
        command = 'AT+CGPSINFO\r\n'
        gps.write(command.encode())
        time.sleep(1)
        GPSDATA = gps.read_all().decode('utf-8')
        # print(GPSDATA)
        output = GPSDATA.split('\n')
        # print(output)
        try:
            output = output[1]
            match = re.search(r'(\d+)(\d{2}\.\d+),\s*([NS]),\s*(\d+)(\d{2}\.\d+),\s*([EW])', output)
            if match:
                latitude_degrees = int(match.group(1))
                latitude_minutes = float(match.group(2))
                if match.group(3) == 'S':
                    latitude_degrees *= -1
                longitude_degrees = int(match.group(4))
                longitude_minutes = float(match.group(5))
                if match.group(6) == 'W':
                    longitude_degrees *= -1

                # Convert to proper latitude and longitude format
                latitude = latitude_degrees + latitude_minutes / 60
                longitude = abs(longitude_degrees) + longitude_minutes / 60
                if match.group(6) == 'W':
                    longitude = -longitude

                # Print the latitude and longitude
                # print(f"{latitude}, {longitude}")
                latitude += -2.76833 * 10 ** (-5)
                latitude -= 0.000045
                longitude += 9.8 * 10 ** (-6)
                longitude += 0.00003
                return latitude, longitude

        except:
            print("Searching for GPS")


def execute_command(direction, duration, ser):
    # speed is 120 meters a minute or 2 meters per second
    if direction == "fwd":
        val = int(31)
        command = bytes([val + 64])
        command2 = bytes([(val + 127 + 64)])
        ser.write(command)
        ser.write(command2)
        duration *= (0.5 * (100 / 93) * (3 / 2.7))
        while duration >= 0:
            time.sleep(0.01)
            duration -= 0.01
            # check for OA here
            if oa_threshold():  # check for obstacle
                ser.write(b'\x00')  # stops motors
                time.sleep(0.1)  # maybe keep, need to test
                return True
            duration -= process_time_for_OA  # subtract the process time for OA to account for time lost during oa_threshold
        ser.write(b'\x00')  # stops motors
        return False

    elif direction == "right":
        val = int((25 / 100) * 127)
        command = bytes([val + 1])
        command2 = bytes([val + 127 + 64])
        ser.write(command)
        ser.write(command2)
        duration = duration * 3 * 0.0088 * (90 / 106.7) * (90 / 96.6)
        while (duration >= 0):
            time.sleep(0.01)
            duration -= 0.01

    elif direction == "left":
        val = int((25 / 100) * 127)
        command = bytes([val + 64])
        command2 = bytes([val + 127 + 1])
        ser.write(command)
        ser.write(command2)
        duration = duration * 3 * 0.0088 * (90 / 106.7) * (90 / 96.6)
        while (duration >= 0):
            time.sleep(0.01)
            duration -= 0.01
            time.sleep(0.01)
            duration -= 0.01

    else:
        print("Invalid direction command: {}".format(direction))
    ser.write(b'\x00')


def calc_turn(curr_angle, ideal_angle):
    curr_angle = curr_angle % 360
    ideal_angle = ideal_angle % 360
    angle_diff = ideal_angle - curr_angle
    if angle_diff > 180:
        angle_diff -= 360
    elif angle_diff < -180:
        angle_diff += 360

    return angle_diff


# NAVIGATION AND OBSTACLE AVOIDANCE PROCEDURE ##########################################################################
def node_seeker(ser, gps, datapath):
    print("start")
    self_angle = 0
    angle_to_node = 0
    current_angle = 0
    gps_record = []  # gps list recording

    print("getting nodes")
    for i in range(len(datapath)):
        curr0, curr1 = get_GPS(gps)
        print("getting GPS")
        destination_lat = datapath[i][1]
        destination_lon = datapath[i][0]
        print(f"seeing node {i} {destination_lat} {destination_lon}")
        distance_to_node, angle_from_north, angle_difference = havsin.haversine_with_angle(curr0, curr1,
                                                                                           destination_lat,
                                                                                           destination_lon, self_angle)
        print(f"getting distance to node: {distance_to_node}")

        # dictionary for converting direction to correct degree
        direction_degree_dict = {'hard left': -18, 'left': -13, 'right': 13, 'hard right': 18,
                                 'mid hard left': -22, 'mid left': -20, 'mid right': 20, 'mid hard right': 22}

        while distance_to_node > 2:  # check distance of rover to next node
            # OBSTACLE AVOIDANCE GOES HERE TO CHECK FOR CLEARANCE BEFORE MOVING
            while oa_threshold():  # check if threshold is breached by an obstacle
                direction = obstacle_avoidance()  # get direction to turn into
                print(direction)
                angle = direction_degree_dict[direction]  # get subsequent angle based on direction
                print('The angle to turn based on direction:', angle)
                if angle > 0:  # positive angle check
                    execute_command('right', angle, ser)
                elif angle < 0:  # negative angle check
                    angle *= -1
                    execute_command('left', angle, ser)

            ##################################################################
            print(f"Seeking node:  {i + 1} at {destination_lat} {destination_lon}")
            prev0, prev1 = get_GPS(gps)

            if (execute_command('fwd', 2, ser) == False):  # if obstacle not seen
                # execute_command('fwd', 2, ser)  # 10 sec , obstacle detected, inerrurpt
                time.sleep(0.5)
                curr0, curr1 = get_GPS(gps)

                # for gps recording
                gps_rec_tup = (curr0, curr1)
                gps_record.append(gps_record)

                distance_moved, self_angle, angle_difference = havsin.haversine_with_angle(prev0, prev1, curr0, curr1,
                                                                                           current_angle)
                print(f"distance change {distance_moved}, current angle {self_angle}\n")
                distance_to_node, angle_from_north, angle_difference = havsin.haversine_with_angle(curr0, curr1,
                                                                                                   destination_lat,
                                                                                                   destination_lon,
                                                                                                   self_angle)
                print(f"distance to current node {distance_to_node}, node AFN {angle_from_north}\n")
                turn = calc_turn(self_angle, angle_from_north)
                print(f"angle shift by {turn} degrees")

                if (turn > 15):
                    execute_command('right', turn, ser)
                    print(f"adjusting angle, by {turn} degrees right")
                if (turn < -15):
                    execute_command('left', -1 * turn, ser)
                    print(f"adjusting angle by {turn * -1} left")
                print(f"/n")
            else:
                curr0, curr1 = get_GPS(gps)
                self_angle = 0
                distance_to_node, angle_from_north, angle_difference = havsin.haversine_with_angle(curr0, curr1,
                                                                                                   destination_lat,
                                                                                                   destination_lon,
                                                                                                   self_angle)
        print(f"arrived at node {i + 1}\n")
        print(f"\n")

    return gps_record  # return what the GPS recorded for error comparison


# TESTING HERE #########################################################################################################
# Input data here for experimentation
# datapath = [[-96.33988211666667, 30.6204847], [-96.3399373, 30.6205297], [-96.3398821, 30.6205739], [-96.3398526, 30.620548], [-96.339795, 30.6204993]]
# datapath = [[-96.34004, 30.62065], [-96.34010, 30.62061], [-96.34005, 30.62058], [-96.34000, 30.62062]]
# datapath = [[-96.33931, 30.62061], [-96.33963, 30.62064], [-96.33968, 30.62056], [-96.33941, 30.62051], [-96.33928, 30.62054]]
datapath = [[-96.3400910, 30.6204001]]

# node_seeker(gps, ser, datapath)

print(node_seeker(ser, gps, datapath))
# print(f"{calc_turn(247, 26)}")
ser.close()
gps.close()
