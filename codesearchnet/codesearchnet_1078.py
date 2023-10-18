def addValuesToField(self, i, numValues):
    """Add values to the field i."""

    assert(len(self.fields)>i)
    values = [self.addValueToField(i) for n in range(numValues)]
    return values