# Loop to test whether we go into obstacle avoidance
print('In OA test: before import')
import OBJ_AVOID_TEST as OAtest
import serial
import time
import numpy as np

ser = serial.Serial('/dev/ttyS0', 9600)


def oa_threshold(threshold_dist=100):
    sensor_check = OAtest.get_sensor_readings()
    print(type(sensor_check))
    # threshold = 100 # threshold distance to initiate OA procedure
    return np.any(sensor_check < threshold_dist)


def main_control():
    threshold_dist = 100
    direction = 'straight'
    distance = 10
    # contrinue on to main path
    while True:
        while not oa_threshold():
            print('main path')
            direction = 'straight'
            OAtest.execute_command('fwd', 1, ser)
            distance -= 1
            if (distance == 0):
                print("finished run")
                return 0

        if (oa_threshold()):
            print('obstacle avoidance', OAtest.obstacle_avoidance())
            direction = OAtest.obstacle_avoidance()
            if (direction == 'left'):
                OAtest.execute_command('left', 5, ser)
            if (direction == 'hard left'):
                OAtest.execute_command('left', 15, ser)
            if (direction == 'right'):
                OAtest.execute_command('right', 5, ser)
            if (direction == 'hard right'):
                OAtest.execute_command('right', 15, ser)


main_control()

print('End of OA test')

ser.close()
# sensor_check = OAtest.get_sensor_readings()