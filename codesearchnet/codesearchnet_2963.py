def CheckAccess(filename, clean_lines, linenum, nesting_state, error):
  """Checks for improper use of DISALLOW* macros.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    nesting_state: A NestingState instance which maintains information about
                   the current stack of nested blocks being parsed.
    error: The function to call with any errors found.
  """
  line = clean_lines.elided[linenum]  # get rid of comments and strings

  matched = Match((r'\s*(DISALLOW_COPY_AND_ASSIGN|'
                   r'DISALLOW_IMPLICIT_CONSTRUCTORS)'), line)
  if not matched:
    return
  if nesting_state.stack and isinstance(nesting_state.stack[-1], _ClassInfo):
    if nesting_state.stack[-1].access != 'private':
      error(filename, linenum, 'readability/constructors', 3,
            '%s must be in the private: section' % matched.group(1))

  else:
    # Found DISALLOW* macro outside a class declaration, or perhaps it
    # was used inside a function when it should have been part of the
    # class declaration.  We could issue a warning here, but it
    # probably resulted in a compiler error already.
    pass