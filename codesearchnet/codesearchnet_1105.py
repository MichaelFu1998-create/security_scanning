def getParticleInfo(self, modelId):
    """Return particle info for a specific modelId.

    Parameters:
    ---------------------------------------------------------------------
    modelId:  which model Id

    retval:  (particleState, modelId, errScore, completed, matured)
    """
    entry = self._allResults[self._modelIDToIdx[modelId]]
    return (entry['modelParams']['particleState'], modelId, entry['errScore'],
            entry['completed'], entry['matured'])