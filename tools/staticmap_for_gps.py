from staticmap import StaticMap, Line
import os
import sys

sys.path.append('..')
import tools

def generate_coordinate():
    dm = tools.data_manager.DataManager()
    # Download and extract sensor data
    dm.setup_data_files('sensor_data')
    # load gps
    dm.load_gps()

    gps_data = dm.data_dict['gps']
    gps_lat = gps_data['lat']
    gps_lng = gps_data['lng']

    coordinates = []

    for i in range(0, len(gps_lat), 50):
        coordinates.append([gps_lng[i], gps_lat[i]])

    return (coordinates, dm.data_dir)

def map_for_gps():
    m = StaticMap(1000, 1000, 80)

    (coordinates, data_dir) = generate_coordinate()

    line = Line(coordinates, '#D2322D', 4)

    m.add_line(line)

    image = m.render()
    # Put image in the corresponding data directory
    os.chdir(data_dir)
    image.save('umich.png')


if __name__ == '__main__':
    map_for_gps()
