def getCheckpointParentDir(experimentDir):
  """Get checkpoint parent dir.

  Returns: absolute path to the base serialization directory within which
      model checkpoints for this experiment are created
  """
  baseDir = os.path.join(experimentDir, "savedmodels")
  baseDir = os.path.abspath(baseDir)

  return baseDir