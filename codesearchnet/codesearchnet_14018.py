def angle(x1, y1, x2, y2):
    """ The angle in degrees between two vectors.
    """
    sign = 1.0
    usign = (x1*y2 - y1*x2)
    if usign < 0:
        sign = -1.0
    num = x1*x2 + y1*y2
    den = hypot(x1,y1) * hypot(x2,y2)
    ratio = min(max(num/den, -1.0), 1.0)
    return sign * degrees(acos(ratio))