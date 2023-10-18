def _matchReportKeys(reportKeyREs=[], allReportKeys=[]):
  """
  Extract all items from the 'allKeys' list whose key matches one of the regular
  expressions passed in 'reportKeys'.

  Parameters:
  ----------------------------------------------------------------------------
  reportKeyREs:     List of regular expressions
  allReportKeys:    List of all keys

  retval:         list of keys from allReportKeys that match the regular expressions
                    in 'reportKeyREs'
                  If an invalid regular expression was included in 'reportKeys',
                    then BadKeyError() is raised
  """

  matchingReportKeys = []

  # Extract the report items of interest
  for keyRE in reportKeyREs:
    # Find all keys that match this regular expression
    matchObj = re.compile(keyRE)
    found = False
    for keyName in allReportKeys:
      match = matchObj.match(keyName)
      if match and match.end() == len(keyName):
        matchingReportKeys.append(keyName)
        found = True
    if not found:
      raise _BadKeyError(keyRE)

  return matchingReportKeys