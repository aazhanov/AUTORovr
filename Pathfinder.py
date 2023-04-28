import pandas as pd
import geopandas as gpd
import osmnx as ox
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
import itertools  # added
from shapely.geometry import LineString, Point, Polygon
from math import radians, sin, cos, sqrt, atan2

# COORDINATES
# # Zach Lat / Long (START)
# zach_lat, zach_lon = 30.621289494918237, -96.34037747550609  # N, W
# # Kyle Field Lat / Long (END)
# kyle_lat, kyle_lon = 30.61034118687136, -96.34009337550648  # S, E
# #n, w, s, e = zach_lat, zach_lon, kyle_lat, kyle_lon
# bbox = [n, s, e, w]

# setup and config
ox.config(log_console=True, use_cache=True)


def route_nodes_to_list(path_nodes):
    """Converts a path nodes GeoDataFrame to a NumPy array and returns it"""
    # get astar_route_nodes and djikstra_route_nodes
    new_coordinate = pd.DataFrame(path_nodes[['lon', 'lat']])
    # new_coordinate = new_coordinate[['lat', 'lon']]
    new_index = list(range(0, len(new_coordinate)))
    # rename the node number index
    new_coordinate['num'] = new_index  # create a new column with indices ranging from 0 to # of nodes
    new_coordinate = new_coordinate.set_index('num')  # create a new DataFrame object with original indices replaced
    coordinate_arr = new_coordinate.to_numpy()  # convert DataFrame object to NumPy array
    # print("Coordinate path array:")
    # print(coordinate_arr)
    return coordinate_arr


def coordinates_to_distance(coordinate_arr):
    """Converts an array of coordinates to a total distance"""
    distance = 0
    R = 6371  # Radius of the Earth in kilometers
    coordinate_length = len(coordinate_arr)
    # print(coordinate_length)
    for i in range(coordinate_length - 1):
        coord1 = coordinate_arr[i]
        coord2 = coordinate_arr[i + 1]
        # print(coord1, " ", coord2)
        lon1 = coord1[0]
        lat1 = coord1[1]
        # print("coord1: ", "lat:", lat1, "lon:", lon1)
        lon2 = coord2[0]
        lat2 = coord2[1]
        # print("coord2: ", "lat:", lat2, "lon:", lon2)
        # convert lat and lon to radians
        lon1, lat1, lon2, lat2 = radians(lon1), radians(lat1), radians(lon2), radians(lat2)
        # differences in lat and lon
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        # Haversine formula
        square_half_chord_len = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        ang_dist = 2 * atan2(sqrt(square_half_chord_len), sqrt(1 - square_half_chord_len))
        distance += (R * ang_dist)
    # print("calulated distance: ", distance)
    return distance


def bbox_generator():
    """Return map coord bounds"""
    # CREATE MAP BOUNDARY ENVELOPING KNOWN TEST AREAS
    # use a centroid between test areas and create all encompassing map from that
    # centroid near : ENGINEERING ACTIVITIES BUILDING A
    centroid_lat, centroid_lon = 30.61588, -96.33713

    centroid_lat_adjustment = 0.002
    centroid_lat += centroid_lat_adjustment

    centroid_lon_adjustment = 0.003
    centroid_lon += centroid_lon_adjustment

    adjustment = 0.01  # degrees which correspond to km
    lat_max = centroid_lat + adjustment  # N
    lat_min = centroid_lat - adjustment  # S
    lon_max = centroid_lon + adjustment  # E
    lon_min = centroid_lon - adjustment  # W

    lon_adjustment = 0.002
    lon_max -= lon_adjustment  # move left by making more negative
    lon_min += lon_adjustment  # move right by making less negative

    n, s, e, w = lat_max, lat_min, lon_max, lon_min
    bbox = [n, s, e, w]
    return bbox


