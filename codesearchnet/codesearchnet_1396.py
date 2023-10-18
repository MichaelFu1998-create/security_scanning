def getOverlaps(self, inputPattern):
    """
    Return the degree of overlap between an input pattern and each category
    stored in the classifier. The overlap is computed by computing:

    .. code-block:: python

      logical_and(inputPattern != 0, trainingPattern != 0).sum()

    :param inputPattern: pattern to check overlap of

    :returns: (overlaps, categories) Two numpy arrays of the same length, where:
    
                * overlaps: an integer overlap amount for each category
                * categories: category index for each element of overlaps
    """
    assert self.useSparseMemory, "Not implemented yet for dense storage"

    overlaps = self._Memory.rightVecSumAtNZ(inputPattern)
    return (overlaps, self._categoryList)