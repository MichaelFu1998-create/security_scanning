def _removeRows(self, rowsToRemove):
    """
    A list of row indices to remove. There are two caveats. First, this is
    a potentially slow operation. Second, pattern indices will shift if
    patterns before them are removed.
    """
    # Form a numpy array of row indices to be removed
    removalArray = numpy.array(rowsToRemove)

    # Remove categories
    self._categoryList = numpy.delete(numpy.array(self._categoryList),
                                      removalArray).tolist()

    if self.fixedCapacity:
      self._categoryRecencyList = numpy.delete(
        numpy.array(self._categoryRecencyList), removalArray).tolist()

    # Remove the partition ID, if any for these rows and rebuild the id map.
    for row in reversed(rowsToRemove):  # Go backwards
      # Remove these patterns from partitionList
      self._partitionIdList.pop(row)
    self._rebuildPartitionIdMap(self._partitionIdList)


    # Remove actual patterns
    if self.useSparseMemory:
      # Delete backwards
      for rowIndex in rowsToRemove[::-1]:
        self._Memory.deleteRow(rowIndex)
    else:
      self._M = numpy.delete(self._M, removalArray, 0)

    numRemoved = len(rowsToRemove)

    # Sanity checks
    numRowsExpected = self._numPatterns - numRemoved
    if self.useSparseMemory:
      if self._Memory is not None:
        assert self._Memory.nRows() == numRowsExpected
    else:
      assert self._M.shape[0] == numRowsExpected
    assert len(self._categoryList) == numRowsExpected

    self._numPatterns -= numRemoved
    return numRemoved