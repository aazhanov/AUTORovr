import math
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf, linewidth=10000)  # fully prints matrix; full width

# USE NUMPY LISTS FOR STORING DATA SINCE THEY ARE MORE COMPRESSED : maybe
# matrix map will have bounds like pathfinding map


def mile_to_meters(miles):
    """convert miles to meters"""
    return miles * 1609.34


def nearest_meter(meters):
    """get nearest integer meter from float"""
    return math.ceil(meters)


def create_lat_lon_matrix(lat_start, lat_end, lat_step, lon_start, lon_end, lon_step):
    latitudes = np.arange(lat_start, lat_end, lat_step)
    longitudes = np.arange(lon_start, lon_end, lon_step)
    lat_lon_matrix = np.zeros((len(latitudes), len(longitudes)), dtype=[('lat', float), ('lon', float)])
    for i in range(len(latitudes)):
        for j in range(len(longitudes)):
            lat_lon_matrix[i, j] = (latitudes[i], longitudes[j])
    return lat_lon_matrix


def bresenham_line(start_x, start_y, end_x, end_y):
    """creates line trace from cells connecting a start and an end and returns cell array that make the line"""
    dx = abs(end_x - start_x)
    dy = abs(end_y - start_y)
    if start_x < end_x:
        x_slope = 1
    else:
        x_slope = -1

    if start_y < end_y:
        y_slope = 1
    else:
        y_slope = -1
    error = dx - dy
    line_cells = []
    # line_cells = np.empty((0,), dtype=[('x', int), ('y', int)])

    while True:
        line_cells.append((start_x, start_y))
        # line_cells = np.append(line_cells, np.array([(start_x, start_y)], dtype=line_cells.dtype))
        if start_x == end_x and start_y == end_y:
            break
        doubled_error = 2 * error
        if doubled_error > -dy:
            error -= dy
            start_x += x_slope
        if doubled_error < dx:
            error += dx
            start_y += y_slope

    return line_cells


# visualize map and nodes
def visualizer(matrix, max_val):
    """creates and shows a colored NxN trial matrix populated with obstacles"""
    # 0 for free cell, 1 for start, 2 for end, 3 for path
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    fig, ax = plt.subplots()
    # ax.matshow(matrix, cmap='plasma') # prev used

    # plot matrix plot with imshow
    im = ax.imshow(matrix, cmap='plasma')
    # setting origin in bottom left corner
    ax.set_ylim(ax.get_ylim()[::-1])

    for i in range(max_val):
        for j in range(max_val):
            c = matrix[j, i]
            ax.text(i, j, str(c), va='center', ha='center')

    return plt.show()


def matrix_generator(n):
    """returns an NxN matrix"""
    initialized_zero_matrix = np.zeros((n, n), dtype=int)
    return initialized_zero_matrix


def target_cells_populater(target_cell_list, mat):
    """populates a matrix with target path trace nodes, including start, end, and intermediary nodes
    and returns target cell populated matrix"""
    # 0 is a free cell, 1 is start, 2 is end, 3 is intermediary node, 4 is path cell
    list_length = len(target_cell_list)

    for idx, cell in enumerate(target_cell_list):
        row = cell[0]
        col = cell[1]
        if idx == 0:
            mat[row][col] = 1
        elif idx == (list_length - 1):
            mat[row][col] = 2
        else:
            mat[row][col] = 3

    return mat


