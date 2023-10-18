def readNamelist(namFilename, unique_glyphs=False, cache=None):
  """
  Args:
    namFilename: The path to the  Namelist file.
    unique_glyphs: Optional, whether to only include glyphs unique to subset.
    cache: Optional, a dict used to cache loaded Namelist files

  Returns:
  A dict with following keys:
  "fileName": (string) absolut path to namFilename
  "ownCharset": (set) the set of codepoints defined by the file itself
  "header": (dict) the result of _parseNamelistHeader
  "includes":
      (set) if unique_glyphs=False, the resulting dicts of readNamelist
            for each of the include files
      (None) if unique_glyphs=True
  "charset":
      (set) if unique_glyphs=False, the union of "ownCharset" and all
            "charset" items of each included file
      (None) if unique_glyphs=True

  If you are using  unique_glyphs=True and an external cache, don't expect
  the keys "includes" and "charset" to have a specific value.
  Depending on the state of cache, if unique_glyphs=True the returned
  dict may have None values for its "includes" and "charset" keys.
  """
  currentlyIncluding = set()
  if not cache:
    cache = {}
  return _readNamelist(currentlyIncluding, cache, namFilename, unique_glyphs)