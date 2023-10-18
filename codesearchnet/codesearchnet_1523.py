def getNextRecordDict(self):
    """Returns next available data record from the storage as a dict, with the
    keys being the field names. This also adds in some meta fields:

      - ``_category``: The value from the category field (if any)
      - ``_reset``: True if the reset field was True (if any)
      - ``_sequenceId``: the value from the sequenceId field (if any)

    """

    values = self.getNextRecord()
    if values is None:
      return None

    if not values:
      return dict()

    if self._modelRecordEncoder is None:
      self._modelRecordEncoder = ModelRecordEncoder(
        fields=self.getFields(),
        aggregationPeriod=self.getAggregationMonthsAndSeconds())

    return self._modelRecordEncoder.encode(values)