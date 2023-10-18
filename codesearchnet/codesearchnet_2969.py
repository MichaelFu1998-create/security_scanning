def IsDecltype(clean_lines, linenum, column):
  """Check if the token ending on (linenum, column) is decltype().

  Args:
    clean_lines: A CleansedLines instance containing the file.
    linenum: the number of the line to check.
    column: end column of the token to check.
  Returns:
    True if this token is decltype() expression, False otherwise.
  """
  (text, _, start_col) = ReverseCloseExpression(clean_lines, linenum, column)
  if start_col < 0:
    return False
  if Search(r'\bdecltype\s*$', text[0:start_col]):
    return True
  return False