def matchPatterns(patterns, keys):
  """
  Returns a subset of the keys that match any of the given patterns

  :param patterns: (list) regular expressions to match
  :param keys: (list) keys to search for matches
  """
  results = []
  if patterns:
    for pattern in patterns:
      prog = re.compile(pattern)
      for key in keys:
        if prog.match(key):
          results.append(key)
  else:
    return None

  return results