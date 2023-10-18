def grow(self, rows, cols):
    """
    Grows the histogram to have rows rows and cols columns.
    Must not have been initialized before, or already have the same
    number of columns.
    If rows is smaller than the current number of rows,
    does not shrink.
    Also updates the sizes of the row and column sums.

    :param rows: Integer number of rows.
    :param cols: Integer number of columns.
    """
    if not self.hist_:
      self.hist_ = SparseMatrix(rows, cols)
      self.rowSums_ = numpy.zeros(rows, dtype=dtype)
      self.colSums_ = numpy.zeros(cols, dtype=dtype)
      self.hack_ = None
    else:
      oldRows = self.hist_.nRows()
      oldCols = self.hist_.nCols()
      nextRows = max(oldRows, rows)
      nextCols = max(oldCols, cols)
      if (oldRows < nextRows) or (oldCols < nextCols):
        self.hist_.resize(nextRows, nextCols)
        if oldRows < nextRows:
          oldSums = self.rowSums_
          self.rowSums_ = numpy.zeros(nextRows, dtype=dtype)
          self.rowSums_[0:len(oldSums)] = oldSums
          self.hack_ = None
        if oldCols < nextCols:
          oldSums = self.colSums_
          self.colSums_ = numpy.zeros(nextCols, dtype=dtype)
          self.colSums_[0:len(oldSums)] = oldSums
          self.hack_ = None