def euclidian_distance(neighborID, targetID):
    """Returns Euclidian distance between two pairs of coordinates (points)"""
    x1 = graph_nodes.x[neighborID]
    y1 = graph_nodes.y[neighborID]
    x2 = graph_nodes.x[targetID]
    y2 = graph_nodes.y[targetID]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def coordinate_input_and_point_conversion(start_point, target_point):
    # INPUTTING COORDINATES ###############################################################
    """Input start and target destination and return a list of Point converted GeoDataFrame"""
    # current position of rover = start location, and user inputs target destination
    # need to convert location points to geodataframes to be used for spatial operations
    # start_point = (start_lon, start_lat)
    # target_point = (target_lon, target_lat)

    # create a column with a geometry label to store the location via a Point class object (representing lat,lon)
    current_location = gpd.GeoDataFrame(columns=['y', 'x', 'street_count', 'lon', 'lat', 'highway', 'geometry'],
                                        crs='EPSG:4326', geometry='geometry')
    current_location.at[0, 'y'] = start_point[1]  # start_lat
    current_location.at[0, 'x'] = start_point[0]  # start_lon
    current_location.at[0, 'street_count'] = 0  # temp
    current_location.at[0, 'lon'] = start_point[0]  # start_lon
    current_location.at[0, 'lat'] = start_point[1]  # start_lat
    current_location.at[0, 'highway'] = 'nan'
    current_location.at[0, 'geometry'] = Point(start_point)  # x,y : lon, lat

    target_location = gpd.GeoDataFrame(columns=['y', 'x', 'street_count', 'lon', 'lat', 'highway', 'geometry'],
                                       crs='EPSG:4326', geometry='geometry')
    target_location.at[1, 'y'] = target_point[1]  # target_lat
    target_location.at[1, 'x'] = target_point[0]  # target_lon
    target_location.at[1, 'street_count'] = 0  # temp
    target_location.at[1, 'lon'] = target_point[0]  # target_lon
    target_location.at[1, 'lat'] = target_point[1]  # target_lat
    target_location.at[1, 'highway'] = 'nan'
    target_location.at[1, 'geometry'] = Point(target_point)  # x,y : lon, lat

    converted_point_gdf = [current_location, target_location]
    return converted_point_gdf


