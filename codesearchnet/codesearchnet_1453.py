def getPosition(self):
    """Return the position of this particle. This returns a dict() of key
    value pairs where each key is the name of the flattened permutation
    variable and the value is its chosen value.

    Parameters:
    --------------------------------------------------------------
    retval:     dict() of flattened permutation choices
    """
    result = dict()
    for (varName, value) in self.permuteVars.iteritems():
      result[varName] = value.getPosition()

    return result