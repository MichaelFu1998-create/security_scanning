def setState(self, state):
    """See comments in base class."""
    self._position = state['_position']
    self._velocity = state['velocity']
    self._bestPosition = state['bestPosition']
    self._bestResult = state['bestResult']