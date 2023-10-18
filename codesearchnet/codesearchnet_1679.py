def _setTPDynamicState(self, tpDynamicState):
    """
    Set all the dynamic state variables from the <tpDynamicState> dict.

    <tpDynamicState> dict has all the dynamic state variable names as keys and
    their values at this instant as values.

    We set the dynamic state variables in the tm object with these items.
    """
    for variableName in self._getTPDynamicStateVariableNames():
      self.__dict__[variableName] = tpDynamicState.pop(variableName)