def getPattern(self, idx, sparseBinaryForm=False, cat=None):
    """Gets a training pattern either by index or category number.

    :param idx: Index of the training pattern

    :param sparseBinaryForm: If true, returns a list of the indices of the
        non-zero bits in the training pattern

    :param cat: If not None, get the first pattern belonging to category cat. If
        this is specified, idx must be None.

    :returns: The training pattern with specified index
    """
    if cat is not None:
      assert idx is None
      idx = self._categoryList.index(cat)

    if not self.useSparseMemory:
      pattern = self._Memory[idx]
      if sparseBinaryForm:
        pattern = pattern.nonzero()[0]

    else:
      (nz, values) = self._Memory.rowNonZeros(idx)
      if not sparseBinaryForm:
        pattern = numpy.zeros(self._Memory.nCols())
        numpy.put(pattern, nz, 1)
      else:
        pattern = nz

    return pattern