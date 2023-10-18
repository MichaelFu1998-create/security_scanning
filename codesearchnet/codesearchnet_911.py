def encodeIntoArray(self, input, output):
    """ See method description in base.py """

    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
      output[0:] = 0
    else:
      if not isinstance(input, datetime.datetime):
        raise ValueError("Input is type %s, expected datetime. Value: %s" % (
            type(input), str(input)))

      # Get the scalar values for each sub-field
      scalars = self.getScalars(input)
      # Encoder each sub-field
      for i in xrange(len(self.encoders)):
        (name, encoder, offset) = self.encoders[i]
        encoder.encodeIntoArray(scalars[i], output[offset:])