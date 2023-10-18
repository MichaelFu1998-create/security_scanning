def CheckCStyleCast(filename, clean_lines, linenum, cast_type, pattern, error):
  """Checks for a C-style cast by looking for the pattern.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    cast_type: The string for the C++ cast to recommend.  This is either
      reinterpret_cast, static_cast, or const_cast, depending.
    pattern: The regular expression used to find C-style casts.
    error: The function to call with any errors found.

  Returns:
    True if an error was emitted.
    False otherwise.
  """
  line = clean_lines.elided[linenum]
  match = Search(pattern, line)
  if not match:
    return False

  # Exclude lines with keywords that tend to look like casts
  context = line[0:match.start(1) - 1]
  if Match(r'.*\b(?:sizeof|alignof|alignas|[_A-Z][_A-Z0-9]*)\s*$', context):
    return False

  # Try expanding current context to see if we one level of
  # parentheses inside a macro.
  if linenum > 0:
    for i in xrange(linenum - 1, max(0, linenum - 5), -1):
      context = clean_lines.elided[i] + context
  if Match(r'.*\b[_A-Z][_A-Z0-9]*\s*\((?:\([^()]*\)|[^()])*$', context):
    return False

  # operator++(int) and operator--(int)
  if context.endswith(' operator++') or context.endswith(' operator--'):
    return False

  # A single unnamed argument for a function tends to look like old style cast.
  # If we see those, don't issue warnings for deprecated casts.
  remainder = line[match.end(0):]
  if Match(r'^\s*(?:;|const\b|throw\b|final\b|override\b|[=>{),]|->)',
           remainder):
    return False

  # At this point, all that should be left is actual casts.
  error(filename, linenum, 'readability/casting', 4,
        'Using C-style cast.  Use %s<%s>(...) instead' %
        (cast_type, match.group(1)))

  return True