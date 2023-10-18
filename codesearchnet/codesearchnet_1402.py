def getPartitionId(self, i):
    """
    Gets the partition id given an index.

    :param i: index of partition
    :returns: the partition id associated with pattern i. Returns None if no id
        is associated with it.
    """
    if (i < 0) or (i >= self._numPatterns):
      raise RuntimeError("index out of bounds")
    partitionId = self._partitionIdList[i]
    if partitionId == numpy.inf:
      return None
    else:
      return partitionId