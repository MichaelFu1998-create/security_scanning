def _saveModel(model, experimentDir, checkpointLabel, newSerialization=False):
  """Save model"""
  checkpointDir = _getModelCheckpointDir(experimentDir, checkpointLabel)
  if newSerialization:
    model.writeToCheckpoint(checkpointDir)
  else:
    model.save(saveModelDir=checkpointDir)