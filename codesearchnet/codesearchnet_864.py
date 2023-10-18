def getCompletedSwarms(self):
    """Return the list of all completed swarms.

    Parameters:
    ---------------------------------------------------------------------
    retval:   list of active swarm Ids
    """
    swarmIds = []
    for swarmId, info in self._state['swarms'].iteritems():
      if info['status'] == 'completed':
        swarmIds.append(swarmId)

    return swarmIds