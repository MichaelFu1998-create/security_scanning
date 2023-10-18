def _writePrediction(self, result):
    """
    Writes the results of one iteration of a model. The results are written to
    this ModelRunner's in-memory cache unless this model is the "best model" for
    the job. If this model is the "best model", the predictions are written out
    to a permanent store via a prediction output stream instance


    Parameters:
    -----------------------------------------------------------------------
    result:      A opf_utils.ModelResult object, which contains the input and
                  output for this iteration
    """
    self.__predictionCache.append(result)

    if self._isBestModel:
     self.__flushPredictionCache()