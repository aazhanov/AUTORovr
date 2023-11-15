# validate the ultrasonic sensors are working and check the distances measured

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Trigger (Out)
GPIO.setup(3, GPIO.OUT)  # L2
GPIO.setup(11, GPIO.OUT)  # L1
GPIO.setup(19, GPIO.OUT)  # M
GPIO.setup(29, GPIO.OUT)  # R1
GPIO.setup(33, GPIO.OUT)  # R2

# Echo (In)
GPIO.setup(5, GPIO.IN)  # L2
GPIO.setup(13, GPIO.IN)  # L1
GPIO.setup(21, GPIO.IN)  # M
GPIO.setup(31, GPIO.IN)  # R1
GPIO.setup(35, GPIO.IN)  # R2


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


while True:
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

    print("L2:", L2, "L1:", L1, "M:", M, "R1:", R1, "R2:", R2)

    time.sleep(0.1)