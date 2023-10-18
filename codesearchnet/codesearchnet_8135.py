def color_scale(color, level):
    """
    Scale RGB tuple by level, 0 - 256
    """
    return tuple([int(i * level) >> 8 for i in list(color)])