def CheckForHeaderGuard(filename, clean_lines, error):
  """Checks that the file contains a header guard.

  Logs an error if no #ifndef header guard is present.  For other
  headers, checks that the full pathname is used.

  Args:
    filename: The name of the C++ header file.
    clean_lines: A CleansedLines instance containing the file.
    error: The function to call with any errors found.
  """

  # Don't check for header guards if there are error suppression
  # comments somewhere in this file.
  #
  # Because this is silencing a warning for a nonexistent line, we
  # only support the very specific NOLINT(build/header_guard) syntax,
  # and not the general NOLINT or NOLINT(*) syntax.
  raw_lines = clean_lines.lines_without_raw_strings
  for i in raw_lines:
    if Search(r'//\s*NOLINT\(build/header_guard\)', i):
      return

  # Allow pragma once instead of header guards
  for i in raw_lines:
    if Search(r'^\s*#pragma\s+once', i):
      return

  cppvar = GetHeaderGuardCPPVariable(filename)

  ifndef = ''
  ifndef_linenum = 0
  define = ''
  endif = ''
  endif_linenum = 0
  for linenum, line in enumerate(raw_lines):
    linesplit = line.split()
    if len(linesplit) >= 2:
      # find the first occurrence of #ifndef and #define, save arg
      if not ifndef and linesplit[0] == '#ifndef':
        # set ifndef to the header guard presented on the #ifndef line.
        ifndef = linesplit[1]
        ifndef_linenum = linenum
      if not define and linesplit[0] == '#define':
        define = linesplit[1]
    # find the last occurrence of #endif, save entire line
    if line.startswith('#endif'):
      endif = line
      endif_linenum = linenum

  if not ifndef or not define or ifndef != define:
    error(filename, 0, 'build/header_guard', 5,
          'No #ifndef header guard found, suggested CPP variable is: %s' %
          cppvar)
    return

  # The guard should be PATH_FILE_H_, but we also allow PATH_FILE_H__
  # for backward compatibility.
  if ifndef != cppvar:
    error_level = 0
    if ifndef != cppvar + '_':
      error_level = 5

    ParseNolintSuppressions(filename, raw_lines[ifndef_linenum], ifndef_linenum,
                            error)
    error(filename, ifndef_linenum, 'build/header_guard', error_level,
          '#ifndef header guard has wrong style, please use: %s' % cppvar)

  # Check for "//" comments on endif line.
  ParseNolintSuppressions(filename, raw_lines[endif_linenum], endif_linenum,
                          error)
  match = Match(r'#endif\s*//\s*' + cppvar + r'(_)?\b', endif)
  if match:
    if match.group(1) == '_':
      # Issue low severity warning for deprecated double trailing underscore
      error(filename, endif_linenum, 'build/header_guard', 0,
            '#endif line should be "#endif  // %s"' % cppvar)
    return

  # Didn't find the corresponding "//" comment.  If this file does not
  # contain any "//" comments at all, it could be that the compiler
  # only wants "/**/" comments, look for those instead.
  no_single_line_comments = True
  for i in xrange(1, len(raw_lines) - 1):
    line = raw_lines[i]
    if Match(r'^(?:(?:\'(?:\.|[^\'])*\')|(?:"(?:\.|[^"])*")|[^\'"])*//', line):
      no_single_line_comments = False
      break

  if no_single_line_comments:
    match = Match(r'#endif\s*/\*\s*' + cppvar + r'(_)?\s*\*/', endif)
    if match:
      if match.group(1) == '_':
        # Low severity warning for double trailing underscore
        error(filename, endif_linenum, 'build/header_guard', 0,
              '#endif line should be "#endif  /* %s */"' % cppvar)
      return

  # Didn't find anything
  error(filename, endif_linenum, 'build/header_guard', 5,
        '#endif line should be "#endif  // %s"' % cppvar)