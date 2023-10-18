def _initPermConnected(self):
    """
    Returns a randomly generated permanence value for a synapses that is
    initialized in a connected state. The basic idea here is to initialize
    permanence values very close to synPermConnected so that a small number of
    learning steps could make it disconnected or connected.

    Note: experimentation was done a long time ago on the best way to initialize
    permanence values, but the history for this particular scheme has been lost.
    """
    p = self._synPermConnected + (
        self._synPermMax - self._synPermConnected)*self._random.getReal64()

    # Ensure we don't have too much unnecessary precision. A full 64 bits of
    # precision causes numerical stability issues across platforms and across
    # implementations
    p = int(p*100000) / 100000.0
    return p