import numpy as np

def threshold_lidar_pts(data_i):
    min_lidar_pts = 1
    thresh = 1
    ZERO = 0
    x, y, time = data_i

    threshold_indices = x < thresh
    x[threshold_indices] = ZERO
    threshold_indices = y < thresh
    y[threshold_indices] = ZERO

    x_index = np.nonzero(x)
    x_index_str = str(x_index)
    y_index = np.nonzero(y)
    y_index_str = str(y_index)
    is_equal = x_index_str == y_index_str
    if is_equal == True:
        x = x[np.nonzero(x)]
        y = y[np.nonzero(y)]
    else:
        index = []
        t = ZERO
        t_next = t + 1
        while t < len(x):
            if x[t] == ZERO and x[t] == y[t]:
                index = np.append(index, t)
            t = t_next
        x = np.delete(x, index)
        y = np.delete(y, index)
    return x, y, time