def load(cls, savedModelDir):
    """ Load saved model.

    :param savedModelDir: (string)
           Directory of where the experiment is to be or was saved
    :returns: (:class:`Model`) The loaded model instance
    """
    logger = opf_utils.initLogger(cls)
    logger.debug("Loading model from local checkpoint at %r...", savedModelDir)

    # Load the model
    modelPickleFilePath = Model._getModelPickleFilePath(savedModelDir)

    with open(modelPickleFilePath, 'rb') as modelPickleFile:
      logger.debug("Unpickling Model instance...")

      model = pickle.load(modelPickleFile)

      logger.debug("Finished unpickling Model instance")

    # Tell the model to load extra data, if any, that was too big for pickling
    model._deSerializeExtraData(
        extraDataDir=Model._getModelExtraDataDir(savedModelDir))

    logger.debug("Finished Loading model from local checkpoint")

    return model