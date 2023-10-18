def getState(self):
    """See comments in base class."""
    return dict(_position = self._position,
                position = self.getPosition(),
                velocity = self._velocity,
                bestPosition = self._bestPosition,
                bestResult = self._bestResult)