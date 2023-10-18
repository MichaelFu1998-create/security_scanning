def parseSdr(s):
  """
  Parses a string containing only 0's and 1's and return a Python list object.

  :param s: (string) string to parse
  :returns: (list) SDR out
  """
  assert isinstance(s, basestring)
  sdr = [int(c) for c in s if c in ("0", "1")]
  if len(sdr) != len(s):
    raise ValueError("The provided string %s is malformed. The string should "
                     "have only 0's and 1's.")

  return sdr