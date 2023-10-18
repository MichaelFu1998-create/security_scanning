def _initializeBucketMap(self, maxBuckets, offset):
    """
    Initialize the bucket map assuming the given number of maxBuckets.
    """
    # The first bucket index will be _maxBuckets / 2 and bucket indices will be
    # allowed to grow lower or higher as long as they don't become negative.
    # _maxBuckets is required because the current SDR Classifier assumes bucket
    # indices must be non-negative. This normally does not need to be changed
    # but if altered, should be set to an even number.
    self._maxBuckets = maxBuckets
    self.minIndex = self._maxBuckets / 2
    self.maxIndex = self._maxBuckets / 2

    # The scalar offset used to map scalar values to bucket indices. The middle
    # bucket will correspond to numbers in the range
    # [offset-resolution/2, offset+resolution/2).
    # The bucket index for a number x will be:
    #     maxBuckets/2 + int( round( (x-offset)/resolution ) )
    self._offset = offset

    # This dictionary maps a bucket index into its bit representation
    # We initialize the class with a single bucket with index 0
    self.bucketMap = {}

    def _permutation(n):
      r = numpy.arange(n, dtype=numpy.uint32)
      self.random.shuffle(r)
      return r

    self.bucketMap[self.minIndex] = _permutation(self.n)[0:self.w]

    # How often we need to retry when generating valid encodings
    self.numTries = 0