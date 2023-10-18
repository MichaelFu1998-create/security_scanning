def _storeSample(self, inputVector, trueCatIndex, partition=0):
    """
    Store a training sample and associated category label
    """

    # If this is the first sample, then allocate a numpy array
    # of the appropriate size in which to store all samples.
    if self._samples is None:
      self._samples = numpy.zeros((0, len(inputVector)), dtype=RealNumpyDType)
      assert self._labels is None
      self._labels = []

    # Add the sample vector and category lable
    self._samples = numpy.concatenate((self._samples, numpy.atleast_2d(inputVector)), axis=0)
    self._labels += [trueCatIndex]

    # Add the partition ID
    if self._partitions is None:
      self._partitions = []
    if partition is None:
      partition = 0
    self._partitions += [partition]