def initialize_map_and_plot(start_point, target_point):
    global graph_nodes  # make available for A* Heuristic
    """get graph walkable paths"""
    # INPUTTING COORDINATES ###############################################################
    """Input start and target destination"""
    # current position of rover = start location, and user inputs target destination
    # need to convert location points to geodataframes to be used for spatial operations
    # EXAMPLE SETUP : conv_points = coordinate_input_and_point_conversion(zach_lat, zach_lon, kyle_lat, kyle_lon)

    # INPUTTING COORDINATES ###############################################################
    # Input start and target destination
    # current position of rover = start location, and user inputs target destination
    # need to convert location points to geodataframes to be used for spatial operations

    conv_points = coordinate_input_and_point_conversion(start_point, target_point)
    # assign conv points to current and target location from returned list
    current_location = conv_points[0]  # type : gdf
    target_location = conv_points[1]  # type : gdf
    # assign conv points to current and target location from returned list
    current_location = conv_points[0]  # type : gdf
    target_location = conv_points[1]  # type : gdf

    bbox = bbox_generator()  # get bbox
    # QUERY GRAPH ########################################################################
    graph = ox.graph_from_bbox(*bbox,
                               network_type='walk',
                               retain_all=True,
                               simplify=True)

    # FIND GEOMETRIES #####################################################################
    # Find grass/parks, parking lots, bodies of water, and buildings
    # Green area GeoDataFrame
    tags1 = {'leisure': 'park', 'landuse': 'grass'}  # Key val pairs for parks and grass
    green_area = ox.geometries_from_bbox(*bbox, tags1)  # gets park/grass nodes

    # Parking/Parking Lot area GeoDataFrame
    tags2 = {'parking': True, 'parking': 'surface'}
    parking_area = ox.geometries_from_bbox(*bbox, tags2)  # get parking lot nodes

    # Water area GeoDataFrame
    tags3 = {'natural': 'water'}
    water_area = ox.geometries_from_bbox(*bbox, tags3)  # get water nodes

    # Building area GeoDataFrame
    tags4 = {'building': True}
    building_area = ox.geometries_from_bbox(*bbox, tags4)

    # POPULATE GEOMETRY WITH NODES
    # identify geometries of interest : Aggie Park, lot in front of WEB
    # 182 green geoms
    # AGGIE PARK HAS INDEX 3
    aggie_park = green_area.geometry.iloc[3]
    # web parking consists of 2 lots
    # WEB LOT has index 15 and 19
    web_lot1 = parking_area.geometry.iloc[19]
    web_lot2 = parking_area.geometry.iloc[15]

    # convert to gdf in order to plot
    aggie_park_gdf = gpd.GeoDataFrame(columns=['geometry'], crs='EPSG:4326', geometry='geometry')
    aggie_park_gdf.at[0, 'geometry'] = aggie_park  # x,y : lon, lat

    web_lot1_gdf = gpd.GeoDataFrame(columns=['geometry'], crs='EPSG:4326', geometry='geometry')
    web_lot1_gdf.at[0, 'geometry'] = web_lot1  # x,y : lon, lat

    web_lot2_gdf = gpd.GeoDataFrame(columns=['geometry'], crs='EPSG:4326', geometry='geometry')
    web_lot2_gdf.at[0, 'geometry'] = web_lot2  # x,y : lon, lat

    # GETTING NODES IN GEOMETRY ##########################################################
    # graph_nodes = ox.graph_to_gdfs(graph, edges=False)
    # nodes_in_polygon = graph_nodes[graph_nodes.within(aggie_park_gdf)]
    # print("Nodes in poly: ", nodes_in_polygon)

    # ADDING NODES TO GEOMETRY
    id_count = 2  # start at 2
    edge_count_id = 2  # start at 2
    # adding helpful points to agpark geometry from aggiemap (starting from top left of water, going around water)
    # points are obtained from AggieMap

    # outer loops left and through bridge
    agpark_points_outerloop_bridge = [(30.61014, -96.33813), (30.61021, -96.33785), (30.61021, -96.33785),
                                      (30.61012, -96.33755), (30.61004, -96.33742), (30.60999, -96.33741),
                                      (30.60995, -96.33738), (30.60995, -96.33733), (30.60991, -96.33729),
                                      (30.60982, -96.33719), (30.60982, -96.33719), (30.60969, -96.33709),
                                      (30.60967, -96.33712), (30.60964, -96.33717), (30.60962, -96.33721),
                                      (30.60956, -96.33731), (30.60950, -96.33743), (30.60944, -96.33754),
                                      (30.60952, -96.33764), (30.60959, -96.33769), (30.60963, -96.33777),
                                      (30.60963, -96.33786), (30.60965, -96.33795), (30.60969, -96.33803),
                                      (30.60976, -96.33809), (30.60985, -96.33812), (30.60991, -96.33816),
                                      (30.60997, -96.33814), (30.61011, -96.33815)]
    agpark_length1 = len(agpark_points_outerloop_bridge)

    # first node is by the top of bridge, the last node is by the end of the bridge
    agpark_points_outerloop_right = [(30.60971, -96.33694), (30.60965, -96.33682), (30.60958, -96.33677),
                                     (30.60953, -96.33670), (30.60953, -96.33658), (30.60954, -96.33645),
                                     (30.60940, -96.33644), (30.60932, -96.33644), (30.60924, -96.33644),
                                     (30.60917, -96.33643), (30.60909, -96.33643), (30.60901, -96.33642),
                                     (30.60880, -96.33641), (30.60880, -96.33663), (30.60881, -96.33683),
                                     (30.60886, -96.33714), (30.60892, -96.33732), (30.60899, -96.33745),
                                     (30.60904, -96.33741), (30.60911, -96.33738), (30.60916, -96.33738),
                                     (30.60924, -96.33742), (30.60929, -96.33750), (30.60935, -96.33753),
                                     (30.60942, -96.33753)]
    agpark_length2 = len(agpark_points_outerloop_right)

    # for loop to place nodes for agpark outerloop and bridge
    for i in range(agpark_length1):
        # print(agpark_points_outerloop_bridge[i])
        p = agpark_points_outerloop_bridge[i]
        # print(p)
        graph.add_node(id_count, x=p[1], y=p[0])
        id_count += 1

    # for loop to connect agpark outerloop and bridge nodes with edges
    for j in range(agpark_length1 - 1):
        graph.add_edge(edge_count_id, edge_count_id + 1)  # direction 1
        graph.add_edge(edge_count_id + 1, edge_count_id)  # direction 2
        edge_count_id += 1
        if j == agpark_length1 - 2:
            graph.add_edge(edge_count_id, 2)  # direction 1
            graph.add_edge(2, edge_count_id)  # direction 2
            edge_count_id += 1

    # for loop to place nodes for agpark right outerloop
    for i in range(agpark_length2):
        p = agpark_points_outerloop_right[i]
        graph.add_node(id_count, x=p[1], y=p[0])
        id_count += 1

    # connect bridge to start of second loop
    graph.add_edge(13, edge_count_id)  # direction 1
    graph.add_edge(edge_count_id, 13)  # direction 2

    # for loop to connect agpark right outerloop nodes with edges
    for j in range(agpark_length2 - 1):
        graph.add_edge(edge_count_id, edge_count_id + 1)  # direction 1
        graph.add_edge(edge_count_id + 1, edge_count_id)  # direction 2
        edge_count_id += 1

    # connect end of second loop to end of bridge area
    graph.add_edge(edge_count_id, 19)  # direction 1
    graph.add_edge(19, edge_count_id)  # direction 2

    # connect right loop, to straight walk path
    graph.add_edge(36, ox.nearest_nodes(graph, -96.3364534, 30.6094822))  # direction 1
    graph.add_edge(ox.nearest_nodes(graph, -96.3364534, 30.6094822), 36)  # direction 2

    # connect left loop to nearest walk path
    graph.add_edge(27, ox.nearest_nodes(graph, -96.338304, 30.609777))  # direction 1
    graph.add_edge(ox.nearest_nodes(graph, -96.338304, 30.609777), 27)  # direction 2

    # connect left loop to nearest walk path
    graph.add_edge(27, ox.nearest_nodes(graph, -96.338663, 30.610175))  # direction 1
    graph.add_edge(ox.nearest_nodes(graph, -96.338663, 30.610175), 27)  # direction 2

    # connect left loop to nearest walk path
    graph.add_edge(43, ox.nearest_nodes(graph, -96.3364347, 30.6088328))  # direction 1
    graph.add_edge(ox.nearest_nodes(graph, -96.3364347, 30.6088328), 43)  # direction 2

    # # VALIDATION : validating that nodes and edges placed by network run
    # # custom nodes/edges for WEB lot : VALIDATE that paths go between parking spaces
    # weblot_points = [(30.62255, -96.33709), (30.62169, -96.33605), (30.62157, -96.33618), (30.62244, -96.33722),
    #                  (30.62232, -96.33736), (30.62145, -96.33631), (30.62132, -96.33643), (30.62221, -96.33749),
    #                  (30.62203, -96.33768), (30.62116, -96.33662), (30.62104, -96.33676), (30.62193, -96.33782),
    #                  (30.62183, -96.33797), (30.62121, -96.33723), (30.62107, -96.33740), (30.62170, -96.33816),
    #                  (30.62157, -96.33830), (30.62094, -96.33753)]
    # weblot_points_length = len(weblot_points)
    #
    # # for loop to place nodes for web lot
    # for i in range(weblot_points_length):
    #     p = weblot_points[i]
    #     graph.add_node(id_count, x=p[1], y=p[0])
    #     id_count += 1
    #
    # edge_count_id += 1
    # # for loop to weblot nodes with edges
    # for j in range(weblot_points_length - 1):
    #     graph.add_edge(edge_count_id, edge_count_id + 1)  # direction 1
    #     graph.add_edge(edge_count_id + 1, edge_count_id)  # direction 2
    #     edge_count_id += 1

    # CREATE AND ADD EDGES FOR INPUT ###############################################################
    # process inputs after custom node population
    # find nearest nodes to start and target nodes and connect with an edge
    node_id_nearest_to_start = ox.nearest_nodes(graph, start_point[0], start_point[1])
    node_id_nearest_to_target = ox.nearest_nodes(graph, target_point[0], target_point[1])

    # INSERT START / TARGET NODES HERE ###################################################
    # add nodes to the MultiDiGraph
    # start_node_id = 0  # start 0
    # start_lon = start_point[0]
    # start_lat = start_point[1]
    # graph.add_node(node_id, x=start_lon, y=start_lat)
    graph.add_node(0, x=start_point[0], y=start_point[1])  # add start node
    graph.add_node(1, x=target_point[0], y=target_point[1])  # add end node

    # connect inputs to nearest nodes with an edge and MAKE BIDIRECTIONAL
    graph.add_edge(0, node_id_nearest_to_start)  # direction 1
    graph.add_edge(node_id_nearest_to_start, 0)  # direction 2

    graph.add_edge(1, node_id_nearest_to_target)  # direction 1
    graph.add_edge(node_id_nearest_to_target, 1)  # direction 2

    # PROJECT GRAPH AND GET GDFS EDGES ###################################################
    graph_projection = ox.project_graph(graph, to_crs='crs')  # project crs coordinates of nodes/edges on graph map
    edges = ox.graph_to_gdfs(graph_projection, nodes=False)  # get connections; edges are the node connections

    # get graph (walkway) nodes
    graph_nodes = ox.graph_to_gdfs(graph_projection, edges=False)
    # get CRS from graph edges
    CRS = edges.crs  # get crs of the edges
    # Reproject the nodes on interest using the same crs (coordinate reference system)
    graph_nodes.to_crs(CRS)
    green_area.to_crs(CRS)
    parking_area.to_crs(CRS)
    current_location.to_crs(CRS)  # origin node
    target_location.to_crs(CRS)  # destination node

    # PLOT TEST CASES : AGGIE PARK and WEB LOT
    # VALIDATION OF CORRECT REGIONS
    fig, ax = plt.subplots(figsize=(11, 11))
    edges.plot(ax=ax, color='black', linewidth=0.5, alpha=1, zorder=0)
    green_area.geometry.plot(ax=ax, color='green', linewidth=0.5, alpha=1, zorder=1)
    parking_area.plot(ax=ax, color='#4C4E52', zorder=2)
    aggie_park_gdf.plot(ax=ax, color='red', linewidth=0.5, alpha=1, zorder=3)
    web_lot1_gdf.plot(ax=ax, color='red', linewidth=0.5, alpha=1, zorder=4)
    web_lot2_gdf.plot(ax=ax, color='red', linewidth=0.5, alpha=1, zorder=5)

    # PLOTTING NODES
    fig, ax = plt.subplots(figsize=(11, 11))
    edges.plot(ax=ax, color='black', linewidth=0.5, alpha=1, zorder=0)
    graph_nodes.plot(ax=ax, color='gray', markersize=12, zorder=1)

    # route nodes stored in GeoDatFrame
    # route_nodes = gpd.GeoDataFrame() # IN USE
    djikstra_route_nodes = gpd.GeoDataFrame()  # FOR DEMO
    astar_route_nodes = gpd.GeoDataFrame()  # FOR DEMO

    # the for loops iterate over the origin and destinations
    for current_idx, current in current_location.iterrows():
        # print('current_idx: ', current_idx, 'current: ', current)
        # find closest node ID to location node
        nearest_start_node = ox.nearest_nodes(G=graph_projection, X=current.geometry.x, Y=current.geometry.y)

        # Extract coordinate info from destination node
        for target_idx, target in target_location.iterrows():
            # print('target_idx: ', target_idx, 'target: ', target)
            # find closest node ID from target node
            nearest_target_node = ox.nearest_nodes(G=graph_projection, X=target.geometry.x, Y=target.geometry.y)

            print(nearest_start_node)
            print(nearest_target_node)
            print(graph_nodes.x[nearest_start_node])

            # using networkx djikstra algo to get shortest path
            # shortest_path = nx.dijkstra_path(G=graph_projection, source=nearest_start_node, target=nearest_target_node,
            #                               weight='length')

            astar_shortest_path = nx.astar_path(G=graph_projection, source=nearest_start_node,
                                                target=nearest_target_node,
                                                heuristic=euclidian_distance, weight='cost')

            djikstra_shortest_path = nx.dijkstra_path(G=graph_projection, source=nearest_start_node,
                                                      target=nearest_target_node,
                                                      weight='length')

            # get only the nodes from the shortest path
            # path_nodes = graph_nodes.loc[shortest_path]  # IN USE
            astar_path_nodes = graph_nodes.loc[astar_shortest_path]  # FOR DEMO
            djikstra_path_nodes = graph_nodes.loc[djikstra_shortest_path]  # FOR DEMO
            # reformat path nodes into LineString object
            # nodes_list = LineString(list(path_nodes.geometry.values))  # IN USE
            astar_nodes_list = LineString(list(astar_path_nodes.geometry.values))  # IN DEMO
            djikstra_nodes_list = LineString(list(djikstra_path_nodes.geometry.values))  # IN DEMO
            # append LineString of path nodes into a GeoDataFrame
            # route_nodes = route_nodes.append([[nodes_list]], ignore_index=True)  # has only LineString attribute IN USE!!
            astar_route_nodes = astar_route_nodes.append([[astar_nodes_list]], ignore_index=True)  # FOR DEMO
            djikstra_route_nodes = djikstra_route_nodes.append([[djikstra_nodes_list]], ignore_index=True)  # FOR DEMO

    # Need to convert DataFrame back to GeoDataFrame !!!
    # Give the output nodes column the geometry name to set the geometry
    # route_nodes.columns = ['geometry']  # IN USE
    astar_route_nodes.columns = ['geometry']  # FOR DEMO
    djikstra_route_nodes.columns = ['geometry']  # FOR DEMO

    # Set geometry of the nodes
    # route_nodes = route_nodes.set_geometry('geometry')  # IN USE
    # route_nodes.crs = graph_nodes.crs  # IN USE
    astar_route_nodes = astar_route_nodes.set_geometry('geometry')  # IN USE
    djikstra_route_nodes = djikstra_route_nodes.set_geometry('geometry')  # IN USE

    astar_route_nodes.crs = graph_nodes.crs  # IN USE
    djikstra_route_nodes.crs = graph_nodes.crs  # IN USE

    # TURNING ROUTE INTO A LIST OF NODES ######################################################
    astar_np_array = route_nodes_to_list(astar_path_nodes)
    print("num of nodes in asta: ", len(astar_np_array))

    djikstra_np_array = route_nodes_to_list(djikstra_path_nodes)  # return Djikstra nodes since better algo
    print("num of nodes in djikstra: ", len(djikstra_np_array))
    print(djikstra_np_array)
    # print(djikstra_np_array[0])
    # print(djikstra_np_array[0][0])
    # print(djikstra_np_array[0][1])

    # CONVERT LIST INTO DISTANCES
    # VALIDATION : used google maps to plot similar distances and note the total distance traveled
    astar_distance = coordinates_to_distance(astar_np_array)
    djikstra_distance = coordinates_to_distance(djikstra_np_array)

    # FORMAT STRING FOR PLOT
    # show the total distance taken by the pathfinding algorithms
    astar_str = 'AStar Distance: {} km'.format(astar_distance)
    djikstra_str = 'Djikstra Distance: {} km'.format(djikstra_distance)

    # PLOTTING ############################################################################
    # areas deemed legal for traversal
    # Get plot of walkable pathways, green areas, and parking lots
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(11, 11))
    green_area.plot(ax=ax, color='green', alpha=0.5, zorder=0)
    water_area.plot(ax=ax, color='blue', alpha=0.5, zorder=1)
    building_area.plot(ax=ax, color='tan', zorder=2)
    parking_area.plot(ax=ax, color='#4C4E52', zorder=3)
    edges.plot(ax=ax, color='gray', linewidth=0.5, alpha=1, zorder=4)
    current_location.plot(ax=ax, color='red', markersize=15, zorder=5)
    target_location.plot(ax=ax, color='green', markersize=15, zorder=6)
    # route_nodes.plot(ax=ax, color='red', linewidth=2, zorder=7)  # IN USE
    # djikstra_route_nodes.plot(ax=ax, color='red', linewidth=2, zorder=7, label='Djikstra')  # FOR DEMO
    # astar_route_nodes.plot(ax=ax, color='purple', linewidth=2, zorder=8, label='AStar')  # FOR DEMO
    astar_route_nodes.plot(ax=ax, color='purple', linewidth=2, zorder=7, label=astar_str)  # FOR DEMO
    djikstra_route_nodes.plot(ax=ax, color='red', linewidth=2, zorder=8, label=djikstra_str)  # FOR DEMO
    plt.legend(loc="upper left")  # FOR DEMO
    plt.show()

    return djikstra_np_array


