def UpdateIncludeState(filename, include_dict, io=codecs):
  """Fill up the include_dict with new includes found from the file.

  Args:
    filename: the name of the header to read.
    include_dict: a dictionary in which the headers are inserted.
    io: The io factory to use to read the file. Provided for testability.

  Returns:
    True if a header was successfully added. False otherwise.
  """
  headerfile = None
  try:
    headerfile = io.open(filename, 'r', 'utf8', 'replace')
  except IOError:
    return False
  linenum = 0
  for line in headerfile:
    linenum += 1
    clean_line = CleanseComments(line)
    match = _RE_PATTERN_INCLUDE.search(clean_line)
    if match:
      include = match.group(2)
      include_dict.setdefault(include, linenum)
  return True