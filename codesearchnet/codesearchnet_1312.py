def modelsGetParams(self, modelIDs):
    """ Get the params and paramsHash for a set of models.

    WARNING!!!: The order of the results are NOT necessarily in the same order as
    the order of the model IDs passed in!!!

    Parameters:
    ----------------------------------------------------------------
    modelIDs:    list of model IDs
    retval:      list of result namedtuples defined in
                  ClientJobsDAO._models.getParamsNamedTuple. Each tuple
                  contains: (modelId, params, engParamsHash)
    """
    assert isinstance(modelIDs, self._SEQUENCE_TYPES), (
      "Wrong modelIDs type: %r") % (type(modelIDs),)
    assert len(modelIDs) >= 1, "modelIDs is empty"

    rows = self._getMatchingRowsWithRetries(
      self._models, {'model_id' : modelIDs},
      [self._models.pubToDBNameDict[f]
       for f in self._models.getParamsNamedTuple._fields])

    # NOTE: assertion will also fail when modelIDs contains duplicates
    assert len(rows) == len(modelIDs), "Didn't find modelIDs: %r" % (
      (set(modelIDs) - set(r[0] for r in rows)),)

    # Return the params and params hashes as a namedtuple
    return [self._models.getParamsNamedTuple._make(r) for r in rows]