def CheckAltTokens(filename, clean_lines, linenum, error):
  """Check alternative keywords being used in boolean expressions.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  line = clean_lines.elided[linenum]

  # Avoid preprocessor lines
  if Match(r'^\s*#', line):
    return

  # Last ditch effort to avoid multi-line comments.  This will not help
  # if the comment started before the current line or ended after the
  # current line, but it catches most of the false positives.  At least,
  # it provides a way to workaround this warning for people who use
  # multi-line comments in preprocessor macros.
  #
  # TODO(unknown): remove this once cpplint has better support for
  # multi-line comments.
  if line.find('/*') >= 0 or line.find('*/') >= 0:
    return

  for match in _ALT_TOKEN_REPLACEMENT_PATTERN.finditer(line):
    error(filename, linenum, 'readability/alt_tokens', 2,
          'Use operator %s instead of %s' % (
              _ALT_TOKEN_REPLACEMENT[match.group(1)], match.group(1)))