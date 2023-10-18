def getBucketIndices(self, input, learn=None):
    """
    [overrides nupic.encoders.scalar.ScalarEncoder.getBucketIndices]
    """

    self.recordNum +=1
    if learn is None:
      learn = self._learningEnabled

    if type(input) is float and math.isnan(input):
      input = SENTINEL_VALUE_FOR_MISSING_DATA

    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
      return [None]
    else:
      self._setMinAndMax(input, learn)
      return super(AdaptiveScalarEncoder, self).getBucketIndices(input)