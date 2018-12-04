"""
This filter is for filter the NaNs from csv file and return a new csv without NaN.
"""

def filter_nan(file_name):

    with open(file_name, 'r')as r:
        lines = r.readlines()
    with open(file_name, 'w')as w:
        for l in lines:
            if 'nan' not in l:
                w.write(l)

# Put gps.csv to the same directory then run this main.
if __name__ == '__main__':
    filter_nan('gps.csv')