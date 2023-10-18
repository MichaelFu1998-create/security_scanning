def CheckPrintf(filename, clean_lines, linenum, error):
  """Check for printf related issues.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  line = clean_lines.elided[linenum]

  # When snprintf is used, the second argument shouldn't be a literal.
  match = Search(r'snprintf\s*\(([^,]*),\s*([0-9]*)\s*,', line)
  if match and match.group(2) != '0':
    # If 2nd arg is zero, snprintf is used to calculate size.
    error(filename, linenum, 'runtime/printf', 3,
          'If you can, use sizeof(%s) instead of %s as the 2nd arg '
          'to snprintf.' % (match.group(1), match.group(2)))

  # Check if some verboten C functions are being used.
  if Search(r'\bsprintf\s*\(', line):
    error(filename, linenum, 'runtime/printf', 5,
          'Never use sprintf. Use snprintf instead.')
  match = Search(r'\b(strcpy|strcat)\s*\(', line)
  if match:
    error(filename, linenum, 'runtime/printf', 4,
          'Almost always, snprintf is better than %s' % match.group(1))