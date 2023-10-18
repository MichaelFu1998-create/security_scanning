def pushAwayFrom(self, otherPositions, rng):
    """See comments in base class."""
    # Get the count of how many in each position
    positions = [self.choices.index(x) for x in otherPositions]

    positionCounts = [0] * len(self.choices)
    for pos in positions:
      positionCounts[pos] += 1

    self._positionIdx = numpy.array(positionCounts).argmin()
    self._bestPositionIdx = self._positionIdx