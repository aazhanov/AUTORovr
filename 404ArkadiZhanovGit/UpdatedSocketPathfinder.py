# socket first then pathfinder
import socket
import time
import FinalizedPathfinder as fp


# # CASE 1
# tlat, tlon = 30.625489, -96.33693
# tpoint = (tlon, tlat)
# tlat2, tlon2 = 30.622441, -96.33453
# tpoint2 = (tlon2, tlat2)
#
# start_point = tpoint
# target_point = tpoint2

######################################
# data comes in as lat long lat long

def coord_parser(string):
    "parses a lat lon lat lon string and turns into coordinates"
    # flipping lat lon
    tokens = string.split()
    start_point = (float(tokens[1]), float(tokens[0]))  # (float(tokens[0]), float(tokens[1]))
    end_point = (float(tokens[3]), float(tokens[2]))  # (float(tokens[2]), float(tokens[3]))
    return start_point, end_point


# IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = ("100.96.1.38", 12345)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server")

    connected = True
    while connected:
        try:
            msg = client.recv(SIZE).decode(FORMAT)
            if msg:
                path = 0
                print(msg)
                print('msg typr:', type(msg))
                # client.send("Test".encode("utf-8")) # test
                # Start pathfinder here
                start_and_end_points = coord_parser(msg)  # parse the input msg strin of coords
                print(start_and_end_points[0], type(start_and_end_points[0]))
                print(start_and_end_points[1], type(start_and_end_points[1]))
                coord_list = fp.pathfinder(start_and_end_points[0],
                                           start_and_end_points[1])  # call pathfinder and get node list
                coord_list_string = str(coord_list)  # coord list converted to string
                print('coord list string:', coord_list_string)
                client.send(coord_list_string.encode("utf-8"))
        except ConnectionResetError:
            print(f"Server disconnected.")
            break
        # print(f"[SERVER] {msg}")


if __name__ == "__main__":
    main()