# TEST CASE ; INPUTTING COORDINATES ###################################################
# Zach Lat / Long (START)
zach_lat, zach_lon = 30.621289494918237, -96.34037747550609
zach_point = (zach_lon, zach_lat)
# Kyle Field Lat / Long (END)
kyle_lat, kyle_lon = 30.61034118687136, -96.34009337550648
kyle_point = (kyle_lon, kyle_lat)
# Aggie Park
agpark_lat, agpark_lon = 30.60994, -96.33688
agpark_point = (agpark_lon, agpark_lat)
# Parking Lot 51
lot51_lat, lot51_lon = 30.62178, -96.33698
lot51_point = (lot51_lon, lot51_lat)
# in front of zach
slat, slon = 30.622625, -96.335211
spoint = (slon, slat)
# left corner of lot
lotlat, lotlon = 30.621570, -96.338239 + 0.0001
lotpoint = (lotlon, lotlat)

# TEST POINTS
tlat, tlon = 30.625489, -96.33693
tpoint = (tlon, tlat)

tlat2, tlon2 = 30.622441, -96.33453
tpoint2 = (tlon2, tlat2)

# TEST POINTS
# case 1
tlat, tlon = 30.610188, -96.338237
tpoint = (tlon, tlat)
tlat2, tlon2 = 30.609700, -96.336385
tpoint2 = (tlon2, tlat2)

