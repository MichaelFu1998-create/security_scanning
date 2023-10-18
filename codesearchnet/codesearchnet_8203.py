def hsv2rgb_360(hsv):
    """Python default hsv to rgb conversion for when hue values in the
    range 0-359 are preferred.  Due to requiring float math, this method
    is slower than hsv2rgb_rainbow and hsv2rgb_spectrum."""

    h, s, v = hsv

    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return (int(r * 255.0), int(g * 255.0), int(b * 255.0))