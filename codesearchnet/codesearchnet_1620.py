def mapBucketIndexToNonZeroBits(self, index):
    """
    Given a bucket index, return the list of non-zero bits. If the bucket
    index does not exist, it is created. If the index falls outside our range
    we clip it.

    :param index The bucket index to get non-zero bits for.
    @returns numpy array of indices of non-zero bits for specified index.
    """
    if index < 0:
      index = 0

    if index >= self._maxBuckets:
      index = self._maxBuckets-1

    if not self.bucketMap.has_key(index):
      if self.verbosity >= 2:
        print "Adding additional buckets to handle index=", index
      self._createBucket(index)
    return self.bucketMap[index]