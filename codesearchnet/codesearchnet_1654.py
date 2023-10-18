def getBucketValues(self):
    """ See the function description in base.py """

    # Need to re-create?
    if self._bucketValues is None:
      topDownMappingM = self._getTopDownMapping()
      numBuckets = topDownMappingM.nRows()
      self._bucketValues = []
      for bucketIdx in range(numBuckets):
        self._bucketValues.append(self.getBucketInfo([bucketIdx])[0].value)

    return self._bucketValues