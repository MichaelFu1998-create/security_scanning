def getBucketIndices(self, input):
    """ See method description in base.py """

    # Get the bucket index from the underlying scalar encoder
    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
      return [None]
    else:
      return self.encoder.getBucketIndices(self.categoryToIndex.get(input, 0))