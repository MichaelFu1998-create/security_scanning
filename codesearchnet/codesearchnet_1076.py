def encodeAllRecords(self, records=None, toBeAdded=True):
    """Encodes a list of records.
    Parameters:
    --------------------------------------------------------------------
    records:      One or more records. (i,j)th element of this 2D array
                  specifies the value at field j of record i.
                  If unspecified, records previously generated and stored are
                  used.
    toBeAdded:    Whether the encodings corresponding to the record are added to
                  the corresponding fields
    """
    if records is None:
      records = self.getAllRecords()
    if self.verbosity>0: print 'Encoding', len(records), 'records.'
    encodings = [self.encodeRecord(record, toBeAdded) for record in records]

    return encodings