import os
import sys
# sys.path.append('..')

from staticmap import Line
from tools.static_map_base_layer import StaticMapBaseLayer

import matplotlib.pyplot as plt


def generate_coordinates(data_dict):
    gps_data = data_dict['gps']
    gps_lat = gps_data['lat']
    gps_lng = gps_data['lng']

    coordinates = []

    # for i in range(0, len(gps_lat), 50):
    for i in range(0, len(gps_lat)):
        coordinates.append([gps_lng[i], gps_lat[i]])

    return coordinates

def divide_coordinates(coordinates):
    interval = len(coordinates) // 50 + 1
    divided_coordinates = []
    for i in range(0, len(coordinates), interval):
        divided_coordinates.append(coordinates[i: i + interval])
    return divided_coordinates

def map_for_gps_gif():
    dm = DataManager('2013-01-10')
    # Download and extract sensor data
    dm.setup_data_files('sensor_data')
    # load gps
    dm.load_gps()

    m = StaticMapBaseLayer(1000, 1000, 80)

    coordinates = generate_coordinates(dm.data_dict)
    # Put image in the corresponding data directory
    os.chdir(dm.data_dir)

    line = Line(coordinates, 'red', 4)
    m.add_line(line)

    divided_coordinates = divide_coordinates(coordinates)
    length = len(divided_coordinates)
    for i in range(length):
        temp_line = Line(divided_coordinates[i], 'red', 4)
        m.add_line(temp_line)
        print('Total : ' + str(length)  + '  So far :' + str(i))
        if i != 0:
            prev_line = Line([divided_coordinates[i - 1][-1], divided_coordinates[i][0]], 'red', 4)
            m.add_line(prev_line)
        image = m.render()
        image.save('umich' + str(i) + '.png')


def map_for_gps(data_dict, data_dir):
    m = StaticMapBaseLayer(1000, 1000, 80)

    coordinates = generate_coordinates(data_dict)
    # Put image in the corresponding data directory
    os.chdir(data_dir)

    line = Line(coordinates, 'red', 4)
    m.add_line(line)

    image = m.render_without_features()
    image.save('map.png')

    points = m.extract_line_points()
    x_coords = [item[0] for item in points]
    y_coords = [item[1] for item in points]

    return x_coords, y_coords

if __name__ == '__main__':
    from tools.data_manager import DataManager
    dm = DataManager('2013-01-10')
    # Download and extract sensor data
    dm.setup_data_files('sensor_data')
    # load gps
    dm.load_gps()
    map_for_gps(dm.data_dict, dm.data_dir)
