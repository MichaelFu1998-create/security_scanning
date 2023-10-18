def addValueToField(self, i, value=None):
    """Add 'value' to the field i.
    Parameters:
    --------------------------------------------------------------------
    value:       value to be added
    i:           value is added to field i
    """

    assert(len(self.fields)>i)
    if value is None:
      value = self.fields[i].dataClass.getNext()
      self.fields[i].addValue(value)
      return value

    else: self.fields[i].addValue(value)