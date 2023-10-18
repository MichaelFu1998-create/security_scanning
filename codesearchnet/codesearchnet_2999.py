def FlagCxx14Features(filename, clean_lines, linenum, error):
  """Flag those C++14 features that we restrict.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  line = clean_lines.elided[linenum]

  include = Match(r'\s*#\s*include\s+[<"]([^<"]+)[">]', line)

  # Flag unapproved C++14 headers.
  if include and include.group(1) in ('scoped_allocator', 'shared_mutex'):
    error(filename, linenum, 'build/c++14', 5,
          ('<%s> is an unapproved C++14 header.') % include.group(1))