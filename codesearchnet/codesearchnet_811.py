def _initPermNonConnected(self):
    """
    Returns a randomly generated permanence value for a synapses that is to be
    initialized in a non-connected state.
    """
    p = self._synPermConnected * self._random.getReal64()

    # Ensure we don't have too much unnecessary precision. A full 64 bits of
    # precision causes numerical stability issues across platforms and across
    # implementations
    p = int(p*100000) / 100000.0
    return p