def getState(self):
    """See comments in base class."""
    return dict(_position = self.getPosition(),
                position = self.getPosition(),
                velocity = None,
                bestPosition = self.choices[self._bestPositionIdx],
                bestResult = self._bestResult)