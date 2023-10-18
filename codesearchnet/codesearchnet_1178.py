def encodeIntoArray(self, inputData, output):
    """
    See `nupic.encoders.base.Encoder` for more information.

    :param: inputData (tuple) Contains speed (float), longitude (float),
                             latitude (float), altitude (float)
    :param: output (numpy.array) Stores encoded SDR in this numpy array
    """
    altitude = None
    if len(inputData) == 4:
      (speed, longitude, latitude, altitude) = inputData
    else:
      (speed, longitude, latitude) = inputData
    coordinate = self.coordinateForPosition(longitude, latitude, altitude)
    radius = self.radiusForSpeed(speed)
    super(GeospatialCoordinateEncoder, self).encodeIntoArray(
     (coordinate, radius), output)