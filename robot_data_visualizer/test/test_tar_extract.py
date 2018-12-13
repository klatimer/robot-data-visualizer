import unittest
import os
import sys
sys.path.append('.')
sys.path.append('..')
sys.path.append('../..')
from robot_data_visualizer.download_tar import download_tar
from robot_data_visualizer.tar_extract import tar_extract

class TestTarExtract(unittest.TestCase):

    def setUp(self):
        self.data_dir_name = 'data'
        self.base_name = 'http://robots.engin.umich.edu/nclt'
        self.date = '2013-01-10'
        self.root_path = os.path.abspath('.')
        self.data_dir_root = os.path.join(self.root_path, self.data_dir_name)
        self.curr_data_dir = os.path.join(self.data_dir_root, self.date)

    def test_tar_extract_sensor_data(self):
        filename = download_tar(self.base_name, self.date, 'sensor_data')
        tar_extract(filename)
        self.assertTrue(not (os.listdir(self.curr_data_dir) is 0)) # directory should not be empty

    def tearDown(self):
        os.chdir(self.root_path)

if __name__ == '__main__':
    unittest.main()