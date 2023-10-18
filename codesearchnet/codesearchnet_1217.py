def agitate(self):
    """See comments in base class."""
    # Increase velocity enough that it will be higher the next time
    # newPosition() is called. We know that newPosition multiplies by inertia,
    # so take that into account.
    self._velocity *= 1.5 / self._inertia

    # Clip velocity
    maxV = (self.max - self.min)/2
    if self._velocity > maxV:
      self._velocity = maxV
    elif self._velocity < -maxV:
      self._velocity = -maxV

    # if we at the max or min, reverse direction
    if self._position == self.max and self._velocity > 0:
      self._velocity *= -1
    if self._position == self.min and self._velocity < 0:
      self._velocity *= -1