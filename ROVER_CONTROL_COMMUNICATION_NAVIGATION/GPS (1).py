import socket
import time
import serial
import csv
from datetime import datetime
import re

# Create a socket object
#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gps = serial.Serial('/dev/ttyUSB2', 9600)
def get_GPS(gps):
    test = 0
    if(test == 1):
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
        #print(GPSDATA)
        output = GPSDATA.split('\n')
        #print(output)
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
            #print(f"{latitude}, {longitude}")
                latitude += -2.76833*10**(-5)
                latitude -= 0.000045
                latitude += 0.00009
                longitude += 9.8*10**(-6)
                longitude += 0.00003
                longitude -= 0.00004
                return latitude, longitude

        except:
            print("Searching for GPS")
    # In this example, we'll simply reverse the received data
    # Send the reversed data back to the client
    #if check == 'N':
    #    client_socket.send(information.encode('utf-8'))
    #print("data sent")
    # Close the client socket
#client_socket.close()

csv_file = 'gps_data.csv'
while True:
    lat, lon = get_GPS(gps)
    print(f"{lat}, {lon}")
    with open(csv_file, 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow([lat, lon])
    time.sleep(1)
#while True:
#    this, that = get_GPS(gps)
#    print(f"{this}, {that}")
gps.close()
