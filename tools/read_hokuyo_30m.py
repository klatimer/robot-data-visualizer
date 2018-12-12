"""
code referenced from: http://robots.engin.umich.edu/nclt/python/read_hokuyo_30m.py
"""

import struct
import numpy as np


def convert(x_s):
    """
    This function converts the raw hokuyo data into meters.

    :param x_s: scaled data
    :return: float64 -- distance in meters
    """

    scaling = 0.005 # 5 mm
    offset = -100.0

    x_converted = x_s * scaling + offset

    return x_converted
def read_hokuyo(filename, max_samples=1000000):
    """
    This function reads the hokuyo data from a binary file.

    :param filename: Binary file to read.
    :type filename: str.
    :param max_samples: Maximum number of samples that will be read.
    :type num_samples: int.
    :return: list -- lidar data in cartesian coordinates
    """

    # List of tuples (x, y, timestamp) to return
    # x and y are lists of values
    data_x_y_time = []

    # hokuyo_30m always has 1081 hits
    num_hits = 1081

    # angles for each range observation
    rad0 = -135 * (np.pi/180.0)
    radstep = 0.25 * (np.pi/180.0)
    angles = np.linspace(rad0, rad0 + (num_hits-1)*radstep, num_hits)

    # Open file for binary read
    f_bin = open(filename, "rb")

    try:
        j = 0
        while j < max_samples:
            # Read timestamp
            expected_length = 8
            buf = f_bin.read(expected_length)
            if len(buf) is expected_length:
                utime = struct.unpack('<Q', buf)[0]
                radius = np.zeros(num_hits)
                for i in range(num_hits):
                    s_struct = struct.unpack('<H', f_bin.read(2))[0]
                    radius[i] = convert(s_struct)
            else:
                break

            x_coord = radius * np.cos(angles)
            y_coord = radius * np.sin(angles)

            # Append tuple of positions and timestamp
            data_x_y_time.append((x_coord, y_coord, utime))
            j = j + 1
    finally:
        f_bin.close()

    return data_x_y_time
