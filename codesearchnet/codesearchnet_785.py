def _getStateAnomalyVector(self, state):
    """
    Returns a state's anomaly vertor converting it from spare to dense
    """
    vector = numpy.zeros(self._anomalyVectorLength)
    vector[state.anomalyVector] = 1
    return vector