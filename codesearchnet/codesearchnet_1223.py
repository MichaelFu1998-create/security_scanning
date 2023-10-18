def setState(self, state):
    """See comments in base class."""
    self._positionIdx = self.choices.index(state['_position'])
    self._bestPositionIdx = self.choices.index(state['bestPosition'])
    self._bestResult = state['bestResult']