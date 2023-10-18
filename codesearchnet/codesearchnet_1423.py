def rewind(self):
    """
    Put us back at the beginning of the file again.
    """

    # Superclass rewind
    super(FileRecordStream, self).rewind()

    self.close()
    self._file = open(self._filename, self._mode)
    self._reader = csv.reader(self._file, dialect="excel")

    # Skip header rows
    self._reader.next()
    self._reader.next()
    self._reader.next()

    # Reset record count, etc.
    self._recordCount = 0