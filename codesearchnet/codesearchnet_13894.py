def lerp(a, b, t):
    """ Returns the linear interpolation between a and b for time t between 0.0-1.0.
        For example: lerp(100, 200, 0.5) => 150.
    """
    if t < 0.0:
        return a
    if t > 1.0:
        return b
    return a + (b - a) * t