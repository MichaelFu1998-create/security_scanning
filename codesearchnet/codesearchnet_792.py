def setLocalAreaDensity(self, localAreaDensity):
    """
    Sets the local area density. Invalidates the 'numActiveColumnsPerInhArea'
    parameter
    
    :param localAreaDensity: (float) value to set
    """
    assert(localAreaDensity > 0 and localAreaDensity <= 1)
    self._localAreaDensity = localAreaDensity
    self._numActiveColumnsPerInhArea = 0