def rUpdate(original, updates):
  """Recursively updates the values in original with the values from updates."""
  # Keep a list of the sub-dictionaries that need to be updated to avoid having
  # to use recursion (which could fail for dictionaries with a lot of nesting.
  dictPairs = [(original, updates)]
  while len(dictPairs) > 0:
    original, updates = dictPairs.pop()
    for k, v in updates.iteritems():
      if k in original and isinstance(original[k], dict) and isinstance(v, dict):
        dictPairs.append((original[k], v))
      else:
        original[k] = v