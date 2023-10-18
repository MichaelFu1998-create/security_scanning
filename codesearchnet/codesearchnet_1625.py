def _countOverlapIndices(self, i, j):
    """
    Return the overlap between bucket indices i and j
    """
    if self.bucketMap.has_key(i) and self.bucketMap.has_key(j):
      iRep = self.bucketMap[i]
      jRep = self.bucketMap[j]
      return self._countOverlap(iRep, jRep)
    else:
      raise ValueError("Either i or j don't exist")