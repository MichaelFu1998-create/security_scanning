def getParameterArrayCount(self, name, index):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.getParameterArrayCount`.

    TODO: as a temporary hack, getParameterArrayCount checks to see if there's a
    variable, private or not, with that name. If so, it returns the value of the
    variable.
    """
    p = self.getParameter(name)
    if (not hasattr(p, '__len__')):
      raise Exception("Attempt to access parameter '%s' as an array but it is not an array" % name)
    return len(p)