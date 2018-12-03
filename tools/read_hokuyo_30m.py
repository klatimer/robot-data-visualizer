# !/usr/bin/python
# Base on http://robots.engin.umich.edu/nclt/python/read_hokuyo_30m.py
# Example code to go through the hokuyo_30m.bin file, read timestamps and the hits
# in each packet, and plot them.
#
# To call:
#
#   python read_hokuyo_30m.py hokuyo_30m.bin
#

import sys
import struct
import numpy as np
import matplotlib.pyplot as plt

def convert(x_s):

    scaling = 0.005 # 5 mm
    offset = -100.0

    x = x_s * scaling + offset

    return x

def read_hokuyo(filename, max_samples=1000000):
    # List of tuples (x, y, timestamp) to return
    # x and y are lists of values
    data = []

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
            utime = struct.unpack('<Q', f_bin.read(8))[0]
            r = np.zeros(num_hits)
            for i in range(num_hits):
                s = struct.unpack('<H', f_bin.read(2))[0]
                r[i] = convert(s)

            x = r * np.cos(angles)
            y = r * np.sin(angles)

            # Append tuple of positions and timestamp
            data.append((x, y, utime))
            j = j + 1
    finally:
        f_bin.close()

    return data

if __name__ == '__main__':
    data = read_hokuyo('../data/2013-01-10/hokuyo_30m.bin', 100)