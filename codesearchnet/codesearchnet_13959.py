def hex_to_rgb(hex):
    """ Returns RGB values for a hex color string.
    """
    hex = hex.lstrip("#")
    if len(hex) < 6:
        hex += hex[-1] * (6 - len(hex))
    if len(hex) == 6:
        r, g, b = hex[0:2], hex[2:4], hex[4:]
        r, g, b = [int(n, 16) / 255.0 for n in (r, g, b)]
        a = 1.0
    elif len(hex) == 8:
        r, g, b, a = hex[0:2], hex[2:4], hex[4:6], hex[6:]
        r, g, b, a = [int(n, 16) / 255.0 for n in (r, g, b, a)]
    return r, g, b, a