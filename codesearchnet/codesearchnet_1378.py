def getBucketInfo(self, buckets):
    """
    Returns a list of :class:`.EncoderResult` namedtuples describing the inputs
    for each sub-field that correspond to the bucket indices passed in
    ``buckets``. To get the associated field names for each of the values, call
    :meth:`.getScalarNames`.

    :param buckets: The list of bucket indices, one for each sub-field encoder.
                   These bucket indices for example may have been retrieved
                   from the :meth:`.getBucketIndices` call.
    :return: A list of :class:`.EncoderResult`.
    """
    # Fall back topdown compute
    if self.encoders is None:
      raise RuntimeError("Must be implemented in sub-class")

    # Concatenate the results from bucketInfo on each child encoder
    retVals = []
    bucketOffset = 0
    for i in xrange(len(self.encoders)):
      (name, encoder, offset) = self.encoders[i]

      if encoder.encoders is not None:
        nextBucketOffset = bucketOffset + len(encoder.encoders)
      else:
        nextBucketOffset = bucketOffset + 1
      bucketIndices = buckets[bucketOffset:nextBucketOffset]
      values = encoder.getBucketInfo(bucketIndices)

      retVals.extend(values)

      bucketOffset = nextBucketOffset

    return retVals