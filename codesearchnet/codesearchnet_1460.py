def create(modelConfig, logLevel=logging.ERROR):
    """ Create a new model instance, given a description dictionary.

    :param modelConfig: (dict)
           A dictionary describing the current model,
           `described here <../../quick-start/example-model-params.html>`_.

    :param logLevel: (int) The level of logging output that should be generated

    :raises Exception: Unsupported model type

    :returns: :class:`nupic.frameworks.opf.model.Model`
    """
    logger = ModelFactory.__getLogger()
    logger.setLevel(logLevel)
    logger.debug("ModelFactory returning Model from dict: %s", modelConfig)

    modelClass = None
    if modelConfig['model'] == "HTMPrediction":
      modelClass = HTMPredictionModel
    elif modelConfig['model'] == "TwoGram":
      modelClass = TwoGramModel
    elif modelConfig['model'] == "PreviousValue":
      modelClass = PreviousValueModel
    else:
      raise Exception("ModelFactory received unsupported Model type: %s" % \
                      modelConfig['model'])

    return modelClass(**modelConfig['modelParams'])