def _getReportItem(itemName, results):
  """
  Get a specific item by name out of the results dict.

  The format of itemName is a string of dictionary keys separated by colons,
  each key being one level deeper into the results dict. For example,
  'key1:key2' would fetch results['key1']['key2'].

  If itemName is not found in results, then None is returned

  """

  subKeys = itemName.split(':')
  subResults = results
  for subKey in subKeys:
    subResults = subResults[subKey]

  return subResults