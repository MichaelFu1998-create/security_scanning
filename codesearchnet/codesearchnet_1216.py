def getPosition(self):
    """See comments in base class."""
    if self.stepSize is None:
      return self._position

    # Find nearest step
    numSteps = (self._position - self.min)  / self.stepSize
    numSteps = int(round(numSteps))
    position = self.min + (numSteps * self.stepSize)
    position = max(self.min, position)
    position = min(self.max, position)
    return position