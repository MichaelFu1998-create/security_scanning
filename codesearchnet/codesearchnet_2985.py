def IsDerivedFunction(clean_lines, linenum):
  """Check if current line contains an inherited function.

  Args:
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
  Returns:
    True if current line contains a function with "override"
    virt-specifier.
  """
  # Scan back a few lines for start of current function
  for i in xrange(linenum, max(-1, linenum - 10), -1):
    match = Match(r'^([^()]*\w+)\(', clean_lines.elided[i])
    if match:
      # Look for "override" after the matching closing parenthesis
      line, _, closing_paren = CloseExpression(
          clean_lines, i, len(match.group(1)))
      return (closing_paren >= 0 and
              Search(r'\boverride\b', line[closing_paren:]))
  return False