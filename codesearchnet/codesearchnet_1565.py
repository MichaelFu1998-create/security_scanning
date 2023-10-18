def _printAvailableCheckpoints(experimentDir):
  """List available checkpoints for the specified experiment."""
  checkpointParentDir = getCheckpointParentDir(experimentDir)

  if not os.path.exists(checkpointParentDir):
    print "No available checkpoints."
    return

  checkpointDirs = [x for x in os.listdir(checkpointParentDir)
                    if _isCheckpointDir(os.path.join(checkpointParentDir, x))]
  if not checkpointDirs:
    print "No available checkpoints."
    return

  print "Available checkpoints:"
  checkpointList = [_checkpointLabelFromCheckpointDir(x)
                    for x in checkpointDirs]

  for checkpoint in sorted(checkpointList):
    print "\t", checkpoint

  print
  print "To start from a checkpoint:"
  print "  python run_opf_experiment.py experiment --load <CHECKPOINT>"
  print "For example, to start from the checkpoint \"MyCheckpoint\":"
  print "  python run_opf_experiment.py experiment --load MyCheckpoint"