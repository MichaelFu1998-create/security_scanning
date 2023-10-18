def getParameter(self, paramName):
    """Get parameter value"""
    (setter, getter) = self._getParameterMethods(paramName)
    if getter is None:
      import exceptions
      raise exceptions.Exception(
          "getParameter -- parameter name '%s' does not exist in region %s of type %s"
          % (paramName, self.name, self.type))
    return getter(paramName)