import os
import sys
sys.path.append('..')

from staticmap import Line

from tools.data_manager import DataManager
from tools.static_map_base_layer import StaticMapBaseLayer
from tools.staticmap_for_gps import generate_coordinates

import matplotlib.pyplot as plt


def plot_gps_on_map():
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

    image = m.render_without_features()
    image.save('umich_empty.png')

    points = m.extract_line_points()
    x_coords = [item[0] for item in points]
    y_coords = [item[1] for item in points]

    plt.imshow(image)
    plt.plot(x_coords, y_coords)
    plt.show(block=True)  # block program until window is closed

    return points

if __name__ == '__main__':
    plot_gps_on_map()