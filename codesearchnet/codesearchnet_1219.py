def pushAwayFrom(self, otherPositions, rng):
    """See comments in base class."""
    # If min and max are the same, nothing to do
    if self.max == self.min:
      return

    # How many potential other positions to evaluate?
    numPositions = len(otherPositions) * 4
    if numPositions == 0:
      return

    # Assign a weight to each potential position based on how close it is
    # to other particles.
    stepSize = float(self.max-self.min) / numPositions
    positions = numpy.arange(self.min, self.max + stepSize, stepSize)

    # Get rid of duplicates.
    numPositions = len(positions)
    weights = numpy.zeros(numPositions)

    # Assign a weight to each potential position, based on a gaussian falloff
    # from each existing variable. The weight of a variable to each potential
    # position is given as:
    #    e ^ -(dist^2/stepSize^2)
    maxDistanceSq = -1 * (stepSize ** 2)
    for pos in otherPositions:
      distances = pos - positions
      varWeights = numpy.exp(numpy.power(distances, 2) / maxDistanceSq)
      weights += varWeights


    # Put this particle at the position with smallest weight.
    positionIdx = weights.argmin()
    self._position = positions[positionIdx]

    # Set its best position to this.
    self._bestPosition = self.getPosition()

    # Give it a random direction.
    self._velocity *= rng.choice([1, -1])