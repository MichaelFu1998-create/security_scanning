def encodeIntoArray(self, input, output,learn=None):
    """
    [overrides nupic.encoders.scalar.ScalarEncoder.encodeIntoArray]
    """

    self.recordNum +=1
    if learn is None:
      learn = self._learningEnabled
    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
        output[0:self.n] = 0
    elif not math.isnan(input):
      self._setMinAndMax(input, learn)

    super(AdaptiveScalarEncoder, self).encodeIntoArray(input, output)