def cell_paths_generator(target_cell_list):
    """returns combined cell paths used to connect all target cells from start to end"""
    list_length = len(target_cell_list)
    cell_paths = np.empty((0,), dtype=[('x', int), ('y', int)])  # store all cells used in path creation

    for idx, cell in enumerate(target_cell_list):
        if idx == (list_length - 1):
            break
        else:
            cell1 = target_cell_list[idx]
            cell2 = target_cell_list[idx + 1]

            cell1_row = cell1[0]  # get cell1 row
            cell1_col = cell1[1]  # get cell1 col

            cell2_row = cell2[0]  # get cell2 row
            cell2_col = cell2[1]  # get cell2 col

            path = bresenham_line(cell1_row, cell1_col, cell2_row, cell2_col)  # intermediate cell path

            if idx == (list_length - 2):  # include complete path if last path is being generated
                cell_paths = np.append(cell_paths, np.array([path], dtype=cell_paths.dtype))
            else:  # removes duplicate cells that occur as repeated appended target cell by ignoring last cell
                cell_paths = np.append(cell_paths, np.array([path[:-1]], dtype=cell_paths.dtype))

    return cell_paths


def cell_paths_overlay(target_cell_list, mat):
    """returns matrix populated with cell paths"""
    cell_paths = cell_paths_generator(target_cell_list)

    for cell in cell_paths:
        row = cell[0]
        col = cell[1]
        mat[row][col] = 4

    return mat


def find_nearest_cell(matrix, points_list):
    """given a points list, find the nearest points in the matrix based on the points list"""
    # needs to cycle through the matrix len(points_list) times
    error_margin = 0.0001
    plist = len(points_list)
    closest_points_list = []
    current_distance = 10000  # init to large number to overwrite
    smallest_point = None  # start out as uninitialized
    num_rows, num_cols = matrix.shape
    for k in range(plist):
        print(k)
        list_point = points_list[k]
        print(list_point)
        for i in range(num_rows):
            for j in range(num_cols):
                mat_point = matrix[i][j]
                print(mat_point)
                distance = math.sqrt((mat_point[0] - list_point[0]) ** 2 + (mat_point[1] - list_point[1]) ** 2)
                if distance <= current_distance:
                    current_distance = distance
                    smallest_point = mat_point
                if i == (num_rows - 1) and j == (num_cols - 1):
                    closest_points_list.append(smallest_point)
                # comparing point from list from matrix
                # closest_point = matrix[0][0]
    current_distance = 10000  # reset to large value

    return closest_points_list


def get_visuals(target_cell_list, n):
    """returns matrix plot of size NxN with target cells and cell paths based on passed target cell list"""
    mat = matrix_generator(n)  # create a template matrix to be used for
    visualizer(target_cells_populater(target_cell_list, mat), n)  # mat plot of target cells
    visualizer(cell_paths_overlay(cell_paths_generator(target_cell_list), mat), n)  # mat plot of all target cell paths
    return 0


def create_lat_lon_matrix_scatter(lat_start, lat_end, lat_step, lon_start, lon_end, lon_step, marker_size=1000):
    latitudes = np.arange(lat_start, lat_end, lat_step)
    longitudes = np.arange(lon_start, lon_end, lon_step)
    lat_lon_matrix = np.zeros((len(latitudes), len(longitudes)), dtype=[('lat', float), ('lon', float)])
    for i in range(len(latitudes)):
        for j in range(len(longitudes)):
            lat_lon_matrix[i, j] = (latitudes[i], longitudes[j])

    plt.scatter(lat_lon_matrix['lon'], lat_lon_matrix['lat'], marker='s', color='gray', s=marker_size)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.title('lat/lon scatter plot')
    plt.show()
    return lat_lon_matrix


def plot_pcolormesh_matrix(lat_lon_matrix):
    latitudes = lat_lon_matrix['lat']
    longitudes = lat_lon_matrix['lon']

    # create meshgrid of lats and longs
    lon_mesh, lat_mesh = np.meshgrid(longitudes, latitudes)

    # plot grid with pcolormesh
    plt.pcolormesh(lon_mesh, lat_mesh, np.zeros_like(lon_mesh), edgecolors='black', linewidth=1)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.title('lat/lon pcolormesh grid plot')
    plt.show()

    return np.zeros_like(lon_mesh)



############################################################################ FOR DEMO : Proof of concept
print('Navigation proof of concept')
# # MAT SIZE : NxN matrix
N_SIZE = 30

