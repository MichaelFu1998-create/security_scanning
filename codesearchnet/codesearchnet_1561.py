def _getModelCheckpointDir(experimentDir, checkpointLabel):
  """Creates directory for serialization of the model

  checkpointLabel:
      Checkpoint label (string)

  Returns:
    absolute path to the serialization directory
  """
  checkpointDir = os.path.join(getCheckpointParentDir(experimentDir),
                               checkpointLabel + g_defaultCheckpointExtension)
  checkpointDir = os.path.abspath(checkpointDir)

  return checkpointDir