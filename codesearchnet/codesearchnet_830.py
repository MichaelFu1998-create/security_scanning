def setParameter(self, paramName, value):
    """Set parameter value"""
    (setter, getter) = self._getParameterMethods(paramName)
    if setter is None:
      import exceptions
      raise exceptions.Exception(
          "setParameter -- parameter name '%s' does not exist in region %s of type %s"
          % (paramName, self.name, self.type))
    setter(paramName, value)