def _escape(s):
  """Escape commas, tabs, newlines and dashes in a string

  Commas are encoded as tabs
  """
  assert isinstance(s, str), \
        "expected %s but got %s; value=%s" % (type(str), type(s), s)
  s = s.replace("\\", "\\\\")
  s = s.replace("\n", "\\n")
  s = s.replace("\t", "\\t")
  s = s.replace(",", "\t")
  return s