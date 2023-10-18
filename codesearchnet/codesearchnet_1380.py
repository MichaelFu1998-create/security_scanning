def closenessScores(self, expValues, actValues, fractional=True):
    """
    Compute closeness scores between the expected scalar value(s) and actual
    scalar value(s). The expected scalar values are typically those obtained
    from the :meth:`.getScalars` method. The actual scalar values are typically
    those returned from :meth:`.topDownCompute`.

    This method returns one closeness score for each value in expValues (or
    actValues which must be the same length). The closeness score ranges from
    0 to 1.0, 1.0 being a perfect match and 0 being the worst possible match.

    If this encoder is a simple, single field encoder, then it will expect
    just 1 item in each of the ``expValues`` and ``actValues`` arrays.
    Multi-encoders will expect 1 item per sub-encoder.

    Each encoder type can define it's own metric for closeness. For example,
    a category encoder may return either 1 or 0, if the scalar matches exactly
    or not. A scalar encoder might return a percentage match, etc.

    :param expValues: Array of expected scalar values, typically obtained from
                     :meth:`.getScalars`
    :param actValues: Array of actual values, typically obtained from
                     :meth:`.topDownCompute`

    :return: Array of closeness scores, one per item in expValues (or
             actValues).
    """
    # Fallback closenss is a percentage match
    if self.encoders is None:
      err = abs(expValues[0] - actValues[0])
      if fractional:
        denom = max(expValues[0], actValues[0])
        if denom == 0:
          denom = 1.0
        closeness = 1.0 - float(err)/denom
        if closeness < 0:
          closeness = 0
      else:
        closeness = err

      return numpy.array([closeness])

    # Concatenate the results from closeness scores on each child encoder
    scalarIdx = 0
    retVals = numpy.array([])
    for (name, encoder, offset) in self.encoders:
      values = encoder.closenessScores(expValues[scalarIdx:], actValues[scalarIdx:],
                                       fractional=fractional)
      scalarIdx += len(values)
      retVals = numpy.hstack((retVals, values))

    return retVals