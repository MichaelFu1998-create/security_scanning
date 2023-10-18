def getCompletingSwarms(self):
    """Return the list of all completing swarms.

    Parameters:
    ---------------------------------------------------------------------
    retval:   list of active swarm Ids
    """
    swarmIds = []
    for swarmId, info in self._state['swarms'].iteritems():
      if info['status'] == 'completing':
        swarmIds.append(swarmId)

    return swarmIds