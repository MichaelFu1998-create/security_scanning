def getBucketIndices(self, x):
    """ See method description in base.py """

    if ((isinstance(x, float) and math.isnan(x)) or
        x == SENTINEL_VALUE_FOR_MISSING_DATA):
      return [None]

    if self._offset is None:
      self._offset = x

    bucketIdx = (
        (self._maxBuckets/2) + int(round((x - self._offset) / self.resolution))
    )

    if bucketIdx < 0:
      bucketIdx = 0
    elif bucketIdx >= self._maxBuckets:
      bucketIdx = self._maxBuckets-1

    return [bucketIdx]