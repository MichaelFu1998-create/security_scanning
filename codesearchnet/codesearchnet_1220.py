def resetVelocity(self, rng):
    """See comments in base class."""
    maxVelocity = (self.max - self.min) / 5.0
    self._velocity = maxVelocity #min(abs(self._velocity), maxVelocity)
    self._velocity *= rng.choice([1, -1])