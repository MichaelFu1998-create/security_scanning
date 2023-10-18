def modelsGetResultAndStatus(self, modelIDs):
    """ Get the results string and other status fields for a set of models.

    WARNING!!!: The order of the results are NOT necessarily in the same order
    as the order of the model IDs passed in!!!

    For each model, this returns a tuple containing:
     (modelID, results, status, updateCounter, numRecords, completionReason,
         completionMsg, engParamsHash

    Parameters:
    ----------------------------------------------------------------
    modelIDs:    list of model IDs
    retval:      list of result tuples. Each tuple contains:
                    (modelID, results, status, updateCounter, numRecords,
                      completionReason, completionMsg, engParamsHash)
    """
    assert isinstance(modelIDs, self._SEQUENCE_TYPES), (
      "Wrong modelIDs type: %r") % type(modelIDs)
    assert len(modelIDs) >= 1, "modelIDs is empty"

    rows = self._getMatchingRowsWithRetries(
      self._models, {'model_id' : modelIDs},
      [self._models.pubToDBNameDict[f]
       for f in self._models.getResultAndStatusNamedTuple._fields])

    # NOTE: assertion will also fail when modelIDs contains duplicates
    assert len(rows) == len(modelIDs), "Didn't find modelIDs: %r" % (
      (set(modelIDs) - set(r[0] for r in rows)),)

    # Return the results as a list of namedtuples
    return [self._models.getResultAndStatusNamedTuple._make(r) for r in rows]