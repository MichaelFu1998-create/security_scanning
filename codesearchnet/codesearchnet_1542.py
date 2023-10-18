def _createAggregateRecord(self):
    """ Generate the aggregated output record

    Parameters:
    ------------------------------------------------------------------------
    retval: outputRecord

    """

    record = []

    for i, (fieldIdx, aggFP, paramIdx) in enumerate(self._fields):
      if aggFP is None: # this field is not supposed to be aggregated.
        continue

      values = self._slice[i]
      refIndex = None
      if paramIdx is not None:
        record.append(aggFP(values, self._slice[paramIdx]))
      else:
        record.append(aggFP(values))

    return record