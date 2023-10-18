def setParameter(self, parameterName, index, parameterValue):
    """
      Set the value of a Spec parameter. Most parameters are handled
      automatically by PyRegion's parameter set mechanism. The ones that need
      special treatment are explicitly handled here.
    """
    if parameterName == 'topDownMode':
      self.topDownMode = parameterValue
    elif parameterName == 'predictedField':
      self.predictedField = parameterValue
    else:
      raise Exception('Unknown parameter: ' + parameterName)