def isSprintCompleted(self, sprintIdx):
    """Return True if the given sprint has completed."""
    numExistingSprints = len(self._state['sprints'])
    if sprintIdx >= numExistingSprints:
      return False

    return (self._state['sprints'][sprintIdx]['status'] == 'completed')