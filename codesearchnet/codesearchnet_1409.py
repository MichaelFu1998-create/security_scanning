def _finalizeSVD(self, numSVDDims=None):
    """
    Called by finalizeLearning(). This will project all the patterns onto the
    SVD eigenvectors.
    :param numSVDDims: (int) number of egeinvectors used for projection.
    :return:
    """
    if numSVDDims is not None:
      self.numSVDDims = numSVDDims


    if self.numSVDDims=="adaptive":
      if self.fractionOfMax is not None:
          self.numSVDDims = self.getAdaptiveSVDDims(self._s, self.fractionOfMax)
      else:
          self.numSVDDims = self.getAdaptiveSVDDims(self._s)


    if self._vt.shape[0] < self.numSVDDims:
      print "******************************************************************"
      print ("Warning: The requested number of PCA dimensions is more than "
             "the number of pattern dimensions.")
      print "Setting numSVDDims = ", self._vt.shape[0]
      print "******************************************************************"
      self.numSVDDims = self._vt.shape[0]

    self._vt = self._vt[:self.numSVDDims]

    # Added when svd is not able to decompose vectors - uses raw spare vectors
    if len(self._vt) == 0:
      return

    self._Memory = numpy.zeros((self._numPatterns,self.numSVDDims))
    self._M = self._Memory
    self.useSparseMemory = False

    for i in range(self._numPatterns):
      self._Memory[i] = numpy.dot(self._vt, self._a[i])

    self._a = None