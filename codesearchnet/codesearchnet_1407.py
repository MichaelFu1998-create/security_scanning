def computeSVD(self, numSVDSamples=0, finalize=True):
    """
    Compute the singular value decomposition (SVD). The SVD is a factorization
    of a real or complex matrix. It factors the matrix `a` as
    `u * np.diag(s) * v`, where `u` and `v` are unitary and `s` is a 1-d array
    of `a`'s singular values.

    **Reason for computing the SVD:**
    
    There are cases where you want to feed a lot of vectors to the
    KNNClassifier. However, this can be slow. You can speed up training by (1)
    computing the SVD of the input patterns which will give you the
    eigenvectors, (2) only keeping a fraction of the eigenvectors, and (3)
    projecting the input patterns onto the remaining eigenvectors.

    Note that all input patterns are projected onto the eigenvectors in the same
    fashion. Keeping only the highest eigenvectors increases training
    performance since it reduces the dimensionality of the input.

    :param numSVDSamples: (int) the number of samples to use for the SVD
                          computation.

    :param finalize: (bool) whether to apply SVD to the input patterns.

    :returns: (array) The singular values for every matrix, sorted in
               descending order.
    """
    if numSVDSamples == 0:
      numSVDSamples = self._numPatterns

    if not self.useSparseMemory:
      self._a = self._Memory[:self._numPatterns]
    else:
      self._a = self._Memory.toDense()[:self._numPatterns]

    self._mean = numpy.mean(self._a, axis=0)
    self._a -= self._mean
    u,self._s,self._vt = numpy.linalg.svd(self._a[:numSVDSamples])

    if finalize:
      self._finalizeSVD()

    return self._s