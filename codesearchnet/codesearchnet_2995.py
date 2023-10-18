def CheckRedundantVirtual(filename, clean_lines, linenum, error):
  """Check if line contains a redundant "virtual" function-specifier.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  # Look for "virtual" on current line.
  line = clean_lines.elided[linenum]
  virtual = Match(r'^(.*)(\bvirtual\b)(.*)$', line)
  if not virtual: return

  # Ignore "virtual" keywords that are near access-specifiers.  These
  # are only used in class base-specifier and do not apply to member
  # functions.
  if (Search(r'\b(public|protected|private)\s+$', virtual.group(1)) or
      Match(r'^\s+(public|protected|private)\b', virtual.group(3))):
    return

  # Ignore the "virtual" keyword from virtual base classes.  Usually
  # there is a column on the same line in these cases (virtual base
  # classes are rare in google3 because multiple inheritance is rare).
  if Match(r'^.*[^:]:[^:].*$', line): return

  # Look for the next opening parenthesis.  This is the start of the
  # parameter list (possibly on the next line shortly after virtual).
  # TODO(unknown): doesn't work if there are virtual functions with
  # decltype() or other things that use parentheses, but csearch suggests
  # that this is rare.
  end_col = -1
  end_line = -1
  start_col = len(virtual.group(2))
  for start_line in xrange(linenum, min(linenum + 3, clean_lines.NumLines())):
    line = clean_lines.elided[start_line][start_col:]
    parameter_list = Match(r'^([^(]*)\(', line)
    if parameter_list:
      # Match parentheses to find the end of the parameter list
      (_, end_line, end_col) = CloseExpression(
          clean_lines, start_line, start_col + len(parameter_list.group(1)))
      break
    start_col = 0

  if end_col < 0:
    return  # Couldn't find end of parameter list, give up

  # Look for "override" or "final" after the parameter list
  # (possibly on the next few lines).
  for i in xrange(end_line, min(end_line + 3, clean_lines.NumLines())):
    line = clean_lines.elided[i][end_col:]
    match = Search(r'\b(override|final)\b', line)
    if match:
      error(filename, linenum, 'readability/inheritance', 4,
            ('"virtual" is redundant since function is '
             'already declared as "%s"' % match.group(1)))

    # Set end_col to check whole lines after we are done with the
    # first line.
    end_col = 0
    if Search(r'[^\w]\s*$', line):
      break