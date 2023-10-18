def analogous(clr, angle=10, contrast=0.25):
    """
    Returns colors that are next to each other on the wheel.

    These yield natural color schemes (like shades of water or sky).
    The angle determines how far the colors are apart,
    making it bigger will introduce more variation.
    The contrast determines the darkness/lightness of
    the analogue colors in respect to the given colors.
    """
    contrast = max(0, min(contrast, 1.0))

    clr = color(clr)
    colors = colorlist(clr)

    for i, j in [(1, 2.2), (2, 1), (-1, -0.5), (-2, 1)]:
        c = clr.rotate_ryb(angle * i)
        t = 0.44 - j * 0.1
        if clr.brightness - contrast * j < t:
            c.brightness = t
        else:
            c.brightness = clr.brightness - contrast * j
        c.saturation -= 0.05
        colors.append(c)

    return colors