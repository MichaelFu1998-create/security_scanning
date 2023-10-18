def imbox(xy, w, h, angle=0.0, **kwargs):
    """
    draw boundary box
    :param xy: start index xy (ji)
    :param w: width
    :param h: height
    :param angle:
    :param kwargs:
    :return:
    """
    from matplotlib.patches import Rectangle
    return imbound(Rectangle, xy, w, h, angle, **kwargs)