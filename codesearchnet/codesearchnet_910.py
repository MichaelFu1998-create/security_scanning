def getBucketIndices(self, input):
    """ See method description in base.py """

    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
      # Encoder each sub-field
      return [None] * len(self.encoders)

    else:
      assert isinstance(input, datetime.datetime)

      # Get the scalar values for each sub-field
      scalars = self.getScalars(input)

      # Encoder each sub-field
      result = []
      for i in xrange(len(self.encoders)):
        (name, encoder, offset) = self.encoders[i]
        result.extend(encoder.getBucketIndices(scalars[i]))
      return result