def _getW(self):
    """
    Gets a value of `w` for use in generating a pattern.
    """
    w = self._w

    if type(w) is list:
      return w[self._random.getUInt32(len(w))]
    else:
      return w