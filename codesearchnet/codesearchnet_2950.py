def GetIndentLevel(line):
  """Return the number of leading spaces in line.

  Args:
    line: A string to check.

  Returns:
    An integer count of leading spaces, possibly zero.
  """
  indent = Match(r'^( *)\S', line)
  if indent:
    return len(indent.group(1))
  else:
    return 0