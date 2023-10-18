def rgb_to_yiq(rgb):
    """
    Convert an RGB color representation to a YIQ color representation.

    (r, g, b) :: r -> [0, 255]
                 g -> [0, 255]
                 b -> [0, 255]

    :param rgb: A tuple of three numeric values corresponding to the red, green, and blue value.
    :return: YIQ representation of the input RGB value.
    :rtype: tuple
    """
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    y = (0.299 * r) + (0.587 * g) + (0.114 * b)
    i = (0.596 * r) - (0.275 * g) - (0.321 * b)
    q = (0.212 * r) - (0.528 * g) + (0.311 * b)
    return round(y, 3), round(i, 3), round(q, 3)