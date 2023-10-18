def __checkIfBestCompletedModel(self):
    """
    Reads the current "best model" for the job and returns whether or not the
    current model is better than the "best model" stored for the job

    Returns: (isBetter, storedBest, origResultsStr)

    isBetter:
      True if the current model is better than the stored "best model"
    storedResults:
      A dict of the currently stored results in the jobs table record
    origResultsStr:
      The json-encoded string that currently resides in the "results" field
      of the jobs record (used to create atomicity)
    """

    jobResultsStr = self._jobsDAO.jobGetFields(self._jobID, ['results'])[0]

    if jobResultsStr is None:
        jobResults = {}
    else:
      jobResults = json.loads(jobResultsStr)

    isSaved = jobResults.get('saved', False)
    bestMetric = jobResults.get('bestValue', None)

    currentMetric = self._getMetrics()[self._optimizedMetricLabel]
    self._isBestModel = (not isSaved) \
                        or (currentMetric < bestMetric)



    return self._isBestModel, jobResults, jobResultsStr