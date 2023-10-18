def _newRepresentation(self, index, newIndex):
    """
    Return a new representation for newIndex that overlaps with the
    representation at index by exactly w-1 bits
    """
    newRepresentation = self.bucketMap[index].copy()

    # Choose the bit we will replace in this representation. We need to shift
    # this bit deterministically. If this is always chosen randomly then there
    # is a 1 in w chance of the same bit being replaced in neighboring
    # representations, which is fairly high
    ri = newIndex % self.w

    # Now we choose a bit such that the overlap rules are satisfied.
    newBit = self.random.getUInt32(self.n)
    newRepresentation[ri] = newBit
    while newBit in self.bucketMap[index] or \
          not self._newRepresentationOK(newRepresentation, newIndex):
      self.numTries += 1
      newBit = self.random.getUInt32(self.n)
      newRepresentation[ri] = newBit

    return newRepresentation