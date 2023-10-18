def getPositionFromState(pState):
    """Return the position of a particle given its state dict.

    Parameters:
    --------------------------------------------------------------
    retval:     dict() of particle position, keys are the variable names,
                  values are their positions
    """
    result = dict()
    for (varName, value) in pState['varStates'].iteritems():
      result[varName] = value['position']

    return result