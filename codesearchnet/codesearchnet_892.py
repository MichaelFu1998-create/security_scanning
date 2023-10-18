def rApply(d, f):
  """Recursively applies f to the values in dict d.

  Args:
    d: The dict to recurse over.
    f: A function to apply to values in d that takes the value and a list of
        keys from the root of the dict to the value.
  """
  remainingDicts = [(d, ())]
  while len(remainingDicts) > 0:
    current, prevKeys = remainingDicts.pop()
    for k, v in current.iteritems():
      keys = prevKeys + (k,)
      if isinstance(v, dict):
        remainingDicts.insert(0, (v, keys))
      else:
        f(v, keys)