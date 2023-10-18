def reflect(x, y, x0, y0, d=1.0, a=180):
    """ Returns the reflection of a point through origin (x0,y0).
    """
    return coordinates(x0, y0, d * distance(x0, y0, x, y),
                       a + angle(x0, y0, x, y))