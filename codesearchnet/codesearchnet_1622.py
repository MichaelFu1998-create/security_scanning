def _createBucket(self, index):
    """
    Create the given bucket index. Recursively create as many in-between
    bucket indices as necessary.
    """
    if index < self.minIndex:
      if index == self.minIndex - 1:
        # Create a new representation that has exactly w-1 overlapping bits
        # as the min representation
        self.bucketMap[index] = self._newRepresentation(self.minIndex,
                                                        index)
        self.minIndex = index
      else:
        # Recursively create all the indices above and then this index
        self._createBucket(index+1)
        self._createBucket(index)
    else:
      if index == self.maxIndex + 1:
        # Create a new representation that has exactly w-1 overlapping bits
        # as the max representation
        self.bucketMap[index] = self._newRepresentation(self.maxIndex,
                                                        index)
        self.maxIndex = index
      else:
        # Recursively create all the indices below and then this index
        self._createBucket(index-1)
        self._createBucket(index)