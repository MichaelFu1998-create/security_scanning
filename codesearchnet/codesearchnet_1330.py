def _finishSphering(self):
    """
    Compute normalization constants for each feature dimension
    based on the collected training samples.  Then normalize our
    training samples using these constants (so that each input
    dimension has mean and variance of zero and one, respectively.)
    Then feed these "sphered" training samples into the underlying
    SVM model.
    """

    # If we are sphering our data, we need to compute the
    # per-dimension normalization constants
    # First normalize the means (to zero)
    self._normOffset = self._samples.mean(axis=0) * -1.0
    self._samples += self._normOffset
    # Now normalize the variances (to one).  However, we need to be
    # careful because the variance could conceivably be zero for one
    # or more dimensions.
    variance = self._samples.var(axis=0)
    variance[numpy.where(variance == 0.0)] = 1.0
    self._normScale  = 1.0 / numpy.sqrt(variance)
    self._samples *= self._normScale

    # Now feed each "sphered" sample into the SVM library
    for sampleIndex in range(len(self._labels)):
      self._knn.learn(self._samples[sampleIndex],
                      self._labels[sampleIndex],
                      self._partitions[sampleIndex])