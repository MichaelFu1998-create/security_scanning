def color_cmp(a, b):
    """Order colors by hue, saturation and value, in that order.

    Returns -1 if a < b, 0 if a == b and 1 if a < b.
    """
    if a == b:
        return 0

    a, b = rgb_to_hsv(a), rgb_to_hsv(b)
    return -1 if a < b else 1