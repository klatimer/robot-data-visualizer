# Test an import of the DataManager class

import sys
sys.path.append('..')

from tools.data_manager import DataManager


def main():
    try:
        dm = DataManager()
        # Download and extract sensor data
        dm.setup_data_files('sensor_data')
        # Download and extract data for the hokuyo lidar scanner
        dm.setup_data_files('hokuyo')
        # load gps
        dm.load_gps()
        # load first 100 scans of lidar
        dm.load_lidar(100)
        print('Successful load of data')
    except:
        print('Data manager failure')

if __name__ == '__main__':
    main()