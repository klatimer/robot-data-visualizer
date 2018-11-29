#Code copied from: http://robots.engin.umich.edu/nclt/python/read_gps.py and converted to Python3
# Example code to read and plot the gps data.
#GPS data header::::: time (microseconds since 1970) : Unknown : Number of satalites : Latitude (radians) : Longitude (radians) : Elevation (meters above sea level) : Unknown : Unknown
# To call:
#
#   python read_gps.py gps.csv
#

import numpy as np

def read_gps(filename):
    gps = np.loadtxt(filename, delimiter = ",")

    num_sats = gps[:, 2]
    lat = gps[:, 3]
    lng = gps[:, 4]
    alt = gps[:, 5]

    lat0 = lat[0]
    lng0 = lng[0]

    dLat = lat - lat0
    dLng = lng - lng0

    r = 6400000 # approx. radius of earth (m)
    x = r * np.cos(lat0) * np.sin(dLng)
    y = r * np.sin(dLat)

    # Return list of tuples
    gps_data = list(zip(x, y))
    return gps_data