# case 2
tlat, tlon = 30.610188, -96.338237
tpoint = (tlon, tlat)
tlat2, tlon2 = 30.608673, -96.336615
tpoint2 = (tlon2, tlat2)

# # case 3
# tlat, tlon = 30.622604, -96.337128
# tpoint = (tlon, tlat)
# tlat2, tlon2 = 30.620827, -96.337678
# tpoint2 = (tlon2, tlat2)

# RUN HERE #######################################################
# start_point = tpoint
# target_point = tpoint2
# ax_general = initialize_map_and_plot(start_point, target_point)





# # NODE COLLECTION # INPUTTING COORDINATES #############################################
# """Collecting all legal nodes for creation of node pool from which we path find"""
# # combine graph nodes, green area nodes, and parking lot nodes
# graph_nodes = ox.graph_to_gdfs(graph_projection, edges=False)  # get graph (walkway) nodes
#
# CRS = edges.crs  # get crs of the edges
#
# # Reproject the nodes on interest using the same crs (coordinate reference system)
# graph_nodes.to_crs(CRS)
# green_area.to_crs(CRS)
# parking_area.to_crs(CRS)
# current_location.to_crs(CRS)  # origin node
# target_location.to_crs(CRS)  # destination node
#
# # Store the output nodes into GeoDataFrame


