def getBucketIndices(self, input):
    """ See method description in base.py """

    if type(input) is float and math.isnan(input):
      input = SENTINEL_VALUE_FOR_MISSING_DATA

    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
      return [None]

    minbin = self._getFirstOnBit(input)[0]

    # For periodic encoders, the bucket index is the index of the center bit
    if self.periodic:
      bucketIdx = minbin + self.halfwidth
      if bucketIdx < 0:
        bucketIdx += self.n

    # for non-periodic encoders, the bucket index is the index of the left bit
    else:
      bucketIdx = minbin

    return [bucketIdx]