def _filterRecord(filterList, record):
  """ Takes a record and returns true if record meets filter criteria,
  false otherwise
  """

  for (fieldIdx, fp, params) in filterList:
    x = dict()
    x['value'] = record[fieldIdx]
    x['acceptValues'] = params['acceptValues']
    x['min'] = params['min']
    x['max'] = params['max']
    if not fp(x):
      return False

  # None of the field filters triggered, accept the record as a good one
  return True