def IsOutOfLineMethodDefinition(clean_lines, linenum):
  """Check if current line contains an out-of-line method definition.

  Args:
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
  Returns:
    True if current line contains an out-of-line method definition.
  """
  # Scan back a few lines for start of current function
  for i in xrange(linenum, max(-1, linenum - 10), -1):
    if Match(r'^([^()]*\w+)\(', clean_lines.elided[i]):
      return Match(r'^[^()]*\w+::\w+\(', clean_lines.elided[i]) is not None
  return False