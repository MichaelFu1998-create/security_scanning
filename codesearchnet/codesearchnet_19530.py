def plots(data, **kwargs):
    """
    simple wrapper plot with labels and skip x
    :param yonly_or_xy:
    :param kwargs:
    :return:
    """
    labels = kwargs.pop('labels', '')
    loc = kwargs.pop('loc', 1)

    # if len(yonly_or_xy) == 1:
    #     x = range(len(yonly_or_xy))
    #     y = yonly_or_xy
    # else:
    #     x = yonly_or_xy[0]
    #     y = yonly_or_xy[1:]

    lines = plt.plot(np.asarray(data).T, **kwargs)
    if labels:
        plt.legend(lines, labels, loc=loc)
    return lines