def getRecord(self, n=None):
    """Returns the nth record"""

    if n is None:
      assert len(self.fields)>0
      n = self.fields[0].numRecords-1

    assert (all(field.numRecords>n for field in self.fields))

    record = [field.values[n] for field in self.fields]

    return record