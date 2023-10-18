def _getTPDynamicState(self,):
    """
    Parameters:
    --------------------------------------------
    retval:       A dict with all the dynamic state variable names as keys and
                  their values at this instant as values.
    """
    tpDynamicState = dict()
    for variableName in self._getTPDynamicStateVariableNames():
      tpDynamicState[variableName] = copy.deepcopy(self.__dict__[variableName])
    return tpDynamicState