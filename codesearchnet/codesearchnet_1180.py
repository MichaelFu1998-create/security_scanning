def radiusForSpeed(self, speed):
    """
    Returns radius for given speed.

    Tries to get the encodings of consecutive readings to be
    adjacent with some overlap.

    :param: speed (float) Speed (in meters per second)
    :returns: (int) Radius for given speed
    """
    overlap = 1.5
    coordinatesPerTimestep = speed * self.timestep / self.scale
    radius = int(round(float(coordinatesPerTimestep) / 2 * overlap))
    minRadius = int(math.ceil((math.sqrt(self.w) - 1) / 2))
    return max(radius, minRadius)