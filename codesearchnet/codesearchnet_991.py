def parseStringList(s):
  """
  Parse a string of space-separated numbers, returning a Python list.

  :param s: (string) to parse
  :returns: (list) binary SDR
  """
  assert isinstance(s, basestring)
  return [int(i) for i in s.split()]