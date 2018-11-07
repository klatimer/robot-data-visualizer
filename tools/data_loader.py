"""
This class should handle downloading and caching data from the internet into a
'data' folder in the project root directory.
"""
import sys
import os

class DataLoader:

    def __init__(self):
        self.data_dir = 'data'
        self.data_url = 'url for the robot data'

    def download_data(self):
        """
        Make a directory fot the data, and download it.
        """
        p = os.path.dirname(os.path.abspath(__file__)) # path of this file
        os.chdir(p) # set system path to here
        os.chdir('..') # go up one level
        p = os.path.join(p, self.data_dir) # data directory
        if not os.path.exists(p):
            os.mkdir(p)
        # Now that we are in the data directory and have checked that it
        # exists, we can put the data here.


if __name__ == '__main__':
    # do something
    # dl = DataLoader(...)
    # dl.download_data()
