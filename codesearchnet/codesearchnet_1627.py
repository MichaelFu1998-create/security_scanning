def _overlapOK(self, i, j, overlap=None):
    """
    Return True if the given overlap between bucket indices i and j are
    acceptable. If overlap is not specified, calculate it from the bucketMap
    """
    if overlap is None:
      overlap = self._countOverlapIndices(i, j)
    if abs(i-j) < self.w:
      if overlap == (self.w - abs(i-j)):
        return True
      else:
        return False
    else:
      if overlap <= self._maxOverlap:
        return True
      else:
        return False