def appendRecords(self, records, progressCB=None):
    """
    Saves multiple records in the underlying storage.

    :param records: array of records as in
                    :meth:`~.FileRecordStream.appendRecord`
    :param progressCB: (function) callback to report progress
    """

    for record in records:
      self.appendRecord(record)
      if progressCB is not None:
        progressCB()