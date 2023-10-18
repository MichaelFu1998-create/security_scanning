def unescape(s):
  """
  Unescapes a string that may contain commas, tabs, newlines and dashes

  Commas are decoded from tabs.

  :param s: (string) to unescape
  :returns: (string) unescaped string
  """
  assert isinstance(s, basestring)
  s = s.replace('\t', ',')
  s = s.replace('\\,', ',')
  s = s.replace('\\n', '\n')
  s = s.replace('\\\\', '\\')

  return s