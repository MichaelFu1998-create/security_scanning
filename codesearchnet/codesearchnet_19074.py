def _readNamelist(currentlyIncluding, cache, namFilename, unique_glyphs):
  """ Detect infinite recursion and prevent it.

  This is an implementation detail of readNamelist.

  Raises NamelistRecursionError if namFilename is in the process of being included
  """
  # normalize
  filename = os.path.abspath(os.path.normcase(namFilename))
  if filename in currentlyIncluding:
    raise NamelistRecursionError(filename)
  currentlyIncluding.add(filename)
  try:
    result = __readNamelist(cache, filename, unique_glyphs)
  finally:
    currentlyIncluding.remove(filename)
  return result