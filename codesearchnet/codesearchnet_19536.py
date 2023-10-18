def matshow(*args, **kwargs):
    """
    imshow without interpolation like as matshow
    :param args:
    :param kwargs:
    :return:
    """
    kwargs['interpolation'] = kwargs.pop('interpolation', 'none')
    return plt.imshow(*args, **kwargs)