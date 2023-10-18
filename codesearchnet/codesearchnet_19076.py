def codepointsInNamelist(namFilename, unique_glyphs=False, cache=None):
  """Returns the set of codepoints contained in a given Namelist file.

  This is a replacement CodepointsInSubset and implements the "#$ include"
  header format.

  Args:
    namFilename: The path to the  Namelist file.
    unique_glyphs: Optional, whether to only include glyphs unique to subset.
  Returns:
    A set containing the glyphs in the subset.
  """
  key = 'charset' if not unique_glyphs else 'ownCharset'

  internals_dir = os.path.dirname(os.path.abspath(__file__))
  target = os.path.join(internals_dir, namFilename)
  result = readNamelist(target, unique_glyphs, cache)
  return result[key]