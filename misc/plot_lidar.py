def hokuyo_plot(x, y):


    # copied and modified from:
    # https://github.com/matplotlib/matplotlib/issues/8046/#issuecomment-278312361
    # Ellipse parameters
    D_0 = 2
    D_1 = 60
    x0, y0 = 0, 0
    # Figure setup
    fig, ax = plt.subplots()

    # Inner Arc
    ax.add_patch(Arc((x0, y0), D_0, D_0,
                     theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))
    # Outer Arc
    ax.add_patch(Arc((x0, y0), D_1, D_1,
                     theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))

    line_x = [0.8, 21.21, -0.8, -21.21]
    line_y = [-0.8, -21.21, -0.8, -21.21]
    p1_1, p1_2 = 0, 1
    x1, x2 = line_x[p1_1], line_x[p1_2]
    y1, y2 = line_y[p1_1], line_y[p1_2]
    p2_1, p2_2 = 2, 3
    x3, x4 = line_x[p2_1], line_x[p2_2]
    y3, y4 = line_y[p2_1], line_y[p2_2]

    plt.plot([x1, x2], [y1, y2], 'b')
    plt.plot([x3, x4], [y3, y4], 'b')

    plt.plot(x, y, '.')
    plt.title(time)
    plt.pause(delay)
    fig.clf()