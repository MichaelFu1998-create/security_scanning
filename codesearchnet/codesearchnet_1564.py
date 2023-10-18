def _isCheckpointDir(checkpointDir):
  """Return true iff checkpointDir appears to be a checkpoint directory."""
  lastSegment = os.path.split(checkpointDir)[1]
  if lastSegment[0] == '.':
    return False

  if not checkpointDir.endswith(g_defaultCheckpointExtension):
    return False

  if not os.path.isdir(checkpointDir):
    return False

  return True