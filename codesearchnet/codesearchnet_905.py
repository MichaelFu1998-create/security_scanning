def _getTopDownMapping(self):
    """ Return the interal _topDownMappingM matrix used for handling the
    bucketInfo() and topDownCompute() methods. This is a matrix, one row per
    category (bucket) where each row contains the encoded output for that
    category.
    """

    # -------------------------------------------------------------------------
    # Do we need to build up our reverse mapping table?
    if self._topDownMappingM is None:

      # Each row represents an encoded output pattern
      self._topDownMappingM = SM32(self.ncategories, self.n)

      outputSpace = numpy.zeros(self.n, dtype=GetNTAReal())
      for i in xrange(self.ncategories):
        self.encodeIntoArray(self.categories[i], outputSpace)
        self._topDownMappingM.setRowFromDense(i, outputSpace)

    return self._topDownMappingM