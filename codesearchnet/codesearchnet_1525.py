def getFieldMax(self, fieldName):
    """
    If underlying implementation does not support min/max stats collection,
    or if a field type does not support min/max (non scalars), the return
    value will be None.

    :param fieldName: (string) name of field to get max
    :returns: current maximum value for the field ``fieldName``.
    """
    stats = self.getStats()
    if stats == None:
      return None
    maxValues = stats.get('max', None)
    if maxValues == None:
      return None
    index = self.getFieldNames().index(fieldName)
    return maxValues[index]