# # Sanity Check : find num of nodes in each node GeoDataFrame
# graph_num_nodes = len(graph_nodes.geometry)  # num nodes
# green_num_nodes = len(green_area.geometry)  # num of polygons
# parking_num_nodes = len(parking_area.geometry)  # num of polygons
#
# # Coordinates of different node containers
# graph_nodes_coords = [coord for geom in graph_nodes.geometry for coord in list(geom.coords)]  # SUCCESS ; gets nodes
# #green_nodes_coords = [coord for geom in green_area.geometry for coord in list(geom.coords)] # polygon obj needs further parsing
# #parking_nodes_coords = [coord for geom in parking_area.geometry for coord in list(geom.coords)]  # polygon obj needs further parsing

# PROCESSING GREEN AREA TO GET NODES
# green_area_geo_obj = green_area.geometry
# print(len(green_area_geo_obj)) # num of POLY objects each of which is described by nodes
# print(green_area_geo_obj[0])
# print(green_area_geo_obj[1])
# print(green_area_geo_obj[100])
# print(green_area_geo_obj[182])
# print(type(green_area_geo_obj[182]))

# for i in range(len(green_area_geo_obj)): # num of polygons
#     curr_green_poly_obj = green_area_geo_obj[i]
#     print('curr_green_poly_obj: ', curr_green_poly_obj)
#     for j in range(len(curr_green_poly_obj)): # num of coords in polygon object
#         curr_green_coord = curr_green_poly_obj[j]

