def getAllSwarms(self, sprintIdx):
    """Return the list of all swarms in the given sprint.

    Parameters:
    ---------------------------------------------------------------------
    retval:   list of active swarm Ids in the given sprint
    """
    swarmIds = []
    for swarmId, info in self._state['swarms'].iteritems():
      if info['sprintIdx'] == sprintIdx:
        swarmIds.append(swarmId)

    return swarmIds