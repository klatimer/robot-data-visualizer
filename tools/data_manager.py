''' This file contains a class DataManager used to as a manager to control the data
    used in the future.'''

import os
import pickle
from tools.data_loader import DataLoader
from tools.read_hokuyo_30m import read_hokuyo
from tools.tar_extract import tar_extract
from tools.download_tar import download_tar


class DataManager:
    '''This class handles downloading, extracting and storing data to be used by the main application.
    '''

    def __init__(self, date):
        '''
        Initialize all things needed to manager data.
        :param date: The data of data user want choose.
        '''
        # self.owd = os.getcwd()
        tmp = os.getcwd()
        self.owd = os.path.abspath('.')
        self.data_dir_name = 'data'
        self.base_name = 'http://robots.engin.umich.edu/nclt'
        self.date = date
        self.data_dir = os.path.join(self.owd, os.path.join(self.data_dir_name, self.date))
        self.data_dict = {}

    def setup_data_files(self, data_type):
        '''
        Used to setup different kinds of data.
        :param data_type: Different kinds of data
        :return:
        '''
        filename = download_tar(self.base_name, self.date, data_type)
        tar_extract(filename)

    def load_gps(self):
        '''
        Load GPS data. Then load gps data into dictionary.
        '''
        # Loads a list of ordered (x,y) tuples into the 'gps' key of the data dictionary
        os.chdir(self.owd)
        gps_file_path = os.path.join(self.data_dir_name, os.path.join(self.date, 'gps.csv'))
        data_loader = DataLoader(gps_file_path)
        self.data_dict['gps'] = data_loader.get_gps_dictionary()
        self.data_dict['gps_range'] = data_loader.get_gps_range()

    def load_lidar(self, num_samples, pickled = None, delete_pickle = None):
        '''
        Load lidar data and choose the number of samples as user's choice.

        Parameters
        ----------
        delete_pickle
            If delete_pickle = 'delete', delete any existing pickle of lidar.
        num_samples
            The number of lidar samples to use.
        pickled
            If pickled = 'pickled', load from existing pickle of lidar if
            it exists and save a pickle of lidar data.
        '''
        os.chdir(self.owd)
        lidar_file_path = os.path.join(self.data_dir_name,
                                       os.path.join(self.date, 'hokuyo_30m.bin'))
        if delete_pickle == 'delete':
            if os.path.exists("lidar.pickle"):
                os.remove("lidar.pickle")
                print("there is no pickle to delete")
        if pickled == 'pickled':
            try:
                pickled_lidar = pickle.load(open("lidar.pickle", "rb"))
                self.data_dict['lidar'] = pickled_lidar
            except (OSError, IOError) as e:
                self.data_dict['lidar'] = read_hokuyo(lidar_file_path, num_samples)
                pickled_lidar = self.data_dict['lidar']
                pickle.dump(pickled_lidar, open("lidar.pickle", "wb"))
        else:
            self.data_dict['lidar'] = read_hokuyo(lidar_file_path, num_samples)
    def load_all(self):
        '''
        load all gps and lidar data.
        '''
        self.load_gps()
        self.load_lidar(100)    # Note this could take a while - loads a lot of samples

    def get_data(self, key=None):
        '''
        Get data after load.
        :return: Chosen data in the dictionary.
        '''
        if key is None:
            return self.data_dict
        return self.data_dict[key]
