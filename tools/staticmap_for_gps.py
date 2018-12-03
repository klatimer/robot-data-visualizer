from staticmap import StaticMap, Line
import os
import sys

sys.path.append('..')
import tools

def generate_coordinate():
    dm = tools.data_manager.DataManager('2013-01-10')
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

def divide_coordinates(coordinates):
    interval = len(coordinates) // 50 + 1
    divided_coordinates = []
    for i in range(0, len(coordinates), interval):
        divided_coordinates.append(coordinates[i: i + interval])
    return divided_coordinates

def map_for_gps_gif():

    m = StaticMap(1000, 1000, 80)

    (coordinates, data_dir) = generate_coordinate()
    # Put image in the corresponding data directory
    os.chdir(data_dir)

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


def map_for_gps():

    m = StaticMap(1000, 1000, 80)

    (coordinates, data_dir) = generate_coordinate()
    # Put image in the corresponding data directory
    os.chdir(data_dir)

    line = Line(coordinates, 'red', 4)
    m.add_line(line)

    image = m.render()
    image.save('umich_empty.png')

    points = m.extract_line_points()
    #print(points)

    return points

if __name__ == '__main__':
    map_for_gps()
