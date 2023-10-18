def _appendReportKeys(keys, prefix, results):
  """
  Generate a set of possible report keys for an experiment's results.
  A report key is a string of key names separated by colons, each key being one
  level deeper into the experiment results dict. For example, 'key1:key2'.

  This routine is called recursively to build keys that are multiple levels
  deep from the results dict.

  Parameters:
  -----------------------------------------------------------
  keys:         Set of report keys accumulated so far
  prefix:       prefix formed so far, this is the colon separated list of key
                  names that led up to the dict passed in results
  results:      dictionary of results at this level.
  """

  allKeys = results.keys()
  allKeys.sort()
  for key in allKeys:
    if hasattr(results[key], 'keys'):
      _appendReportKeys(keys, "%s%s:" % (prefix, key), results[key])
    else:
      keys.add("%s%s" % (prefix, key))