# test array of targets cells
test_cells_arr = np.array([(2, 0), (25, 5), (25, 10), (7, 23), (19, 29)], dtype=[('x', int), ('y', int)])

# get figures
get_visuals(test_cells_arr, N_SIZE)
############################################################################

# MAIN STEPS #
# create the matrix of cells
# compare the pathdfinder list points to matrix points to find the closest match
# note the closest match and mark as placed node and do this for all points
# run bresenham to connect the dots and get navigation route and return list of all points
# VALIDATE : by calculating the distance and see if reasonable due to assumed linearity by bresenham


test_coords = [[-96.337128, 30.622604],
               [-96.3371069, 30.6225795],
               [-96.3372495, 30.6224529],
               [-96.3373759, 30.6223303],
               [-96.3375029, 30.6222239],
               [-96.3376825, 30.6220708],
               [-96.3378415, 30.6219379],
               [-96.3379903, 30.6218472],
               [-96.3381665, 30.6216913],
               [-96.3380595, 30.6213603],
               [-96.3378464, 30.6211812],
               [-96.3379835, 30.6210563],
               [-96.3380535, 30.6208965],
               [-96.3378261, 30.6205978],
               [-96.337678, 30.620827]]

# print(test_coords)
# print(test_coords[0])
# print(test_coords[0][0])
# print(test_coords[0][1])

lat_step = 0.005
lat_start = 30.605
lat_end = 30.630 + lat_step

lon_step = 0.0025
lon_start = -96.3450
lon_end = -96.3250 + lon_step

# mat = create_lat_lon_matrix(lat_start, lat_end, 0.001, lon_start, lon_end, 0.001)
# print(mat)
# create_lat_lon_matrix_scatter(lat_start, lat_end, lat_step, lon_start, lon_end, lon_step)
# plot_pcolormesh_matrix(mat)
# nearest_cells = find_nearest_cell(mat, test_coords)
# print("printing nearest cells: ", nearest_cells)
# print("num of nearest cells: ", len(nearest_cells))



















###### INITIAL PARTIAL TESTING STARTS HERE #######
# # making a matrix
# MAT_WIDTH = 30
# MAT_HEIGHT = 30
# initialized_zero_matrix = np.zeros((MAT_WIDTH, MAT_HEIGHT), dtype=int)
# # Node Coordinates (Nodes will be non zero values from 1 to n)
# start_node_x = 2
# start_node_y = 0
# end_node_x = MAT_WIDTH - 1 - 10
# end_node_y = MAT_HEIGHT - 1
#
# # will for loop for node placement, for now start and end are 1 and 2, intermediary nodes are 3, path cells are 4
# initialized_zero_matrix[start_node_x][start_node_y] = 1
# initialized_zero_matrix[end_node_x][end_node_y] = 2
#
# # bresenham line test
# path_cells_arr = bresenham_line(start_node_x, start_node_y, end_node_x, end_node_y)
# print(path_cells_arr)
#
# # nodes
# # active_node_list = [(start_node_x, start_node_y), (end_node_x, end_node_y)] # convert to numpy list
# # MAKE NODE LIST OF NUMPY TYPE IN ORDER TO USE INHERENT PYTHON SYNTAX
# active_node_list = np.array([(start_node_x, start_node_y), (end_node_x, end_node_y)], dtype=[('x', int), ('y', int)])
# print(active_node_list)
#
# # populating matrix with line path cells while avoiding start and end nodes
# for cells in path_cells_arr:
#     if cells not in active_node_list:
#         initialized_zero_matrix[cells[0]][cells[1]] = 4
#
# # start_end_cells = np.array([target_cell_list[0], target_cell_list[-1]], dtype=[('x', int), ('y', int)]) # USE FOR FUNC
#
# ## OBSTACLE CREATION
# # for i in range(5):
# #     initialized_zero_matrix[9 + i][16] = 4
#
# # printing map
# # print(initialized_zero_matrix)
# visualizer(initialized_zero_matrix, MAT_WIDTH)
