def _generate(self):
    """
    Generates set of random patterns.
    """
    candidates = np.array(range(self._n), np.uint32)
    for i in xrange(self._num):
      self._random.shuffle(candidates)
      pattern = candidates[0:self._getW()]
      self._patterns[i] = set(pattern)