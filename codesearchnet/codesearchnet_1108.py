def getMaturedSwarmGenerations(self):
    """Return a list of swarm generations that have completed and the
    best (minimal) errScore seen for each of them.

    Parameters:
    ---------------------------------------------------------------------
    retval:  list of tuples. Each tuple is of the form:
              (swarmId, genIdx, bestErrScore)
    """
    # Return results go in this list
    result = []


    # For each of the swarm generations which have had model result updates
    # since the last time we were called, see which have completed.
    modifiedSwarmGens = sorted(self._modifiedSwarmGens)

    # Walk through them in order from lowest to highest generation index
    for key in modifiedSwarmGens:
      (swarmId, genIdx) = key

      # Skip it if we've already reported on it. This should happen rarely, if
      #  ever. It means that some worker has started and completed a model in
      #  this generation after we've determined that the generation has ended.
      if key in self._maturedSwarmGens:
        self._modifiedSwarmGens.remove(key)
        continue

      # If the previous generation for this swarm is not complete yet, don't
      #  bother evaluating this one.
      if (genIdx >= 1) and not (swarmId, genIdx-1) in self._maturedSwarmGens:
        continue

      # We found a swarm generation that had some results reported since last
      # time, see if it's complete or not
      (_, _, errScores, completedFlags, maturedFlags) = \
                                self.getParticleInfos(swarmId, genIdx)
      maturedFlags = numpy.array(maturedFlags)
      numMatured = maturedFlags.sum()
      if numMatured >= self._hsObj._minParticlesPerSwarm \
            and numMatured == len(maturedFlags):
        errScores = numpy.array(errScores)
        bestScore = errScores.min()

        self._maturedSwarmGens.add(key)
        self._modifiedSwarmGens.remove(key)
        result.append((swarmId, genIdx, bestScore))

    # Return results
    return result