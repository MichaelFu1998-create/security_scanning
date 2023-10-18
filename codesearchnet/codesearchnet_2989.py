def CheckCasts(filename, clean_lines, linenum, error):
  """Various cast related checks.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  line = clean_lines.elided[linenum]

  # Check to see if they're using an conversion function cast.
  # I just try to capture the most common basic types, though there are more.
  # Parameterless conversion functions, such as bool(), are allowed as they are
  # probably a member operator declaration or default constructor.
  match = Search(
      r'(\bnew\s+(?:const\s+)?|\S<\s*(?:const\s+)?)?\b'
      r'(int|float|double|bool|char|int32|uint32|int64|uint64)'
      r'(\([^)].*)', line)
  expecting_function = ExpectingFunctionArgs(clean_lines, linenum)
  if match and not expecting_function:
    matched_type = match.group(2)

    # matched_new_or_template is used to silence two false positives:
    # - New operators
    # - Template arguments with function types
    #
    # For template arguments, we match on types immediately following
    # an opening bracket without any spaces.  This is a fast way to
    # silence the common case where the function type is the first
    # template argument.  False negative with less-than comparison is
    # avoided because those operators are usually followed by a space.
    #
    #   function<double(double)>   // bracket + no space = false positive
    #   value < double(42)         // bracket + space = true positive
    matched_new_or_template = match.group(1)

    # Avoid arrays by looking for brackets that come after the closing
    # parenthesis.
    if Match(r'\([^()]+\)\s*\[', match.group(3)):
      return

    # Other things to ignore:
    # - Function pointers
    # - Casts to pointer types
    # - Placement new
    # - Alias declarations
    matched_funcptr = match.group(3)
    if (matched_new_or_template is None and
        not (matched_funcptr and
             (Match(r'\((?:[^() ]+::\s*\*\s*)?[^() ]+\)\s*\(',
                    matched_funcptr) or
              matched_funcptr.startswith('(*)'))) and
        not Match(r'\s*using\s+\S+\s*=\s*' + matched_type, line) and
        not Search(r'new\(\S+\)\s*' + matched_type, line)):
      error(filename, linenum, 'readability/casting', 4,
            'Using deprecated casting style.  '
            'Use static_cast<%s>(...) instead' %
            matched_type)

  if not expecting_function:
    CheckCStyleCast(filename, clean_lines, linenum, 'static_cast',
                    r'\((int|float|double|bool|char|u?int(16|32|64))\)', error)

  # This doesn't catch all cases. Consider (const char * const)"hello".
  #
  # (char *) "foo" should always be a const_cast (reinterpret_cast won't
  # compile).
  if CheckCStyleCast(filename, clean_lines, linenum, 'const_cast',
                     r'\((char\s?\*+\s?)\)\s*"', error):
    pass
  else:
    # Check pointer casts for other than string constants
    CheckCStyleCast(filename, clean_lines, linenum, 'reinterpret_cast',
                    r'\((\w+\s?\*+\s?)\)', error)

  # In addition, we look for people taking the address of a cast.  This
  # is dangerous -- casts can assign to temporaries, so the pointer doesn't
  # point where you think.
  #
  # Some non-identifier character is required before the '&' for the
  # expression to be recognized as a cast.  These are casts:
  #   expression = &static_cast<int*>(temporary());
  #   function(&(int*)(temporary()));
  #
  # This is not a cast:
  #   reference_type&(int* function_param);
  match = Search(
      r'(?:[^\w]&\(([^)*][^)]*)\)[\w(])|'
      r'(?:[^\w]&(static|dynamic|down|reinterpret)_cast\b)', line)
  if match:
    # Try a better error message when the & is bound to something
    # dereferenced by the casted pointer, as opposed to the casted
    # pointer itself.
    parenthesis_error = False
    match = Match(r'^(.*&(?:static|dynamic|down|reinterpret)_cast\b)<', line)
    if match:
      _, y1, x1 = CloseExpression(clean_lines, linenum, len(match.group(1)))
      if x1 >= 0 and clean_lines.elided[y1][x1] == '(':
        _, y2, x2 = CloseExpression(clean_lines, y1, x1)
        if x2 >= 0:
          extended_line = clean_lines.elided[y2][x2:]
          if y2 < clean_lines.NumLines() - 1:
            extended_line += clean_lines.elided[y2 + 1]
          if Match(r'\s*(?:->|\[)', extended_line):
            parenthesis_error = True

    if parenthesis_error:
      error(filename, linenum, 'readability/casting', 4,
            ('Are you taking an address of something dereferenced '
             'from a cast?  Wrapping the dereferenced expression in '
             'parentheses will make the binding more obvious'))
    else:
      error(filename, linenum, 'runtime/casting', 4,
            ('Are you taking an address of a cast?  '
             'This is dangerous: could be a temp var.  '
             'Take the address before doing the cast, rather than after'))