def getScalars(self, input):
    """ See method description in base.py """
    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
      return numpy.array([None])
    else:
      return numpy.array([self.categoryToIndex.get(input, 0)])