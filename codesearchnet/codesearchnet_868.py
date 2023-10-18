def anyGoodSprintsActive(self):
    """Return True if there are any more good sprints still being explored.
    A 'good' sprint is one that is earlier than where we detected an increase
    in error from sprint to subsequent sprint.
    """
    if self._state['lastGoodSprint'] is not None:
      goodSprints = self._state['sprints'][0:self._state['lastGoodSprint']+1]
    else:
      goodSprints = self._state['sprints']

    for sprint in goodSprints:
      if sprint['status'] == 'active':
        anyActiveSprints = True
        break
    else:
      anyActiveSprints = False

    return anyActiveSprints