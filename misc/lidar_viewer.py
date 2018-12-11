"""lidar_viewer visualizes lidar data by ploting it in matplotlib window."""

import sys
sys.path.append('..')
import datetime
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import numpy as np
from tools.data_manager import DataManager


def hokuyo_plot(x_lidar, y_lidar, time):
    """
    Creates plot of xy lidar data with lidar
    range arc plotted in blue line.

    Keyword arguments:
    x_lidar -- x components of lidar scan
    y_lidar -- y components of lidar scan
    time    -- time stamp of lidar scan
    """

    # copied and modified from:
    # https://github.com/matplotlib/matplotlib/issues/8046/#issuecomment-278312361
    # Circle parameters
    # set arc diameters
    diameter = [2, 60]
    #arc center
    center = 0
    #time to wait between plots
    delay = 0.1
    #convert epoch time to datetime format
    time = str(time)
    time = int(time[:10])
    time = datetime.datetime.fromtimestamp(time).strftime('%c')

    # Figure setup
    fig, axes = plt.subplots()
    # delete unused argument 'fig'
    del fig
    #plot inner arc
    axes.add_patch(Arc((center, center), diameter[0], diameter[0],
                       theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))
    #plot outer arc
    axes.add_patch(Arc((center, center), diameter[1], diameter[1],
                       theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))
    # start and end points for lidar boundary lines
    line_start_end = [0.8, 21.21]
    # x & y coordinates for line 1
    line_start_x, line_end_x = line_start_end[0], line_start_end[1]
    line_start_y, line_end_y = -line_start_end[0], -line_start_end[1]
    # plot line 1
    plt.plot([line_start_x, line_end_x], [line_start_y, line_end_y], 'b')
    # x & y coordinates for line 2
    line_start_x, line_end_x = -line_start_end[0], -line_start_end[1]
    line_start_y, line_end_y = -line_start_end[0], -line_start_end[1]
    # plot line 2
    plt.plot([line_start_x, line_end_x], [line_start_y, line_end_y], 'b')
    # plot lidar points
    plt.plot(x_lidar, y_lidar, '.')
    # plot title of time in datetime format
    plt.title(time)
    # label x axis
    plt.xlabel('Distance (meters)')
    # set axis limits
    axes = plt.gca()
    xlimits, ylimits = [-32, 32], [-32, 32]
    axes.set_xlim(xlimits)
    axes.set_ylim(ylimits)
    # wait to close plot for 'delay' seconds
    plt.pause(delay)
    # close plot
    plt.close()


def threshold_lidar_pts(data_i):
    """
    Set points in lidar frame with values less than one
    to zero and remove all zeros from lidar frame.
    Keyword arguments:
    data_i -- lidar frame (x points, y points, timestamp)
    """
    # value below which to threshold data
    thresh = 1
    x_lidar, y_lidar, time = data_i
    # index x values below threshold
    threshold_indices = x_lidar < thresh
    # set x lidar points below threshold to 0
    x_lidar[threshold_indices] = 0
    # index y values below threshold
    threshold_indices = y_lidar < thresh
    # set x lidar points below threshold to 0
    y_lidar[threshold_indices] = 0
    # index lidar points with nonzero values
    x_index = np.nonzero(x_lidar)
    y_index = np.nonzero(y_lidar)
    # convert index list to string for comparison
    # and check equality
    x_index_str = str(x_index)
    y_index_str = str(y_index)
    is_equal = x_index_str == y_index_str
    # if indexes match, remove 0 points all at once
    if is_equal:
        x_lidar = x_lidar[np.nonzero(x_lidar)]
        y_lidar = y_lidar[np.nonzero(y_lidar)]
    #else, remove 0 points one by one
    else:
        index = []
        count = 0
        while count < len(x_lidar):
            if x_lidar[count] == 0 and x_lidar[count] == y_lidar[count]:
                index = np.append(index, count)
            count = count + 1
        x_lidar = np.delete(x_lidar, index)
        y_lidar = np.delete(y_lidar, index)
    # return filtered data
    return (x_lidar, y_lidar, time)


def lidar_viewer(date, num_samples, step_size=40, pickled=False, delete_pickle=False):
    """
    lidar_viewer visualizes lidar data by ploting it in matplotlib window.

    :param date: A 'Session' date from http://robots.engin.umich.edu/nclt/ (string)
    :param num_samples: The number of lidar frames to view (int)
    :param step_size: The amount of frames to skip between plots (data recorded at 40Hz)
    :param pickled: Set to True if you want to save a pickle imported lidar data.
    :param delete_pickle: Set to True if you want to delete any existing pickles of data.
    """
    # initialize datamanager
    data_manager = DataManager(date)
    print('DataManager initialized')
    # Download and extract sensor data
    data_manager.setup_data_files('sensor_data')
    print('sensor data downloaded')
    # Download and extract data for the hokuyo lidar scanner
    data_manager.setup_data_files('hokuyo')

    # load scans of lidar

    print('hokuyo data loading...')
    data_manager.load_lidar(num_samples, pickled, delete_pickle)
    lidar = data_manager.data_dict['lidar']
    print('plotting lidar')
    for i in range(0, int(num_samples/step_size)*step_size, step_size):
        lidar_i = lidar[i]
        x_lidar, y_lidar, time = threshold_lidar_pts(lidar_i)
        x_not_equal_time = str(x_lidar) != str(time)
        if x_not_equal_time:
            hokuyo_plot(x_lidar, y_lidar, time)


if __name__ == '__main__':
    date = '2012-12-01'
    num_samples = 4000
    step_size = 40
    print(range(0, num_samples, step_size))
    pickled = True
    delete_pickle = False
    lidar_viewer(date, num_samples, step_size, pickled, delete_pickle)