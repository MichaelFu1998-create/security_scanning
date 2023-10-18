def compute(self, inputs, outputs):
    """
    Process one input sample.
    This method is called by the runtime engine.
    """
    record = self._constructClassificationRecord(inputs)

    #Classify this point after waiting the classification delay
    if record.ROWID >= self.getParameter('trainRecords'):
      self._classifyState(record)

    #Save new classification record and keep history as moving window
    self._recordsCache.append(record)
    while len(self._recordsCache) > self.cacheSize:
      self._recordsCache.pop(0)

    self.labelResults = record.anomalyLabel

    self._iteration += 1