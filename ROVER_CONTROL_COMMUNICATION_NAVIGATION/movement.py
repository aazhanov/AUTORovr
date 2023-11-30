import time
import serial
import csv
import requests


# The purpose of this code is to test whether or not the rover can be given instructions from a .csv file
ser = serial.Serial('/dev/ttyS0', 9600)

def execute_command(direction, duration, ser):
    #speed is 120 meters a minute or 2 meters per second
    if direction == "fwd":
        #print("going forwards")
        val = int(15)
        command = bytes([val+64])
        command2 = bytes([(val+127+64)])
        ser.write(command)
        ser.write(command2)
        duration*=(0.5*(100/93)*(3/2.7)*2)
        while(duration >= 0):
            time.sleep(0.01)
            #FM = measure_distance(17,23)
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
            #BL = measure_distance(B,L)
            duration -= 0.1

        ser.write(b'\x00')
    elif direction == "right":
        #print(f"going right {duration} degrees")
        val = int(31)
        command = bytes([val+1])
        command2 = bytes([val+127+64])
        #print(command, command2)
        ser.write(command)
        ser.write(command2)
        duration = duration*3*0.0088*(90/106.7)*(90/96.6)
        #print(f"turning right {duration} degrees")
        while(duration >= 0):
            time.sleep(0.01)
            #RF = measure_distance(6,16)
            duration -= 0.01
            #time.sleep(0.1)
            #RB = measure_distance(13,20)
            #duration -= 0.1
            #if(RF or RB < 30):
            #    ser.write(b'\x00')  # Calculate the time it takes to turn right by x degrees
    elif direction == "left":
        #print(f"going left {duration} degrees")
        val = int(45)
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

def grass(ser):
    execute_command('fwd', 1, ser)
    time.sleep(1)
    execute_command('left', 180, ser)

   
grass(ser)#grass(ser)
ser.write(b'\x00')

ser.close()