def setPermanence(self, columnIndex, permanence):
    """
    Sets the permanence values for a given column. ``permanence`` size must 
    match the number of inputs.
    
    :param columnIndex: (int) column index to set permanence for.
    :param permanence: (list) value to set. 
    """
    assert(columnIndex < self._numColumns)
    self._updatePermanencesForColumn(permanence, columnIndex, raisePerm=False)