def escape(s):
  """
  Escape commas, tabs, newlines and dashes in a string

  Commas are encoded as tabs.

  :param s: (string) to escape
  :returns: (string) escaped string
  """
  if s is None:
    return ''

  assert isinstance(s, basestring), \
        "expected %s but got %s; value=%s" % (basestring, type(s), s)
  s = s.replace('\\', '\\\\')
  s = s.replace('\n', '\\n')
  s = s.replace('\t', '\\t')
  s = s.replace(',', '\t')
  return s