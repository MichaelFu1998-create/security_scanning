def _checkpointLabelFromCheckpointDir(checkpointDir):
  """Returns a checkpoint label string for the given model checkpoint directory

  checkpointDir: relative or absolute model checkpoint directory path
  """
  assert checkpointDir.endswith(g_defaultCheckpointExtension)

  lastSegment = os.path.split(checkpointDir)[1]

  checkpointLabel = lastSegment[0:-len(g_defaultCheckpointExtension)]

  return checkpointLabel