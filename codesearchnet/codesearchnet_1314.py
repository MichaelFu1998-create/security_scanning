def modelsGetUpdateCounters(self, jobID):
    """ Return info on all of the models that are in already in the models
    table for a given job. For each model, this returns a tuple
    containing: (modelID, updateCounter).

    Note that we don't return the results for all models, since the results
    string could be quite large. The information we are returning is
    just 2 integer fields.

    Parameters:
    ----------------------------------------------------------------
    jobID:      jobID to query
    retval:     (possibly empty) list of tuples. Each tuple contains:
                  (modelID, updateCounter)
    """
    rows = self._getMatchingRowsWithRetries(
      self._models, {'job_id' : jobID},
      [self._models.pubToDBNameDict[f]
       for f in self._models.getUpdateCountersNamedTuple._fields])

    # Return the results as a list of namedtuples
    return [self._models.getUpdateCountersNamedTuple._make(r) for r in rows]