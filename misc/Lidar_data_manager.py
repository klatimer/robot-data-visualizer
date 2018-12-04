# Test an import of the DataManager class

import sys
sys.path.append('..')

import numpy as np
from tools.data_manager import DataManager

        # Initialize with desired date from the UMich dataset
dm = DataManager('2013-01-10')
        # Download and extract sensor data
dm.setup_data_files('sensor_data')
        # Download and extract data for the hokuyo lidar scanner
dm.setup_data_files('hokuyo')
        # load gps
dm.load_gps()
        # load first 100 scans of lidar
data = dm.data_dict
lidar = data['lidar']
# lidar0 = lidar[0]
x, y, time = lidar[0]
print(y)
num_samples = 100 # the number of points skipped between subsamples
count = 1
for i in range(0, num_samples - 1):
    lidar_i = lidar[i]
    x, y, time = lidar_i
    # print(x)
    x_index = np.nonzero(x)
    x_index_str = str(x_index)
    # print(x_index)
    y_index = np.nonzero(y)
    # print(y_index)
    y_index_str = str(y_index)
    # print(y_index)
    is_equal = x_index_str == y_index_str
    more_than_100 = len(x) > 100
    x = x[np.nonzero(x)]
    if is_equal == True & more_than_100 == True:
        count = count + 1
        # print(len(x))
        # print('min:', np.min(x))
        # print('max:', np.max(x))
        # print('mean:',np.mean(x))
        # print(i)
        # print("x_index length:", len(x_index))
        # print("y_index length:", len(y_index))
        # if len(x_index) == len(y_index):
        # print(i)
    # print(is_equal)
    # x_i = x[x_index]
    print('min:', np.min(x))
    print(count, "of", num_samples)
'''
    for k in range(0,1081):

#downsample_x= (x[::sample_rate])
    downsample_x = x_i
    length_downsample= len(downsample_x)
    print(length_downsample)
    #length_of_x = a.insert(i, length_downsample)
#print(a)
print(index)

'''

