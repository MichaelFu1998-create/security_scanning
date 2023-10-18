def CheckCommaSpacing(filename, clean_lines, linenum, error):
  """Checks for horizontal spacing near commas and semicolons.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  raw = clean_lines.lines_without_raw_strings
  line = clean_lines.elided[linenum]

  # You should always have a space after a comma (either as fn arg or operator)
  #
  # This does not apply when the non-space character following the
  # comma is another comma, since the only time when that happens is
  # for empty macro arguments.
  #
  # We run this check in two passes: first pass on elided lines to
  # verify that lines contain missing whitespaces, second pass on raw
  # lines to confirm that those missing whitespaces are not due to
  # elided comments.
  if (Search(r',[^,\s]', ReplaceAll(r'\boperator\s*,\s*\(', 'F(', line)) and
      Search(r',[^,\s]', raw[linenum])):
    error(filename, linenum, 'whitespace/comma', 3,
          'Missing space after ,')

  # You should always have a space after a semicolon
  # except for few corner cases
  # TODO(unknown): clarify if 'if (1) { return 1;}' is requires one more
  # space after ;
  if Search(r';[^\s};\\)/]', line):
    error(filename, linenum, 'whitespace/semicolon', 3,
          'Missing space after ;')