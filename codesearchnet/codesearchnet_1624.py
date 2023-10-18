def _newRepresentationOK(self, newRep, newIndex):
    """
    Return True if this new candidate representation satisfies all our overlap
    rules. Since we know that neighboring representations differ by at most
    one bit, we compute running overlaps.
    """
    if newRep.size != self.w:
      return False
    if (newIndex < self.minIndex-1) or (newIndex > self.maxIndex+1):
      raise ValueError("newIndex must be within one of existing indices")

    # A binary representation of newRep. We will use this to test containment
    newRepBinary = numpy.array([False]*self.n)
    newRepBinary[newRep] = True

    # Midpoint
    midIdx = self._maxBuckets/2

    # Start by checking the overlap at minIndex
    runningOverlap = self._countOverlap(self.bucketMap[self.minIndex], newRep)
    if not self._overlapOK(self.minIndex, newIndex, overlap=runningOverlap):
      return False

    # Compute running overlaps all the way to the midpoint
    for i in range(self.minIndex+1, midIdx+1):
      # This is the bit that is going to change
      newBit = (i-1)%self.w

      # Update our running overlap
      if newRepBinary[self.bucketMap[i-1][newBit]]:
        runningOverlap -= 1
      if newRepBinary[self.bucketMap[i][newBit]]:
        runningOverlap += 1

      # Verify our rules
      if not self._overlapOK(i, newIndex, overlap=runningOverlap):
        return False

    # At this point, runningOverlap contains the overlap for midIdx
    # Compute running overlaps all the way to maxIndex
    for i in range(midIdx+1, self.maxIndex+1):
      # This is the bit that is going to change
      newBit = i%self.w

      # Update our running overlap
      if newRepBinary[self.bucketMap[i-1][newBit]]:
        runningOverlap -= 1
      if newRepBinary[self.bucketMap[i][newBit]]:
        runningOverlap += 1

      # Verify our rules
      if not self._overlapOK(i, newIndex, overlap=runningOverlap):
        return False

    return True