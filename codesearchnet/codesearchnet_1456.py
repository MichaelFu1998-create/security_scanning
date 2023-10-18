def newPosition(self, whichVars=None):
    # TODO: incorporate data from choice variables....
    # TODO: make sure we're calling this when appropriate.
    """Choose a new position based on results obtained so far from all other
    particles.

    Parameters:
    --------------------------------------------------------------
    whichVars:       If not None, only move these variables
    retval:               new position
    """
    # Get the global best position for this swarm generation
    globalBestPosition = None
    # If speculative particles are enabled, use the global best considering
    #  even particles in the current generation. This gives better results
    #  but does not provide repeatable results because it depends on
    #  worker timing
    if self._hsObj._speculativeParticles:
      genIdx = self.genIdx
    else:
      genIdx = self.genIdx - 1

    if genIdx >= 0:
      (bestModelId, _) = self._resultsDB.bestModelIdAndErrScore(self.swarmId,
                                                                genIdx)
      if bestModelId is not None:
        (particleState, _, _, _, _) = self._resultsDB.getParticleInfo(
          bestModelId)
        globalBestPosition = Particle.getPositionFromState(particleState)

    # Update each variable
    for (varName, var) in self.permuteVars.iteritems():
      if whichVars is not None and varName not in whichVars:
        continue
      if globalBestPosition is None:
        var.newPosition(None, self._rng)
      else:
        var.newPosition(globalBestPosition[varName], self._rng)

    # get the new position
    position = self.getPosition()

    # Log the new position
    if self.logger.getEffectiveLevel() <= logging.DEBUG:
      msg = StringIO.StringIO()
      print >> msg, "New particle position: \n%s" % (pprint.pformat(position,
                                                                    indent=4))
      print >> msg, "Particle variables:"
      for (varName, var) in self.permuteVars.iteritems():
        print >> msg, "  %s: %s" % (varName, str(var))
      self.logger.debug(msg.getvalue())
      msg.close()

    return position