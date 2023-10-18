def firstNonFullGeneration(self, swarmId, minNumParticles):
    """ Return the generation index of the first generation in the given
    swarm that does not have numParticles particles in it, either still in the
    running state or completed. This does not include orphaned particles.

    Parameters:
    ---------------------------------------------------------------------
    swarmId:  A string representation of the sorted list of encoders in this
                 swarm. For example '__address_encoder.__gym_encoder'
    minNumParticles: minium number of partices required for a full
                  generation.

    retval:  generation index, or None if no particles at all.
    """

    if not swarmId in self._swarmNumParticlesPerGeneration:
      return None

    numPsPerGen = self._swarmNumParticlesPerGeneration[swarmId]

    numPsPerGen = numpy.array(numPsPerGen)
    firstNonFull = numpy.where(numPsPerGen < minNumParticles)[0]
    if len(firstNonFull) == 0:
      return len(numPsPerGen)
    else:
      return firstNonFull[0]