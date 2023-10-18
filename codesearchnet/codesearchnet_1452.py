def copyVarStatesFrom(self, particleState, varNames):
    """Copy specific variables from particleState into this particle.

    Parameters:
    --------------------------------------------------------------
    particleState:        dict produced by a particle's getState() method
    varNames:             which variables to copy
    """
    # Set this to false if you don't want the variable to move anymore
    #  after we set the state
    allowedToMove = True

    for varName in particleState['varStates']:
      if varName in varNames:

        # If this particle doesn't include this field, don't copy it
        if varName not in self.permuteVars:
          continue

        # Set the best position to the copied position
        state = copy.deepcopy(particleState['varStates'][varName])
        state['_position'] = state['position']
        state['bestPosition'] = state['position']

        if not allowedToMove:
          state['velocity'] = 0

        # Set the state now
        self.permuteVars[varName].setState(state)

        if allowedToMove:
          # Let the particle move in both directions from the best position
          #  it found previously and set it's initial velocity to a known
          #  fraction of the total distance.
          self.permuteVars[varName].resetVelocity(self._rng)