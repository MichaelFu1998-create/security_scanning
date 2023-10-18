def setParameter(self, name, index, value):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.setParameter`.
    """
    if name == "trainRecords":
      # Ensure that the trainRecords can only be set to minimum of the ROWID in
      # the saved states
      if not (isinstance(value, float) or isinstance(value, int)):
        raise HTMPredictionModelInvalidArgument("Invalid argument type \'%s\'. threshold "
          "must be a number." % (type(value)))

      if len(self._recordsCache) > 0 and value < self._recordsCache[0].ROWID:
        raise HTMPredictionModelInvalidArgument("Invalid value. autoDetectWaitRecord "
          "value must be valid record within output stream. Current minimum "
          " ROWID in output stream is %d." % (self._recordsCache[0].ROWID))

      self.trainRecords = value
      # Remove any labels before the first cached record (wont be used anymore)
      self._deleteRangeFromKNN(0, self._recordsCache[0].ROWID)
      # Reclassify all states
      self._classifyStates()
    elif name == "anomalyThreshold":
      if not (isinstance(value, float) or isinstance(value, int)):
        raise HTMPredictionModelInvalidArgument("Invalid argument type \'%s\'. threshold "
          "must be a number." % (type(value)))
      self.anomalyThreshold = value
      self._classifyStates()
    elif name == "classificationMaxDist":
      if not (isinstance(value, float) or isinstance(value, int)):
        raise HTMPredictionModelInvalidArgument("Invalid argument type \'%s\'. "
          "classificationMaxDist must be a number." % (type(value)))
      self._classificationMaxDist = value
      self._classifyStates()
    elif name == "activeColumnCount":
      self._activeColumnCount = value
    else:
      return PyRegion.setParameter(self, name, index, value)