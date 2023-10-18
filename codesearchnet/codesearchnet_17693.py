def rgb_to_hsv(rgb):
    """
    Convert an RGB color representation to an HSV color representation.

    (r, g, b) :: r -> [0, 255]
                 g -> [0, 255]
                 b -> [0, 255]

    :param rgb: A tuple of three numeric values corresponding to the red, green, and blue value.
    :return: HSV representation of the input RGB value.
    :rtype: tuple
    """
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    _min = min(r, g, b)
    _max = max(r, g, b)
    v = _max
    delta = _max - _min

    if _max == 0:
        return 0, 0, v

    s = delta / _max

    if delta == 0:
        delta = 1

    if r == _max:
        h = 60 * (((g - b) / delta) % 6)

    elif g == _max:
        h = 60 * (((b - r) / delta) + 2)

    else:
        h = 60 * (((r - g) / delta) + 4)

    return round(h, 3), round(s, 3), round(v, 3)