import Pathfinder
from Pathfinder import initialize_map_and_plot
import Navigation
from Navigation import create_lat_lon_matrix, create_lat_lon_matrix_scatter, plot_pcolormesh_matrix

# FOR PATHFINDING
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

# case 3
tlat, tlon = 30.61071, -96.33934
tpoint = (tlon, tlat)
tlat2, tlon2 = 30.62083, -96.33980
tpoint2 = (tlon2, tlat2)



start_point = tpoint
target_point = tpoint2

# FOR NAVIGATION
lat_step = 0.005
lat_start = 30.605
lat_end = 30.630 + lat_step

lon_step = 0.0025
lon_start = -96.3450
lon_end = -96.3250 + lon_step


if __name__ == '__main__':
    # in loop to simulate infinite while loop with sensor input
    # user input to simulate boolean input from obstacle detection
    print('Begin main file block')
    flag_var = input('input here, q to quit: ')
    while flag_var != 'q':
        print('loop run')
        # path
        ax_general = initialize_map_and_plot(start_point, target_point)
        # nav
        mat = create_lat_lon_matrix(lat_start, lat_end, lat_step, lon_start, lon_end, lon_step)
        print(mat)
        create_lat_lon_matrix_scatter(lat_start, lat_end, lat_step, lon_start, lon_end, lon_step)
        plot_pcolormesh_matrix(mat)
        flag_var = input('input here, q to quit: ')
        if flag_var == 'q':
            print('program quit')
