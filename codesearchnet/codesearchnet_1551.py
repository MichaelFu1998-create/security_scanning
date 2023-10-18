def save(self, saveModelDir):
    """ Save the model in the given directory.

    :param saveModelDir: (string)
         Absolute directory path for saving the model. This directory should
         only be used to store a saved model. If the directory does not exist,
         it will be created automatically and populated with model data. A
         pre-existing directory will only be accepted if it contains previously
         saved model data. If such a directory is given, the full contents of
         the directory will be deleted and replaced with current model data.
    """
    logger = self._getLogger()
    logger.debug("(%s) Creating local checkpoint in %r...",
                       self, saveModelDir)

    modelPickleFilePath = self._getModelPickleFilePath(saveModelDir)

    # Clean up old saved state, if any
    if os.path.exists(saveModelDir):
      if not os.path.isdir(saveModelDir):
        raise Exception(("Existing filesystem entry <%s> is not a model"
                         " checkpoint -- refusing to delete (not a directory)") \
                          % saveModelDir)
      if not os.path.isfile(modelPickleFilePath):
        raise Exception(("Existing filesystem entry <%s> is not a model"
                         " checkpoint -- refusing to delete"\
                         " (%s missing or not a file)") % \
                          (saveModelDir, modelPickleFilePath))

      shutil.rmtree(saveModelDir)

    # Create a new directory for saving state
    self.__makeDirectoryFromAbsolutePath(saveModelDir)

    with open(modelPickleFilePath, 'wb') as modelPickleFile:
      logger.debug("(%s) Pickling Model instance...", self)

      pickle.dump(self, modelPickleFile, protocol=pickle.HIGHEST_PROTOCOL)

      logger.debug("(%s) Finished pickling Model instance", self)


    # Tell the model to save extra data, if any, that's too big for pickling
    self._serializeExtraData(extraDataDir=self._getModelExtraDataDir(saveModelDir))

    logger.debug("(%s) Finished creating local checkpoint", self)

    return