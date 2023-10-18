def getPermanence(self, columnIndex, permanence):
    """
    Returns the permanence values for a given column. ``permanence`` size
    must match the number of inputs.
    
    :param columnIndex: (int) column index to get permanence for.
    :param permanence: (list) will be overwritten with permanences. 
    """
    assert(columnIndex < self._numColumns)
    permanence[:] = self._permanences[columnIndex]