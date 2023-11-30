import math

def haversine_with_angle(lat1, lon1, lat2, lon2, current_angle):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles

    # Calculate distance in kilometers
    distance_km = c * r

    # Convert distance to meters
    distance_meters = distance_km * 1000

    # Calculate the angle from true north
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    angle_from_north = math.atan2(y, x)
    angle_from_north = math.degrees(angle_from_north)
    # Calculate the difference between current_angle and angle_from_north
    if angle_from_north < 0:
        angle_from_north+=360
    angle_difference = angle_from_north - current_angle

    # Adjust angle if counterclockwise
    if angle_difference > 180:
        angle_difference -= 360


    return distance_meters, angle_from_north, angle_difference


# Example list of nodes
#nodes = [
#    (30.62085, -96.33973),  # Example latitude and longitude for the first point
#    (30.62080, -96.33985)# Example latitude and longitude for the second point
    # Add more nodes as needed
#]

#current_angle = 0  # Example value for current_angle
#previous_node = None

#for node in nodes:
#    if previous_node:
##        distance, angle_from_north, angle_difference = haversine_with_angle(
#            previous_node[0], previous_node[1], node[0], node[1], current_angle
#        )
#        print(f"The distance between the two points is {distance} meters.")
#        print(f"The angle from true north is {angle_from_north} degrees.")
#        print(f"The difference between current_angle and angle_from_north is {angle_difference} degrees.")
#        print("\n")
#    previous_node = node
