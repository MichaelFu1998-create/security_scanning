def __flushPredictionCache(self):
    """
    Writes the contents of this model's in-memory prediction cache to a permanent
    store via the prediction output stream instance
    """

    if not self.__predictionCache:
      return

    # Create an output store, if one doesn't exist already
    if self._predictionLogger is None:
      self._createPredictionLogger()

    startTime = time.time()
    self._predictionLogger.writeRecords(self.__predictionCache,
                                        progressCB=self.__writeRecordsCallback)
    self._logger.info("Flushed prediction cache; numrows=%s; elapsed=%s sec.",
                      len(self.__predictionCache), time.time() - startTime)
    self.__predictionCache.clear()