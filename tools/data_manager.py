# This class handles downloading, extracting and storing data to be used
#   by the main application.

import os

from tools.download_tar import *
from tools.tar_extract import tar_extract

class DataManager:

    def __init__(self):
        self.data_dir = 'data'
        self.base_name = 'http://robots.engin.umich.edu/nclt'
        self.date = '2013-01-10'

    def setup_data(self):
        ensure_data_dir_exists()
        filename = download_tar(self.base_name, self.date)
        tmp = os.getcwd()
        tar_extract(filename)


if __name__ == '__main__':
    dm = DataManager()
    dm.setup_data()





