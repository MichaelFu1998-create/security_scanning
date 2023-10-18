def recordDataPoint(self, swarmId, generation, errScore):
    """Record the best score for a swarm's generation index (x)
    Returns list of swarmIds to terminate.
    """
    terminatedSwarms = []

    # Append score to existing swarm.
    if swarmId in self.swarmScores:
      entry = self.swarmScores[swarmId]
      assert(len(entry) == generation)
      entry.append(errScore)

      entry = self.swarmBests[swarmId]
      entry.append(min(errScore, entry[-1]))

      assert(len(self.swarmBests[swarmId]) == len(self.swarmScores[swarmId]))
    else:
      # Create list of scores for a new swarm
      assert (generation == 0)
      self.swarmScores[swarmId] = [errScore]
      self.swarmBests[swarmId] = [errScore]

    # If the current swarm hasn't completed at least MIN_GENERATIONS, it should
    # not be candidate for maturation or termination. This prevents the initial
    # allocation of particles in PSO from killing off a field combination too
    # early.
    if generation + 1 < self.MATURITY_WINDOW:
      return terminatedSwarms

    # If the swarm has completed more than MAX_GENERATIONS, it should be marked
    # as mature, regardless of how its value is changing.
    if self.MAX_GENERATIONS is not None and generation > self.MAX_GENERATIONS:
      self._logger.info(
          'Swarm %s has matured (more than %d generations). Stopping' %
          (swarmId, self.MAX_GENERATIONS))
      terminatedSwarms.append(swarmId)

    if self._isTerminationEnabled:
      terminatedSwarms.extend(self._getTerminatedSwarms(generation))

    # Return which swarms to kill when we've reached maturity
    # If there is no change in the swarm's best for some time,
    # Mark it dead
    cumulativeBestScores = self.swarmBests[swarmId]
    if cumulativeBestScores[-1] == cumulativeBestScores[-self.MATURITY_WINDOW]:
      self._logger.info('Swarm %s has matured (no change in %d generations).'
                        'Stopping...'% (swarmId, self.MATURITY_WINDOW))
      terminatedSwarms.append(swarmId)

    self.terminatedSwarms = self.terminatedSwarms.union(terminatedSwarms)
    return terminatedSwarms