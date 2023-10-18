def getState(self):
    """Get the particle state as a dict. This is enough information to
    instantiate this particle on another worker."""
    varStates = dict()
    for varName, var in self.permuteVars.iteritems():
      varStates[varName] = var.getState()

    return dict(id=self.particleId,
                genIdx=self.genIdx,
                swarmId=self.swarmId,
                varStates=varStates)