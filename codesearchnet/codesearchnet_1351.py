def clean_outcpd(self):
    """Hack to act like clean_outcpd on zeta1.TopLevelNode.
    Take the max element in each to column, set it to 1, and set all the
    other elements to 0.
    Only called by inferRowMaxProd() and only needed if an updateRow()
    has been called since the last clean_outcpd().
    """
    m = self.hist_.toDense()
    for j in xrange(m.shape[1]): # For each column.
      cmax = m[:,j].max()
      if cmax:
        m[:,j] = numpy.array(m[:,j] == cmax, dtype=dtype)
    self.hack_ = SparseMatrix(0, self.hist_.nCols())
    for i in xrange(m.shape[0]):
      self.hack_.addRow(m[i,:])