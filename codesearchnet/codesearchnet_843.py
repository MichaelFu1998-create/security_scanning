def _finalize(self):
    """Run final activities after a model has run. These include recording and
    logging the final score"""

    self._logger.info(
      "Finished: modelID=%r; %r records processed. Performing final activities",
      self._modelID, self._currentRecordIndex + 1)

    # =========================================================================
    # Dump the experiment metrics at the end of the task
    # =========================================================================
    self._updateModelDBResults()

    # =========================================================================
    # Check if the current model is the best. Create a milestone if necessary
    # If the model has been killed, it is not a candidate for "best model",
    # and its output cache should be destroyed
    # =========================================================================
    if not self._isKilled:
      self.__updateJobResults()
    else:
      self.__deleteOutputCache(self._modelID)

    # =========================================================================
    # Close output stream, if necessary
    # =========================================================================
    if self._predictionLogger:
      self._predictionLogger.close()

    # =========================================================================
    # Close input stream, if necessary
    # =========================================================================
    if self._inputSource: 
      self._inputSource.close()