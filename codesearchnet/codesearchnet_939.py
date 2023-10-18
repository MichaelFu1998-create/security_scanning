def getParameterArray(self, name, index, a):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.getParameterArray`.

    TODO: as a temporary hack, getParameterArray checks to see if there's a
    variable, private or not, with that name. If so, it returns the value of the
    variable.
    """
    p = self.getParameter(name)
    if (not hasattr(p, '__len__')):
      raise Exception("Attempt to access parameter '%s' as an array but it is not an array" % name)

    if len(p) >  0:
      a[:] = p[:]