def rgb_to_hex(rgb):
    """
    Convert an RGB color representation to a HEX color representation.

    (r, g, b) :: r -> [0, 255]
                 g -> [0, 255]
                 b -> [0, 255]

    :param rgb: A tuple of three numeric values corresponding to the red, green, and blue value.
    :return: HEX representation of the input RGB value.
    :rtype: str
    """
    r, g, b = rgb
    return "#{0}{1}{2}".format(hex(int(r))[2:].zfill(2), hex(int(g))[2:].zfill(2), hex(int(b))[2:].zfill(2))