# green_graph = ox.graph_from_polygon(green_area_geo_obj[0], network_type='all')
# green_stuff = gpd.GeoDataFrame(geometry=green_area_geo_obj)
# # green_nodes = green_stuff['geometry'].tolist()
# # gn = green_stuff['geometry'].values
# # green_nodes_within_polygon = green_stuff[green_stuff['geometry'].within(green_stuff.geometry)]
# green_nodes_within_polygon = green_stuff[green_stuff['geometry'].within(green_stuff.geometry)]
# print(type(green_nodes_within_polygon))
# print(green_area.geometry.iloc[0].exterior)

# YOU ARE GETTING A LIST OF GREEN NODES HERE
# markersize if for nodes/dots
# green_nodes = []
# for i, row in green_area.iterrows():
#     if isinstance(row['geometry'], Polygon):
#         green_nodes.extend(list(row['geometry'].exterior.coords))
#         for interior in row['geometry'].interiors:
#             green_nodes.extend(list(interior.coords))
#
#
# # merging the GeoDataFrames of interest to get all nodes / edges (polygons)
# merged_nodes = pd.concat([graph_nodes, green_area, parking_area])
# # merged_nodes_coords = [coord for geom in merged_nodes.geometry for coord in list(geom.coords)]
# # Sanity Check : make sure the merged nodes num equals the sum of their parts
# merged_num_nodes = len(merged_nodes.geometry)


