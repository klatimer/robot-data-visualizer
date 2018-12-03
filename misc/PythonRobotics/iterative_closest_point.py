"""

Iterative Closest Point (ICP) SLAM example

author: Atsushi Sakai (@Atsushi_twi)

"""

import math
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('..')

import traceback
from tools.data_manager import DataManager

#  ICP parameters
EPS = 0.0001
MAXITER = 100

show_animation = True


def ICP_matching(ppoints, cpoints):
    """
    Iterative Closest Point matching

    - input
    ppoints: 2D points in the previous frame
    cpoints: 2D points in the current frame

    - output
    R: Rotation matrix
    T: Translation vector

    """
    H = None  # homogeneraous transformation matrix

    dError = 1000.0
    preError = 1000.0
    count = 0

    while dError >= EPS:
        count += 1

        if show_animation:
            plt.cla()
            plt.plot(ppoints[0, :], ppoints[1, :], ".r")
            plt.plot(cpoints[0, :], cpoints[1, :], ".b")
            plt.plot(0.0, 0.0, "xr")
            plt.axis("equal")
            plt.pause(1.0)

        inds, error = nearest_neighbor_assosiation(ppoints, cpoints)
        Rt, Tt = SVD_motion_estimation(ppoints[:, inds], cpoints)

        # update current points
        cpoints = (Rt * cpoints) + Tt

        H = update_homogenerous_matrix(H, Rt, Tt)

        dError = abs(preError - error)
        preError = error
        print("Residual:", error)

        if dError <= EPS:
            print("Converge", error, dError, count)
            break
        elif MAXITER <= count:
            print("Not Converge...", error, dError, count)
            break

    R = np.matrix(H[0:2, 0:2])
    T = np.matrix(H[0:2, 2])

    return R, T


def update_homogenerous_matrix(Hin, R, T):

    H = np.matrix(np.zeros((3, 3)))

    H[0, 0] = R[0, 0]
    H[1, 0] = R[1, 0]
    H[0, 1] = R[0, 1]
    H[1, 1] = R[1, 1]
    H[2, 2] = 1.0

    H[0, 2] = T[0, 0]
    H[1, 2] = T[1, 0]

    if Hin is None:
        return H
    else:
        return Hin * H


def nearest_neighbor_assosiation(ppoints, cpoints):

    # calc the sum of residual errors
    dcpoints = ppoints - cpoints
    d = np.linalg.norm(dcpoints, axis=0)
    error = sum(d)

    # calc index with nearest neighbor assosiation
    inds = []
    for i in range(cpoints.shape[1]):
        minid = -1
        mind = float("inf")
        for ii in range(ppoints.shape[1]):
            d = np.linalg.norm(ppoints[:, ii] - cpoints[:, i])

            if mind >= d:
                mind = d
                minid = ii

        inds.append(minid)

    return inds, error


def SVD_motion_estimation(ppoints, cpoints):

    pm = np.matrix(np.mean(ppoints, axis=1))
    cm = np.matrix(np.mean(cpoints, axis=1))

    pshift = np.matrix(ppoints - pm)
    cshift = np.matrix(cpoints - cm)

    W = cshift * pshift.T
    u, s, vh = np.linalg.svd(W)

    R = (u * vh).T
    t = pm - R * cm

    return R, t

def convert(x_s):

    scaling = 0.005 # 5 mm
    offset = -100.0

    x = x_s * scaling + offset

    return x

def choose_lidar_pts(i, data):
    data_i = data[i]
    x,y,time = data_i
    #print(x)
    x_index = np.nonzero(x)
    x_index_str = str(x_index)
    #print(x_index)
    y_index = np.nonzero(y)
    #print(y_index)
    y_index_str = str(y_index)
    #print(y_index)
    is_equal = x_index_str == y_index_str
    more_than_100 = len(x) > 100
    x = x[np.nonzero(x)]
    if is_equal == True & more_than_100 == True:
        return x, y, time


def main():
    print(__file__ + " start!!")

    # simulation parameters
    '''TO DO: 
    X  Find a subsampling routine
    X  Define the number of points to subsample. (define nPoint)
    (Skipping for now) Define the field length (based on data)
    (looks good, still need to determine units) Ensure data is in cartesian coordinates and convert as needed
    set px equal to x coordinate subsample
    set py equal to y coordinate subsample
    develop motion equation from odometry data: define x (m), y (m) and yaw (deg)
    
              '''

    nPoint = 100


    fieldLength = 50.0
    #motion = [0.5, 2.0, math.radians(-10.0)]  # movement [x[m],y[m],yaw[deg]]

    nsim = 10  # number of simulation

    for i in range(nsim):

        # previous points
        px, py, time = choose_lidar_pts(i)
        ppoints = np.matrix(np.vstack((px, py)))

        # current points
        cx, cy, time = choose_lidar_pts(i+1)

        cpoints = np.matrix(np.vstack((cx, cy)))

        R, T = ICP_matching(ppoints, cpoints)


if __name__ == '__main__':
    dm = DataManager('2013-01-10')
    dm.load_lidar(100)
    lidar = dm.data_dict['lidar']
    lidar_0 = lidar[1]
    print(lidar_0)
