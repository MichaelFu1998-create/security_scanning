def getBucketInfo(self, buckets):
    """
    [overrides nupic.encoders.scalar.ScalarEncoder.getBucketInfo]
    """

    if self.minval is None or self.maxval is None:
      return [EncoderResult(value=0, scalar=0,
                           encoding=numpy.zeros(self.n))]

    return super(AdaptiveScalarEncoder, self).getBucketInfo(buckets)