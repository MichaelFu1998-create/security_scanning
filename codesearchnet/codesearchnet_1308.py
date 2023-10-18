def modelsGetFields(self, modelIDs, fields):
    """ Fetch the values of 1 or more fields from a sequence of model records.
    Here, 'fields' is a list with the names of the fields to fetch. The names
    are the public names of the fields (camelBack, not the lower_case_only form
    as stored in the DB).

    WARNING!!!: The order of the results are NOT necessarily in the same order
    as the order of the model IDs passed in!!!


    Parameters:
    ----------------------------------------------------------------
    modelIDs:      A single modelID or sequence of modelIDs
    fields:        A list  of fields to return

    Returns:  If modelIDs is a sequence:
                a list of tuples->(modelID, [field1, field2,...])
              If modelIDs is a single modelID:
                a list of field values->[field1, field2,...]
    """
    assert len(fields) >= 1, 'fields is empty'

    # Form the sequence of field name strings that will go into the
    #  request
    isSequence = isinstance(modelIDs, self._SEQUENCE_TYPES)

    if isSequence:
      assert len(modelIDs) >=1, 'modelIDs is empty'
    else:
      modelIDs = [modelIDs]

    rows = self._getMatchingRowsWithRetries(
      self._models, dict(model_id=modelIDs),
      ['model_id'] + [self._models.pubToDBNameDict[f] for f in fields])

    if len(rows) < len(modelIDs):
      raise RuntimeError("modelIDs not found within the models table: %s" % (
        (set(modelIDs) - set(r[0] for r in rows)),))

    if not isSequence:
      return list(rows[0][1:])

    return [(r[0], list(r[1:])) for r in rows]