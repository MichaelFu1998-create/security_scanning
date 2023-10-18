def coordinates(x0, y0, distance, angle):
    """ Returns the location of a point by rotating around origin (x0,y0).
    """
    return (x0 + cos(radians(angle)) * distance,
            y0 + sin(radians(angle)) * distance)