def __createModelCheckpoint(self):
    """ Create a checkpoint from the current model, and store it in a dir named
    after checkpoint GUID, and finally store the GUID in the Models DB """

    if self._model is None or self._modelCheckpointGUID is None:
      return

    # Create an output store, if one doesn't exist already
    if self._predictionLogger is None:
      self._createPredictionLogger()

    predictions = StringIO.StringIO()
    self._predictionLogger.checkpoint(
      checkpointSink=predictions,
      maxRows=int(Configuration.get('nupic.model.checkpoint.maxPredictionRows')))

    self._model.save(os.path.join(self._experimentDir, str(self._modelCheckpointGUID)))
    self._jobsDAO.modelSetFields(modelID,
                                 {'modelCheckpointId':str(self._modelCheckpointGUID)},
                                 ignoreUnchanged=True)

    self._logger.info("Checkpointed Hypersearch Model: modelID: %r, "
                      "checkpointID: %r", self._modelID, checkpointID)
    return