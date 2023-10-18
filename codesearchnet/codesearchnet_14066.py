def complementary(clr):
    """
    Returns a list of complementary colors.

    The complement is the color 180 degrees across
    the artistic RYB color wheel.
    The list contains darker and softer contrasting
    and complementing colors.
    """
    clr = color(clr)
    colors = colorlist(clr)

    # A contrasting color: much darker or lighter than the original.
    c = clr.copy()
    if clr.brightness > 0.4:
        c.brightness = 0.1 + c.brightness * 0.25
    else:
        c.brightness = 1.0 - c.brightness * 0.25
    colors.append(c)

    # A soft supporting color: lighter and less saturated.
    c = clr.copy()
    c.brightness = 0.3 + c.brightness
    c.saturation = 0.1 + c.saturation * 0.3
    colors.append(c)

    # A contrasting complement: very dark or very light.
    clr = clr.complement
    c = clr.copy()
    if clr.brightness > 0.3:
        c.brightness = 0.1 + clr.brightness * 0.25
    else:
        c.brightness = 1.0 - c.brightness * 0.25
    colors.append(c)

    # The complement and a light supporting variant.
    colors.append(clr)

    c = clr.copy()
    c.brightness = 0.3 + c.brightness
    c.saturation = 0.1 + c.saturation * 0.25
    colors.append(c)

    return colors