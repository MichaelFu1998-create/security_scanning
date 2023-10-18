def getBucketValues(self):
    """
    See the function description in base.py
    """

    # Need to re-create?
    if self._bucketValues is None:
      scaledValues = self.encoder.getBucketValues()
      self._bucketValues = []
      for scaledValue in scaledValues:
        value = math.pow(10, scaledValue)
        self._bucketValues.append(value)

    return self._bucketValues