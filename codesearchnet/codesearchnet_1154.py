def getDataRowCount(self):
    """
    Iterates through stream to calculate total records after aggregation.
    This will alter the bookmark state.
    """
    inputRowCountAfterAggregation = 0
    while True:
      record = self.getNextRecord()
      if record is None:
        return inputRowCountAfterAggregation
      inputRowCountAfterAggregation += 1

      if inputRowCountAfterAggregation > 10000:
        raise RuntimeError('No end of datastream found.')