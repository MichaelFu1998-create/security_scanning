def yiq_to_rgb(yiq):
    """
    Convert a YIQ color representation to an RGB color representation.

    (y, i, q) :: y -> [0, 1]
                 i -> [-0.5957, 0.5957]
                 q -> [-0.5226, 0.5226]

    :param yiq: A tuple of three numeric values corresponding to the luma and chrominance.
    :return: RGB representation of the input YIQ value.
    :rtype: tuple
    """
    y, i, q = yiq
    r = y + (0.956 * i) + (0.621 * q)
    g = y - (0.272 * i) - (0.647 * q)
    b = y - (1.108 * i) + (1.705 * q)

    r = 1 if r > 1 else max(0, r)
    g = 1 if g > 1 else max(0, g)
    b = 1 if b > 1 else max(0, b)

    return round(r * 255, 3), round(g * 255, 3), round(b * 255, 3)