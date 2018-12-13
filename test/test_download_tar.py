import unittest
import os
import sys
sys.path.append('.')
sys.path.append('..')
from tools.download_tar import download_tar
from tools.download_tar import ensure_data_dir_exists

class TestDownloadTar(unittest.TestCase):

    def setUp(self):
        self.data_dir_name = 'data'
        self.base_name = 'http://robots.engin.umich.edu/nclt'
        self.date = '2013-01-10'
        self.root_path = os.path.abspath('.')
        self.data_dir_root = os.path.join(self.root_path, self.data_dir_name)
        self.curr_data_dir = os.path.join(self.data_dir_root, self.date)

    def test_ensure_data_dir_exists(self):
        ensure_data_dir_exists()
        self.assertTrue(os.path.exists(self.data_dir_root))

    def test_download_sensor_data(self):
        download_tar(self.base_name, self.date, 'sensor_data')
        tmp = os.path.exists(self.curr_data_dir)
        self.assertTrue(os.path.exists(self.curr_data_dir))

    def test_download_lidar_data(self):
        download_tar(self.base_name, self.date, 'hokuyo')
        file_name = self.date + '_hokuyo.tar.gz'
        tmp = os.path.join(self.data_dir_root, file_name)
        self.assertTrue(os.path.isfile(os.path.join(self.data_dir_root, file_name)))

    def tearDown(self):
        os.chdir(self.root_path)

if __name__ == '__main__':
    unittest.main()