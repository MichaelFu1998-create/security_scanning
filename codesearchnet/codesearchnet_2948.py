def ReverseCloseExpression(clean_lines, linenum, pos):
  """If input points to ) or } or ] or >, finds the position that opens it.

  If lines[linenum][pos] points to a ')' or '}' or ']' or '>', finds the
  linenum/pos that correspond to the opening of the expression.

  Args:
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    pos: A position on the line.

  Returns:
    A tuple (line, linenum, pos) pointer *at* the opening brace, or
    (line, 0, -1) if we never find the matching opening brace.  Note
    we ignore strings and comments when matching; and the line we
    return is the 'cleansed' line at linenum.
  """
  line = clean_lines.elided[linenum]
  if line[pos] not in ')}]>':
    return (line, 0, -1)

  # Check last line
  (start_pos, stack) = FindStartOfExpressionInLine(line, pos, [])
  if start_pos > -1:
    return (line, linenum, start_pos)

  # Continue scanning backward
  while stack and linenum > 0:
    linenum -= 1
    line = clean_lines.elided[linenum]
    (start_pos, stack) = FindStartOfExpressionInLine(line, len(line) - 1, stack)
    if start_pos > -1:
      return (line, linenum, start_pos)

  # Did not find start of expression before beginning of file, give up
  return (line, 0, -1)