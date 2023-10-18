def _getTotalLineCount(self):
    """ Returns:  count of ALL lines in dataset, including header lines
    """
    # Flush the file before we open it again to count lines
    if self._mode == self._FILE_WRITE_MODE:
      self._file.flush()
    return sum(1 for line in open(self._filename, self._FILE_READ_MODE))