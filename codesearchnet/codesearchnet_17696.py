def hsv_to_rgb(hsv):
    """
    Convert an HSV color representation to an RGB color representation.

    (h, s, v) :: h -> [0, 360)
                 s -> [0, 1]
                 v -> [0, 1]

    :param hsv: A tuple of three numeric values corresponding to the hue, saturation, and value.
    :return: RGB representation of the input HSV value.
    :rtype: tuple
    """
    h, s, v = hsv
    c = v * s
    h /= 60
    x = c * (1 - abs((h % 2) - 1))
    m = v - c

    if h < 1:
        res = (c, x, 0)
    elif h < 2:
        res = (x, c, 0)
    elif h < 3:
        res = (0, c, x)
    elif h < 4:
        res = (0, x, c)
    elif h < 5:
        res = (x, 0, c)
    elif h < 6:
        res = (c, 0, x)
    else:
        raise ColorException("Unable to convert from HSV to RGB")

    r, g, b = res
    return round((r + m)*255, 3), round((g + m)*255, 3), round((b + m)*255, 3)