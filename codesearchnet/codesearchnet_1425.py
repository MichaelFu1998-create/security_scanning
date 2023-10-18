def appendRecord(self, record):
    """
    Saves the record in the underlying csv file.

    :param record: a list of Python objects that will be string-ified
    """

    assert self._file is not None
    assert self._mode == self._FILE_WRITE_MODE
    assert isinstance(record, (list, tuple)), \
      "unexpected record type: " + repr(type(record))

    assert len(record) == self._fieldCount, \
      "len(record): %s, fieldCount: %s" % (len(record), self._fieldCount)

    # Write header if needed
    if self._recordCount == 0:
      # Write the header
      names, types, specials = zip(*self.getFields())
      for line in names, types, specials:
        self._writer.writerow(line)

    # Keep track of sequences, make sure time flows forward
    self._updateSequenceInfo(record)

    line = [self._adapters[i](f) for i, f in enumerate(record)]

    self._writer.writerow(line)
    self._recordCount += 1