def newPosition(self, globalBestPosition, rng):
    """See comments in base class."""
    # First, update the velocity. The new velocity is given as:
    # v = (inertia * v)  + (cogRate * r1 * (localBest-pos))
    #                    + (socRate * r2 * (globalBest-pos))
    #
    # where r1 and r2 are random numbers between 0 and 1.0
    lb=float(Configuration.get("nupic.hypersearch.randomLowerBound"))
    ub=float(Configuration.get("nupic.hypersearch.randomUpperBound"))

    self._velocity = (self._velocity * self._inertia + rng.uniform(lb, ub) *
                      self._cogRate * (self._bestPosition - self.getPosition()))
    if globalBestPosition is not None:
      self._velocity += rng.uniform(lb, ub) * self._socRate * (
          globalBestPosition - self.getPosition())

    # update position based on velocity
    self._position += self._velocity

    # Clip it
    self._position = max(self.min, self._position)
    self._position = min(self.max, self._position)

    # Return it
    return self.getPosition()