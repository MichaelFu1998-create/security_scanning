def getNextRecord(self, useCache=True):
    """ Returns next available data record from the file.

    :returns: a data row (a list or tuple) if available; None, if no more
              records in the table (End of Stream - EOS); empty sequence (list
              or tuple) when timing out while waiting for the next record.
    """
    assert self._file is not None
    assert self._mode == self._FILE_READ_MODE

    # Read the line
    try:
      line = self._reader.next()

    except StopIteration:
      if self.rewindAtEOF:
        if self._recordCount == 0:
          raise Exception("The source configured to reset at EOF but "
                          "'%s' appears to be empty" % self._filename)
        self.rewind()
        line = self._reader.next()

      else:
        return None

    # Keep score of how many records were read
    self._recordCount += 1

    # Split the line to text fields and convert each text field to a Python
    # object if value is missing (empty string) encode appropriately for
    # upstream consumers in the case of numeric types, this means replacing
    # missing data with a sentinel value for string type, we can leave the empty
    # string in place
    record = []
    for i, f in enumerate(line):
      #print "DEBUG: Evaluating field @ index %s: %r" % (i, f)
      #sys.stdout.flush()
      if f in self._missingValues:
        record.append(SENTINEL_VALUE_FOR_MISSING_DATA)
      else:
        # either there is valid data, or the field is string type,
        # in which case the adapter does the right thing by default
        record.append(self._adapters[i](f))

    return record