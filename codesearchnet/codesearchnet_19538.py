def imbound(clspatch, *args, **kwargs):
    """
    :param clspatch:
    :param args:
    :param kwargs:
    :return:
    """
    # todo : add example

    c = kwargs.pop('color', kwargs.get('edgecolor', None))
    kwargs.update(facecolor='none', edgecolor=c)
    return impatch(clspatch, *args, **kwargs)