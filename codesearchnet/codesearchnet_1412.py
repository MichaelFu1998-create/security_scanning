def getNextRecord(self):
    """
    Get the next record to encode. Includes getting a record from the 
    `dataSource` and applying filters. If the filters request more data from the 
    `dataSource` continue to get data from the `dataSource` until all filters 
    are satisfied. This method is separate from :meth:`.RecordSensor.compute` so that we can 
    use a standalone :class:`.RecordSensor` to get filtered data.
    """

    allFiltersHaveEnoughData = False
    while not allFiltersHaveEnoughData:
      # Get the data from the dataSource
      data = self.dataSource.getNextRecordDict()

      if not data:
        raise StopIteration("Datasource has no more data")

      # temporary check
      if "_reset" not in data:
        data["_reset"] = 0
      if "_sequenceId" not in data:
        data["_sequenceId"] = 0
      if "_category" not in data:
        data["_category"] = [None]

      data, allFiltersHaveEnoughData = self.applyFilters(data)

    self.lastRecord = data

    return data