def CheckRedundantOverrideOrFinal(filename, clean_lines, linenum, error):
  """Check if line contains a redundant "override" or "final" virt-specifier.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  # Look for closing parenthesis nearby.  We need one to confirm where
  # the declarator ends and where the virt-specifier starts to avoid
  # false positives.
  line = clean_lines.elided[linenum]
  declarator_end = line.rfind(')')
  if declarator_end >= 0:
    fragment = line[declarator_end:]
  else:
    if linenum > 1 and clean_lines.elided[linenum - 1].rfind(')') >= 0:
      fragment = line
    else:
      return

  # Check that at most one of "override" or "final" is present, not both
  if Search(r'\boverride\b', fragment) and Search(r'\bfinal\b', fragment):
    error(filename, linenum, 'readability/inheritance', 4,
          ('"override" is redundant since function is '
           'already declared as "final"'))