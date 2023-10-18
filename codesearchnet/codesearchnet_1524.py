def getFieldMin(self, fieldName):
    """
    If underlying implementation does not support min/max stats collection,
    or if a field type does not support min/max (non scalars), the return
    value will be None.

    :param fieldName: (string) name of field to get min
    :returns: current minimum value for the field ``fieldName``.
    """
    stats = self.getStats()
    if stats == None:
      return None
    minValues = stats.get('min', None)
    if minValues == None:
      return None
    index = self.getFieldNames().index(fieldName)
    return minValues[index]