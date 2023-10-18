def modelsInfo(self, modelIDs):
    """ Get ALL info for a set of models

    WARNING!!!: The order of the results are NOT necessarily in the same order as
    the order of the model IDs passed in!!!

    Parameters:
    ----------------------------------------------------------------
    modelIDs:    list of model IDs
    retval:      list of nametuples containing all the fields stored for each
                    model.
    """
    assert isinstance(modelIDs, self._SEQUENCE_TYPES), (
      "wrong modelIDs type: %s") % (type(modelIDs),)
    assert modelIDs, "modelIDs is empty"

    rows = self._getMatchingRowsWithRetries(
      self._models, dict(model_id=modelIDs),
      [self._models.pubToDBNameDict[f]
       for f in self._models.modelInfoNamedTuple._fields])

    results = [self._models.modelInfoNamedTuple._make(r) for r in rows]

    # NOTE: assetion will also fail if modelIDs contains duplicates
    assert len(results) == len(modelIDs), "modelIDs not found: %s" % (
      set(modelIDs) - set(r.modelId for r in results))

    return results