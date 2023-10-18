def hex_to_rgb(_hex):
    """
    Convert a HEX color representation to an RGB color representation.

    hex :: hex -> [000000, FFFFFF]

    :param _hex: The 3- or 6-char hexadecimal string representing the color value.
    :return: RGB representation of the input HEX value.
    :rtype: tuple
    """
    _hex = _hex.strip('#')
    n = len(_hex) // 3
    if len(_hex) == 3:
        r = int(_hex[:n] * 2, 16)
        g = int(_hex[n:2 * n] * 2, 16)
        b = int(_hex[2 * n:3 * n] * 2, 16)
    else:
        r = int(_hex[:n], 16)
        g = int(_hex[n:2 * n], 16)
        b = int(_hex[2 * n:3 * n], 16)
    return r, g, b