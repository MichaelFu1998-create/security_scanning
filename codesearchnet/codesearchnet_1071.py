def generateRecord(self, record):
    """Generate a record. Each value is stored in its respective field.
    Parameters:
    --------------------------------------------------------------------
    record:       A 1-D array containing as many values as the number of fields
    fields:       An object of the class field that specifies the characteristics
                  of each value in the record
    Assertion:
    --------------------------------------------------------------------
    len(record)==len(fields):   A value for each field must be specified.
                                Replace missing values of any type by
                                SENTINEL_VALUE_FOR_MISSING_DATA

    This method supports external classes but not combination of classes.
    """
    assert(len(record)==len(self.fields))
    if record is not None:
      for x in range(len(self.fields)):
        self.fields[x].addValue(record[x])

    else:
      for field in self.fields:
        field.addValue(field.dataClass.getNext())