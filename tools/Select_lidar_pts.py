def choose_lidar_pts(data = read_hokuyo('../data/2013-01-10/hokuyo_30m.bin', num_samples = 100),i):
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
        #print(len(x))
        #print('min:', np.min(x))
        #print('max:', np.max(x))
        #print('mean:',np.mean(x))
        #print(i)
        #print("x_index length:", len(x_index))
        #print("y_index length:", len(y_index))
        #if len(x_index) == len(y_index):
            #print(i)
        #print(is_equal)
        #x_i = x[x_index]