# SHORTEST PATH HERE #####################################
# # Take array of dots and project them
# # graph_proj = ox.project_graph(graph)
# # grap
#
# # Convert projection into a geo-dataframe
# edges = ox.graph_to_gdfs(graph_proj, nodes=False)
#
# # Returns the Coordinate Reference system of the GeoDataFrame area
# CRS = edges.crs
# # Given the pulled CRS type, reproject the user's location and destination onto the same coordinate system of the map
# origin_proj = current.to_crs(crs=CRS)
# destination_proj = destination.to_crs(crs=CRS)
#
# # Create a GeoDataFrame to store the route of the shortest path
# output_nodes = gpd.GeoDataFrame()
#
# # Store all nodes from the graph area without the edge nodes
# graph_nodes = ox.graph_to_gdfs(graph_proj, edges=False)
#
# # Extract coordinate info from origin node
# for oidx, orig in origin_proj.iterrows():
#
#     # Locate the graph node closest to the user's location coordinates
#     # nearest_nodes uses k-d trees to find nearest neighbor
#     nearest_origin_node = ox.nearest_nodes(G=graph_proj, X=orig.geometry.x, Y=orig.geometry.y)
#     # Extract coordinate info from destination node
#     for tidx, target in destination_proj.iterrows():
#         # Locate the graph node closest to the user's destination coordinates
#         # nearest_nodes uses k-d trees to find nearest neighbor
#         nearest_target_node = ox.nearest_nodes(graph_proj, X=target.geometry.x, Y=target.geometry.y)
#
#         # Use dijkstra's algorithm to find the shortest path
#         shortest_path = nx.dijkstra_path(graph_proj,
#                                          source=nearest_origin_node,
#                                          target=nearest_target_node, weight='length')
#
#         # Isolate only the nodes of this shortest path
#         path_nodes = graph_nodes.loc[shortest_path]
#
#         # Format results into a linestring to be used for plotting the shortest path for demo purposes
#         # List the nodes into a linestring so that they can be written into a new GeoDataFrame
#         nodes_list = LineString(list(path_nodes.geometry.values))
#         # Place results into a GeoDataFrame
#         output_nodes = output_nodes.append([[nodes_list]], ignore_index=True)
#
# return path_nodes, output_nodes, graph_nodes, edges, origin_proj, destination_proj


# PLOT THE COMBINED NODES
# """Map of all the nodes representing legal areas for traversal"""
# plt.style.use('seaborn')
# fig_nodes, ax_nodes = plt.subplots(figsize=(11, 11))
# merged_nodes.plot(ax=ax_nodes, color='gray', markersize=5, zorder=0)
# g1.plot(ax=ax_nodes, color='gray', linewidth=0.01, zorder=0)
# plt.show()


# # INPUTTING COORDINATES ###############################################################
#     """Input start and target destination"""
#     # current position of rover = start location, and user inputs target destination
#     # need to convert location points to geodataframes to be used for spatial operations
#     # Zach Lat / Long (START)
#     zach_lat, zach_lon = 30.621289494918237, -96.34037747550609
#     zach_point = (zach_lon, zach_lat)
#     # Kyle Field Lat / Long (END)
#     kyle_lat, kyle_lon = 30.61034118687136, -96.34009337550648
#     kyle_point = (kyle_lon, kyle_lat)
#
#     # create a column with a geometry label to store the location via a Point class object (representing lat,lon)
#     current_location = gpd.GeoDataFrame(columns=['geometry'], crs='EPSG:4326', geometry='geometry')
#     current_location.at[0, 'geometry'] = Point(zach_point)  # x,y : lon, lat
#
#     target_location = gpd.GeoDataFrame(columns=['geometry'], crs='EPSG:4326', geometry='geometry')
#     target_location.at[0, 'geometry'] = Point(kyle_point)
