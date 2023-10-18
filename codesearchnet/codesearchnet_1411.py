def setCategoryOfVectors(self, vectorIndices, categoryIndices):
    """Change the category associated with this vector(s).

    Used by the Network Builder to move vectors between categories, to enable
    categories, and to invalidate vectors by setting the category to -1.

    :param vectorIndices: Single index or list of indices

    :param categoryIndices: Single index or list of indices. Can also be a
        single index when vectorIndices is a list, in which case the same
        category will be used for all vectors
    """
    if not hasattr(vectorIndices, "__iter__"):
      vectorIndices = [vectorIndices]
      categoryIndices = [categoryIndices]
    elif not hasattr(categoryIndices, "__iter__"):
      categoryIndices = [categoryIndices] * len(vectorIndices)

    for i in xrange(len(vectorIndices)):
      vectorIndex = vectorIndices[i]
      categoryIndex = categoryIndices[i]

      # Out-of-bounds is not an error, because the KNN may not have seen the
      # vector yet
      if vectorIndex < len(self._categoryList):
        self._categoryList[vectorIndex] = categoryIndex