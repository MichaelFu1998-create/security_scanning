def getLabels(self, start=None, end=None):
    """
    Get the labels on classified points within range start to end. Not inclusive
    of end.

    :returns: (dict) with format:

      ::

        {
          'isProcessing': boolean,
          'recordLabels': list of results
        }

      ``isProcessing`` - currently always false as recalculation blocks; used if
      reprocessing of records is still being performed;

      Each item in ``recordLabels`` is of format:
      
      ::
      
        {
          'ROWID': id of the row,
          'labels': list of strings
        }

    """
    if len(self._recordsCache) == 0:
      return {
        'isProcessing': False,
        'recordLabels': []
      }
    try:
      start = int(start)
    except Exception:
      start = 0

    try:
      end = int(end)
    except Exception:
      end = self._recordsCache[-1].ROWID

    if end <= start:
      raise HTMPredictionModelInvalidRangeError("Invalid supplied range for 'getLabels'.",
                                                debugInfo={
          'requestRange': {
            'startRecordID': start,
            'endRecordID': end
          },
          'numRecordsStored': len(self._recordsCache)
        })

    results = {
      'isProcessing': False,
      'recordLabels': []
    }

    ROWIDX = numpy.array(
        self._knnclassifier.getParameter('categoryRecencyList'))
    validIdx = numpy.where((ROWIDX >= start) & (ROWIDX < end))[0].tolist()
    categories = self._knnclassifier.getCategoryList()
    for idx in validIdx:
      row = dict(
        ROWID=int(ROWIDX[idx]),
        labels=self._categoryToLabelList(categories[idx]))
      results['recordLabels'].append(row)

    return results