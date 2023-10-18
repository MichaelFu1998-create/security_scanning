def _getParameterMethods(self, paramName):
    """Returns functions to set/get the parameter. These are
    the strongly typed functions get/setParameterUInt32, etc.
    The return value is a pair:
        setfunc, getfunc
    If the parameter is not available on this region, setfunc/getfunc
    are None. """
    if paramName in self._paramTypeCache:
      return self._paramTypeCache[paramName]
    try:
      # Catch the error here. We will re-throw in getParameter or
      # setParameter with a better error message than we could generate here
      paramSpec = self.getSpec().parameters.getByName(paramName)
    except:
      return (None, None)
    dataType = paramSpec.dataType
    dataTypeName = basicTypes[dataType]
    count = paramSpec.count
    if count == 1:
      # Dynamically generate the proper typed get/setParameter<dataType>
      x = 'etParameter' + dataTypeName
      try:
        g = getattr(self, 'g' + x) # get the typed getParameter method
        s = getattr(self, 's' + x) # get the typed setParameter method
      except AttributeError:
        raise Exception("Internal error: unknown parameter type %s" %
                        dataTypeName)
      info = (s, g)
    else:
      if dataTypeName == "Byte":
        info = (self.setParameterString, self.getParameterString)
      else:
        helper = _ArrayParameterHelper(self, dataType)
        info = (self.setParameterArray, helper.getParameterArray)

    self._paramTypeCache[paramName] = info
    return info