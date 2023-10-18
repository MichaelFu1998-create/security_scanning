def getParameter(self, parameterName, index=-1):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.getParameter`.
      
    Most parameters are handled automatically by PyRegion's parameter get 
    mechanism. The ones that need special treatment are explicitly handled here.
    """

    if parameterName == 'activeOutputCount':
      return self.columnCount
    elif parameterName == 'spatialPoolerInput':
      return list(self._spatialPoolerInput.reshape(-1))
    elif parameterName == 'spatialPoolerOutput':
      return list(self._spatialPoolerOutput)
    elif parameterName == 'spNumActiveOutputs':
      return len(self._spatialPoolerOutput.nonzero()[0])
    elif parameterName == 'spOutputNonZeros':
      return [len(self._spatialPoolerOutput)] + \
              list(self._spatialPoolerOutput.nonzero()[0])
    elif parameterName == 'spInputNonZeros':
      import pdb; pdb.set_trace()
      return [len(self._spatialPoolerInput)] + \
              list(self._spatialPoolerInput.nonzero()[0])
    elif parameterName == 'spLearningStatsStr':
      try:
        return str(self._sfdr.getLearningStats())
      except:
        return str(dict())
    else:
      return PyRegion.getParameter(self, parameterName, index)