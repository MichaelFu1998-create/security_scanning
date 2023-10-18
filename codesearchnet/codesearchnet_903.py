def getScalars(self, input):
    """ See method description in base.py """
    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
        return numpy.array([0])

    index = self.categoryToIndex.get(input, None)
    if index is None:
      if self._learningEnabled:
        self._addCategory(input)
        index = self.ncategories - 1
      else:
        # if not found, we encode category 0
        index = 0

    return numpy.array([index])