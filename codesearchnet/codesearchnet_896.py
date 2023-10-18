def sortedJSONDumpS(obj):
  """
  Return a JSON representation of obj with sorted keys on any embedded dicts.
  This insures that the same object will always be represented by the same
  string even if it contains dicts (where the sort order of the keys is
  normally undefined).
  """

  itemStrs = []

  if isinstance(obj, dict):
    items = obj.items()
    items.sort()
    for key, value in items:
      itemStrs.append('%s: %s' % (json.dumps(key), sortedJSONDumpS(value)))
    return '{%s}' % (', '.join(itemStrs))

  elif hasattr(obj, '__iter__'):
    for val in obj:
      itemStrs.append(sortedJSONDumpS(val))
    return '[%s]' % (', '.join(itemStrs))

  else:
    return json.dumps(obj)