def closestTrainingPattern(self, inputPattern, cat):
    """Returns the closest training pattern to inputPattern that belongs to
    category "cat".

    :param inputPattern: The pattern whose closest neighbor is sought

    :param cat: The required category of closest neighbor

    :returns: A dense version of the closest training pattern, or None if no
        such patterns exist
    """
    dist = self._getDistances(inputPattern)
    sorted = dist.argsort()

    for patIdx in sorted:
      patternCat = self._categoryList[patIdx]

      # If closest pattern belongs to desired category, return it
      if patternCat == cat:
        if self.useSparseMemory:
          closestPattern = self._Memory.getRow(int(patIdx))
        else:
          closestPattern = self._M[patIdx]

        return closestPattern

    # No patterns were found!
    return None