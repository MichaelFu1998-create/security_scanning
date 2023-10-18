def rotate(x, y, x0, y0, angle):
    """ Returns the coordinates of (x,y) rotated around origin (x0,y0).
    """
    x, y = x - x0, y - y0
    a, b = cos(radians(angle)), sin(radians(angle))
    return (x * a - y * b + x0,
            y * a + x * b + y0)