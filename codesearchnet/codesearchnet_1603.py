def _getEphemeralMembers(self):
    """
    List of our member variables that we don't need to be saved
    """
    e = BacktrackingTM._getEphemeralMembers(self)
    if self.makeCells4Ephemeral:
      e.extend(['cells4'])
    return e