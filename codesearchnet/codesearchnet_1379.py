def topDownCompute(self, encoded):
    """
    Returns a list of :class:`.EncoderResult` namedtuples describing the
    top-down best guess inputs for each sub-field given the encoded output.
    These are the values which are most likely to generate the given encoded
    output. To get the associated field names for each of the values, call
    :meth:`.getScalarNames`.

    :param encoded: The encoded output. Typically received from the topDown
                    outputs from the spatial pooler just above us.

    :return: A list of :class:`.EncoderResult`
    """
    # Fallback topdown compute
    if self.encoders is None:
      raise RuntimeError("Must be implemented in sub-class")

    # Concatenate the results from topDownCompute on each child encoder
    retVals = []
    for i in xrange(len(self.encoders)):
      (name, encoder, offset) = self.encoders[i]

      if i < len(self.encoders)-1:
        nextOffset = self.encoders[i+1][2]
      else:
        nextOffset = self.width

      fieldOutput = encoded[offset:nextOffset]
      values = encoder.topDownCompute(fieldOutput)

      if _isSequence(values):
        retVals.extend(values)
      else:
        retVals.append(values)

    return retVals