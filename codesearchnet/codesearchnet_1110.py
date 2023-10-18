def getResultsPerChoice(self, swarmId, maxGenIdx, varName):
    """ Return a dict of the errors obtained on models that were run with
    each value from a PermuteChoice variable.

    For example, if a PermuteChoice variable has the following choices:
      ['a', 'b', 'c']

    The dict will have 3 elements. The keys are the stringified choiceVars,
    and each value is tuple containing (choiceVar, errors) where choiceVar is
    the original form of the choiceVar (before stringification) and errors is
    the list of errors received from models that used the specific choice:
    retval:
      ['a':('a', [0.1, 0.2, 0.3]), 'b':('b', [0.5, 0.1, 0.6]), 'c':('c', [])]


    Parameters:
    ---------------------------------------------------------------------
    swarmId:  swarm Id of the swarm to retrieve info from
    maxGenIdx: max generation index to consider from other models, ignored
                if None
    varName:  which variable to retrieve

    retval:  list of the errors obtained from each choice.
    """
    results = dict()
    # Get all the completed particles in this swarm
    (allParticles, _, resultErrs, _, _) = self.getParticleInfos(swarmId,
                                              genIdx=None, matured=True)

    for particleState, resultErr in itertools.izip(allParticles, resultErrs):
      # Consider this generation?
      if maxGenIdx is not None:
        if particleState['genIdx'] > maxGenIdx:
          continue

      # Ignore unless this model completed successfully
      if resultErr == numpy.inf:
        continue

      position = Particle.getPositionFromState(particleState)
      varPosition = position[varName]
      varPositionStr = str(varPosition)
      if varPositionStr in results:
        results[varPositionStr][1].append(resultErr)
      else:
        results[varPositionStr] = (varPosition, [resultErr])

    return results