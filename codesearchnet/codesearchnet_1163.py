def _generate(self):
    """
    Generates set of consecutive patterns.
    """
    n = self._n
    w = self._w

    assert type(w) is int, "List for w not supported"

    for i in xrange(n / w):
      pattern = set(xrange(i * w, (i+1) * w))
      self._patterns[i] = pattern