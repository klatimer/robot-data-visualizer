# This class handles downloading, extracting and storing data to be used
#   by the main application.

import os

from tools.download_tar import *
from tools.tar_extract import tar_extract
from tools.read_gps import read_gps
from tools.read_hokuyo_30m import read_hokuyo

class DataManager:

    def __init__(self):
        self.owd = owd # original working directory (project root)
        self.data_dir = 'data'
        self.base_name = 'http://robots.engin.umich.edu/nclt'
        self.date = '2013-01-10'
        self.data_dict = {}

    def setup_data_files(self, data_type):
        ensure_data_dir_exists()
        filename = download_tar(self.base_name, self.date, data_type)
        tar_extract(filename)

    def load_gps(self):
        # Loads a list of ordered (x,y) tuples into the 'gps' key of the data dictionary
        os.chdir(self.owd)
        gps_file_path = os.path.join(self.data_dir, os.path.join(self.date, 'gps.csv'))
        self.data_dict['gps'] = read_gps(gps_file_path)

    def load_lidar(self, num_samples):
        os.chdir(self.owd)
        lidar_file_path = os.path.join(self.data_dir, os.path.join(self.date, 'hokuyo_30m.bin'))
        self.data_dict['lidar'] = read_hokuyo(lidar_file_path, num_samples)

    def load_all(self):
        self.load_gps()
        self.load_lidar() # Note this could take a while - loads a lot of samples

    def get_data(self, key=None):
        if key is None:
            return self.data_dict
        else:
            return self.data_dict[key]


if __name__ == '__main__':
    dm = DataManager()
    # Download and extract sensor data
    dm.setup_data_files('sensor_data')
    # Download and extract data for the hokuyo lidar scanner
    dm.setup_data_files('hokuyo')
    # load gps
    dm.load_gps()
    # load first 100 scans of lidar
    dm.load_lidar(100)
    tmp = 'temp'






