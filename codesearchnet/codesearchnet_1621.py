def encodeIntoArray(self, x, output):
    """ See method description in base.py """

    if x is not None and not isinstance(x, numbers.Number):
      raise TypeError(
          "Expected a scalar input but got input of type %s" % type(x))

    # Get the bucket index to use
    bucketIdx = self.getBucketIndices(x)[0]

    # None is returned for missing value in which case we return all 0's.
    output[0:self.n] = 0
    if bucketIdx is not None:
      output[self.mapBucketIndexToNonZeroBits(bucketIdx)] = 1