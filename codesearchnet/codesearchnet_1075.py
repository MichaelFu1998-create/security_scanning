def encodeRecord(self, record, toBeAdded=True):
    """Encode a record as a sparse distributed representation
    Parameters:
    --------------------------------------------------------------------
    record:        Record to be encoded
    toBeAdded:     Whether the encodings corresponding to the record are added to
                   the corresponding fields
    """
    encoding=[self.fields[i].encodeValue(record[i], toBeAdded) for i in \
              xrange(len(self.fields))]

    return encoding