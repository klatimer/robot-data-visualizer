# This class handles downloading, extracting and storing data to be used
#   by the main application.

import os
# import sys
# sys.path.append('..')
# __all__=['DataManager']
# from tools import *

from tools.read_hokuyo_30m import read_hokuyo
from tools.tar_extract import tar_extract
from tools.download_tar import download_tar
from tools.data_loader import DataLoader


class DataManager:

    def __init__(self):
        self.owd = os.getcwd()
        self.data_dir_name = 'data'
        self.base_name = 'http://robots.engin.umich.edu/nclt'
        self.date = '2013-01-10'
        self.data_dir = os.path.join(self.owd, os.path.join(self.data_dir_name, self.date))
        self.data_dict = {}

    def setup_data_files(self, data_type):
        filename = download_tar(self.base_name, self.date, data_type)
        tar_extract(filename)

    def load_gps(self):
        # Loads a list of ordered (x,y) tuples into the 'gps' key of the data dictionary
        os.chdir(self.owd)
        gps_file_path = os.path.join(self.data_dir_name, os.path.join(self.date, 'gps.csv'))
        data_loader = DataLoader(gps_file_path)
        self.data_dict['gps'] = data_loader.get_gps_dictionary()
        self.data_dict['gps_range'] = data_loader.get_gps_range()

    def load_lidar(self, num_samples):
        os.chdir(self.owd)
        lidar_file_path = os.path.join(self.data_dir_name, os.path.join(self.date, 'hokuyo_30m.bin'))
        self.data_dict['lidar'] = read_hokuyo(lidar_file_path, num_samples)

    def load_all(self):
        self.load_gps()
        self.load_lidar()    # Note this could take a while - loads a lot of samples

    def get_data(self, key=None):
        if key is None:
            return self.data_dict
        else:
            return self.data_dict[key]






