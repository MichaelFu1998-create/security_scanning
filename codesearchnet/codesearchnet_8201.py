def hsv2rgb_spectrum(hsv):
    """Generates RGB values from HSV values in line with a typical light
    spectrum."""
    h, s, v = hsv
    return hsv2rgb_raw(((h * 192) >> 8, s, v))