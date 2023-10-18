def dictDiff(da, db):
  """ Compares two python dictionaries at the top level and return differences

  da:             first dictionary
  db:             second dictionary

  Returns:        None if dictionaries test equal; otherwise returns a
                  dictionary as follows:
                  {
                    'inAButNotInB':
                        <sequence of keys that are in da but not in db>
                    'inBButNotInA':
                        <sequence of keys that are in db but not in da>
                    'differentValues':
                        <sequence of keys whose corresponding values differ
                         between da and db>
                  }
  """
  different = False

  resultDict = dict()

  resultDict['inAButNotInB'] = set(da) - set(db)
  if resultDict['inAButNotInB']:
    different = True

  resultDict['inBButNotInA'] = set(db) - set(da)
  if resultDict['inBButNotInA']:
    different = True

  resultDict['differentValues'] = []
  for key in (set(da) - resultDict['inAButNotInB']):
    comparisonResult = da[key] == db[key]
    if isinstance(comparisonResult, bool):
      isEqual = comparisonResult
    else:
      # This handles numpy arrays (but only at the top level)
      isEqual = comparisonResult.all()
    if not isEqual:
      resultDict['differentValues'].append(key)
      different = True

  assert (((resultDict['inAButNotInB'] or resultDict['inBButNotInA'] or
          resultDict['differentValues']) and different) or not different)

  return resultDict if different else None