def rCopy(d, f=identityConversion, discardNoneKeys=True, deepCopy=True):
  """Recursively copies a dict and returns the result.

  Args:
    d: The dict to copy.
    f: A function to apply to values when copying that takes the value and the
        list of keys from the root of the dict to the value and returns a value
        for the new dict.
    discardNoneKeys: If True, discard key-value pairs when f returns None for
        the value.
    deepCopy: If True, all values in returned dict are true copies (not the
        same object).
  Returns:
    A new dict with keys and values from d replaced with the result of f.
  """
  # Optionally deep copy the dict.
  if deepCopy:
    d = copy.deepcopy(d)

  newDict = {}
  toCopy = [(k, v, newDict, ()) for k, v in d.iteritems()]
  while len(toCopy) > 0:
    k, v, d, prevKeys = toCopy.pop()
    prevKeys = prevKeys + (k,)
    if isinstance(v, dict):
      d[k] = dict()
      toCopy[0:0] = [(innerK, innerV, d[k], prevKeys)
                     for innerK, innerV in v.iteritems()]
    else:
      #print k, v, prevKeys
      newV = f(v, prevKeys)
      if not discardNoneKeys or newV is not None:
        d[k] = newV
  return newDict