def coordinateForPosition(self, longitude, latitude, altitude=None):
    """
    Returns coordinate for given GPS position.

    :param: longitude (float) Longitude of position
    :param: latitude (float) Latitude of position
    :param: altitude (float) Altitude of position
    :returns: (numpy.array) Coordinate that the given GPS position
                          maps to
    """
    coords = PROJ(longitude, latitude)

    if altitude is not None:
      coords = transform(PROJ, geocentric, coords[0], coords[1], altitude)

    coordinate = numpy.array(coords)
    coordinate = coordinate / self.scale
    return coordinate.astype(int)