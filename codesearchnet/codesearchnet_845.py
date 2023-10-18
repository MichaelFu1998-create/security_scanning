def __deleteModelCheckpoint(self, modelID):
    """
    Delete the stored checkpoint for the specified modelID. This function is
    called if the current model is now the best model, making the old model's
    checkpoint obsolete

    Parameters:
    -----------------------------------------------------------------------
    modelID:      The modelID for the checkpoint to delete. This is NOT the
                  unique checkpointID
    """

    checkpointID = \
        self._jobsDAO.modelsGetFields(modelID, ['modelCheckpointId'])[0]

    if checkpointID is None:
      return

    try:
      shutil.rmtree(os.path.join(self._experimentDir, str(self._modelCheckpointGUID)))
    except:
      self._logger.warn("Failed to delete model checkpoint %s. "\
                        "Assuming that another worker has already deleted it",
                        checkpointID)
      return

    self._jobsDAO.modelSetFields(modelID,
                                 {'modelCheckpointId':None},
                                 ignoreUnchanged=True)
    return