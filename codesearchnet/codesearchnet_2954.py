def CheckForBadCharacters(filename, lines, error):
  """Logs an error for each line containing bad characters.

  Two kinds of bad characters:

  1. Unicode replacement characters: These indicate that either the file
  contained invalid UTF-8 (likely) or Unicode replacement characters (which
  it shouldn't).  Note that it's possible for this to throw off line
  numbering if the invalid UTF-8 occurred adjacent to a newline.

  2. NUL bytes.  These are problematic for some tools.

  Args:
    filename: The name of the current file.
    lines: An array of strings, each representing a line of the file.
    error: The function to call with any errors found.
  """
  for linenum, line in enumerate(lines):
    if unicode_escape_decode('\ufffd') in line:
      error(filename, linenum, 'readability/utf8', 5,
            'Line contains invalid UTF-8 (or Unicode replacement character).')
    if '\0' in line:
      error(filename, linenum, 'readability/nul', 5, 'Line contains NUL byte.')