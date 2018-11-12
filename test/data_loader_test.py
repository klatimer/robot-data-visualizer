import unittest
import numpy as np
import sys
sys.path.append('..')
import tools.data_loader as DL


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.data_loader_1 = DL.DataLoader('Dataset1')
        self.data_loader_2 = DL.DataLoader('Dataset2')
        self.data_loader_3 = DL.DataLoader('Dataset3')

    def test_length(self):
        self.assertEqual(len(self.data_loader_1.get_gps_dictionary()['lat']), 31793)
        self.assertEqual(len(self.data_loader_1.get_gps_dictionary()['lng']), 31793)
        self.assertEqual(len(self.data_loader_1.get_gps_dictionary()['alt']), 31793)

        self.assertEqual(len(self.data_loader_2.get_gps_dictionary()['lat']), 7186)
        self.assertEqual(len(self.data_loader_2.get_gps_dictionary()['lng']), 7186)
        self.assertEqual(len(self.data_loader_2.get_gps_dictionary()['alt']), 7186)

        self.assertEqual(len(self.data_loader_3.get_gps_dictionary()['lat']), 34963)
        self.assertEqual(len(self.data_loader_3.get_gps_dictionary()['lng']), 34963)
        self.assertEqual(len(self.data_loader_3.get_gps_dictionary()['alt']), 34963)

    def test_specific_value(self):
        self.assertEqual(self.data_loader_1.get_gps_dictionary()['lat'][31585], 0.737842485 * 180 / np.pi)
        self.assertEqual(self.data_loader_1.get_gps_dictionary()['lng'][31585], -1.460770125 * 180 / np.pi)
        self.assertEqual(self.data_loader_1.get_gps_dictionary()['alt'][124], 270.7)

        self.assertEqual(self.data_loader_2.get_gps_dictionary()['lat'][6552], 0.738168689900502 * 180 / np.pi)
        self.assertEqual(self.data_loader_2.get_gps_dictionary()['lng'][6552], -1.4610748478234 * 180 / np.pi)
        self.assertEqual(self.data_loader_2.get_gps_dictionary()['alt'][6552], 284.2)

        self.assertEqual(self.data_loader_3.get_gps_dictionary()['lat'][2958], 0.738168079035264 * 180 / np.pi)
        self.assertEqual(self.data_loader_3.get_gps_dictionary()['lng'][2958], -1.46110171426999 * 180 / np.pi)
        self.assertEqual(self.data_loader_3.get_gps_dictionary()['alt'][2958], 268.4)


if __name__ == '__main__':
    unittest.main()
