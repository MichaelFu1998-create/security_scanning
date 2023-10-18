def loadFromCheckpoint(savedModelDir, newSerialization=False):
    """ Load saved model.

    :param savedModelDir: (string)
           Directory of where the experiment is to be or was saved
    :returns: (:class:`nupic.frameworks.opf.model.Model`) The loaded model
              instance.
    """
    if newSerialization:
      return HTMPredictionModel.readFromCheckpoint(savedModelDir)
    else:
      return Model.load(savedModelDir)