def IsInitializerList(clean_lines, linenum):
  """Check if current line is inside constructor initializer list.

  Args:
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
  Returns:
    True if current line appears to be inside constructor initializer
    list, False otherwise.
  """
  for i in xrange(linenum, 1, -1):
    line = clean_lines.elided[i]
    if i == linenum:
      remove_function_body = Match(r'^(.*)\{\s*$', line)
      if remove_function_body:
        line = remove_function_body.group(1)

    if Search(r'\s:\s*\w+[({]', line):
      # A lone colon tend to indicate the start of a constructor
      # initializer list.  It could also be a ternary operator, which
      # also tend to appear in constructor initializer lists as
      # opposed to parameter lists.
      return True
    if Search(r'\}\s*,\s*$', line):
      # A closing brace followed by a comma is probably the end of a
      # brace-initialized member in constructor initializer list.
      return True
    if Search(r'[{};]\s*$', line):
      # Found one of the following:
      # - A closing brace or semicolon, probably the end of the previous
      #   function.
      # - An opening brace, probably the start of current class or namespace.
      #
      # Current line is probably not inside an initializer list since
      # we saw one of those things without seeing the starting colon.
      return False

  # Got to the beginning of the file without seeing the start of
  # constructor initializer list.
  return False