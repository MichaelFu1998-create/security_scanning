def getBucketValues(self):
    """ See the function description in base.py """

    if self._bucketValues is None:
      numBuckets = len(self.encoder.getBucketValues())
      self._bucketValues = []
      for bucketIndex in range(numBuckets):
        self._bucketValues.append(self.getBucketInfo([bucketIndex])[0].value)

    return self._bucketValues