def getAllRecords(self):
    """Returns all the records"""
    values=[]
    numRecords = self.fields[0].numRecords
    assert (all(field.numRecords==numRecords for field in self.fields))

    for x in range(numRecords):
      values.append(self.getRecord(x))

    return values