def ParseNolintSuppressions(filename, raw_line, linenum, error):
  """Updates the global list of line error-suppressions.

  Parses any NOLINT comments on the current line, updating the global
  error_suppressions store.  Reports an error if the NOLINT comment
  was malformed.

  Args:
    filename: str, the name of the input file.
    raw_line: str, the line of input text, with comments.
    linenum: int, the number of the current line.
    error: function, an error handler.
  """
  matched = Search(r'\bNOLINT(NEXTLINE)?\b(\([^)]+\))?', raw_line)
  if matched:
    if matched.group(1):
      suppressed_line = linenum + 1
    else:
      suppressed_line = linenum
    category = matched.group(2)
    if category in (None, '(*)'):  # => "suppress all"
      _error_suppressions.setdefault(None, set()).add(suppressed_line)
    else:
      if category.startswith('(') and category.endswith(')'):
        category = category[1:-1]
        if category in _ERROR_CATEGORIES:
          _error_suppressions.setdefault(category, set()).add(suppressed_line)
        elif category not in _LEGACY_ERROR_CATEGORIES:
          error(filename, linenum, 'readability/nolint', 5,
                'Unknown NOLINT error category: %s' % category)