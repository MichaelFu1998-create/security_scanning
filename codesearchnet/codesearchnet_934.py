def setParameter(self, parameterName, index, parameterValue):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.setParameter`.

    Set the value of a Spec parameter. Most parameters are handled
    automatically by PyRegion's parameter set mechanism. The ones that need
    special treatment are explicitly handled here.
    """
    if parameterName in self._spatialArgNames:
      setattr(self._sfdr, parameterName, parameterValue)

    elif parameterName == "logPathInput":
      self.logPathInput = parameterValue
      # Close any existing log file
      if self._fpLogSPInput:
        self._fpLogSPInput.close()
        self._fpLogSPInput = None
      # Open a new log file
      if parameterValue:
        self._fpLogSPInput = open(self.logPathInput, 'w')

    elif parameterName == "logPathOutput":
      self.logPathOutput = parameterValue
      # Close any existing log file
      if self._fpLogSP:
        self._fpLogSP.close()
        self._fpLogSP = None
      # Open a new log file
      if parameterValue:
        self._fpLogSP = open(self.logPathOutput, 'w')

    elif parameterName == "logPathOutputDense":
      self.logPathOutputDense = parameterValue
      # Close any existing log file
      if self._fpLogSPDense:
        self._fpLogSPDense.close()
        self._fpLogSPDense = None
      # Open a new log file
      if parameterValue:
        self._fpLogSPDense = open(self.logPathOutputDense, 'w')

    elif hasattr(self, parameterName):
      setattr(self, parameterName, parameterValue)

    else:
      raise Exception('Unknown parameter: ' + parameterName)