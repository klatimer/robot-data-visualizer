# This script downloads a tar file from the UMich robotics dataset
# Reference: http://blog.ppkt.eu/2014/06/python-urllib-and-tarfile/

import os
import urllib.request

os.chdir('..') # go up to project root directory
owd = os.getcwd() # original working directory
data_dir = None

# Make sure that there is a 'data' directory
def ensure_data_dir_exists():
    global owd, data_dir
    p = owd
    p = os.path.join(p, 'data')
    if not os.path.exists(p):
        os.mkdir(p)
    data_dir = p

# Download the tar file and put it in the data directory
def download_tar(base_name, date, data_type):
    ensure_data_dir_exists()
    global data_dir
    os.chdir(data_dir)
    if data_type is 'sensor_data': # miscellaneous sensors, incl. GPS
        tmp = '%s/sensor_data/' % base_name
        fname = '%s_sen.tar.gz' % date
    elif data_type is 'hokuyo': # hokuyo lidar scanner
        tmp = '%s/hokuyo_data/' % base_name
        fname = '%s_hokuyo.tar.gz' % date
    # TODO throw exception for invalid data_type
    url = tmp + fname
    path = os.path.join(data_dir, fname)
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    else:
        pass
    # os.chdir('gui') # FIXME
    return fname
