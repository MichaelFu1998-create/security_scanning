def FindCheckMacro(line):
  """Find a replaceable CHECK-like macro.

  Args:
    line: line to search on.
  Returns:
    (macro name, start position), or (None, -1) if no replaceable
    macro is found.
  """
  for macro in _CHECK_MACROS:
    i = line.find(macro)
    if i >= 0:
      # Find opening parenthesis.  Do a regular expression match here
      # to make sure that we are matching the expected CHECK macro, as
      # opposed to some other macro that happens to contain the CHECK
      # substring.
      matched = Match(r'^(.*\b' + macro + r'\s*)\(', line)
      if not matched:
        continue
      return (macro, len(matched.group(1)))
  return (None, -1)