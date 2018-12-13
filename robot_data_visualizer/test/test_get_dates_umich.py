import unittest
import sys
sys.path.append('.')
sys.path.append('..')
sys.path.append('../..')
from robot_data_visualizer.get_dates_umich import get_dates_umich

class TestGetDatesUmich(unittest.TestCase):

    def setUp(self):
        self.dates = get_dates_umich()

    def test_returns_list(self):
        self.assertTrue(type(self.dates) is list)

    def test_element_type(self):
        for date in self.dates:
            self.assertTrue(type(date) is str)

if __name__ == '__main__':
    unittest.main()