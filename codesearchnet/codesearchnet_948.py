def getParameter(self, parameterName, index=-1):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.getParameter`.

    Get the value of a parameter. Most parameters are handled automatically by
    :class:`~nupic.bindings.regions.PyRegion.PyRegion`'s parameter get mechanism. The 
    ones that need special treatment are explicitly handled here.
    """
    if parameterName in self._temporalArgNames:
      return getattr(self._tfdr, parameterName)
    else:
      return PyRegion.getParameter(self, parameterName, index)