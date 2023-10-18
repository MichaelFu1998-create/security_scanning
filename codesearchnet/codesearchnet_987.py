def parseBool(s):
  """
  String to boolean

  :param s: (string)
  :return: (bool)
  """
  l = s.lower()
  if l in ("true", "t", "1"):
    return True
  if l in ("false", "f", "0"):
    return False
  raise Exception("Unable to convert string '%s' to a boolean value" % s)