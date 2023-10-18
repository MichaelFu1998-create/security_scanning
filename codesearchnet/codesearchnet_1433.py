def getDataRowCount(self):
    """
    :returns: (int) count of data rows in dataset (excluding header lines)
    """
    numLines = self._getTotalLineCount()

    if numLines == 0:
      # this may be the case in a file opened for write before the
      # header rows are written out
      assert self._mode == self._FILE_WRITE_MODE and self._recordCount == 0
      numDataRows = 0
    else:
      numDataRows = numLines - self._NUM_HEADER_ROWS

    assert numDataRows >= 0

    return numDataRows