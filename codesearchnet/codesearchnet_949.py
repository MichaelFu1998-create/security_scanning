def setParameter(self, parameterName, index, parameterValue):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.setParameter`.
    """
    if parameterName in self._temporalArgNames:
      setattr(self._tfdr, parameterName, parameterValue)

    elif parameterName == "logPathOutput":
      self.logPathOutput = parameterValue
      # Close any existing log file
      if self._fpLogTPOutput is not None:
        self._fpLogTPOutput.close()
        self._fpLogTPOutput = None

      # Open a new log file if requested
      if parameterValue:
        self._fpLogTPOutput = open(self.logPathOutput, 'w')

    elif hasattr(self, parameterName):
      setattr(self, parameterName, parameterValue)

    else:
      raise Exception('Unknown parameter: ' + parameterName)