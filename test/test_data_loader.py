import unittest
import numpy as np
import sys
import os
"""
var = os.getcwd()
print('current working directory: ' + var)
test_path = os.path.abspath('.')
print('path to test dir: ' + test_path)
os.chdir(test_path)
"""
sys.path.append('.')
sys.path.append('..')
import tools.data_manager as DM

class BasicTest(unittest.TestCase):
    def setUp(self):
        self.Datamanager = DM.DataManager('2013-01-10')
        self.Datamanager.load_gps()

    def test_length(self):
        self.assertEqual(len(self.Datamanager.data_dict['gps']['lat']), 7186)
        self.assertEqual(len(self.Datamanager.data_dict['gps']['lng']), 7186)
        self.assertEqual(len(self.Datamanager.data_dict['gps']['alt']), 7186)

    def test_specific_value(self):
        self.assertEqual(self.Datamanager.data_dict['gps']['lat'][6552], 0.738168689900502 * 180 / np.pi)
        self.assertEqual(self.Datamanager.data_dict['gps']['lng'][6552], -1.4610748478234 * 180 / np.pi)
        self.assertEqual(self.Datamanager.data_dict['gps']['alt'][6552], 284.2)

if __name__ == '__main__':
    unittest.main()

