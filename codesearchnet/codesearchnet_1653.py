def _getTopDownMapping(self):
    """ Return the interal _topDownMappingM matrix used for handling the
    bucketInfo() and topDownCompute() methods. This is a matrix, one row per
    category (bucket) where each row contains the encoded output for that
    category.
    """

    # Do we need to build up our reverse mapping table?
    if self._topDownMappingM is None:

      # The input scalar value corresponding to each possible output encoding
      if self.periodic:
        self._topDownValues = numpy.arange(self.minval + self.resolution / 2.0,
                                           self.maxval,
                                           self.resolution)
      else:
        #Number of values is (max-min)/resolutions
        self._topDownValues = numpy.arange(self.minval,
                                           self.maxval + self.resolution / 2.0,
                                           self.resolution)

      # Each row represents an encoded output pattern
      numCategories = len(self._topDownValues)
      self._topDownMappingM = SM32(numCategories, self.n)

      outputSpace = numpy.zeros(self.n, dtype=GetNTAReal())
      for i in xrange(numCategories):
        value = self._topDownValues[i]
        value = max(value, self.minval)
        value = min(value, self.maxval)
        self.encodeIntoArray(value, outputSpace, learn=False)
        self._topDownMappingM.setRowFromDense(i, outputSpace)

    return self._topDownMappingM