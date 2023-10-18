def CheckForNonConstReference(filename, clean_lines, linenum,
                              nesting_state, error):
  """Check for non-const references.

  Separate from CheckLanguage since it scans backwards from current
  line, instead of scanning forward.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    nesting_state: A NestingState instance which maintains information about
                   the current stack of nested blocks being parsed.
    error: The function to call with any errors found.
  """
  # Do nothing if there is no '&' on current line.
  line = clean_lines.elided[linenum]
  if '&' not in line:
    return

  # If a function is inherited, current function doesn't have much of
  # a choice, so any non-const references should not be blamed on
  # derived function.
  if IsDerivedFunction(clean_lines, linenum):
    return

  # Don't warn on out-of-line method definitions, as we would warn on the
  # in-line declaration, if it isn't marked with 'override'.
  if IsOutOfLineMethodDefinition(clean_lines, linenum):
    return

  # Long type names may be broken across multiple lines, usually in one
  # of these forms:
  #   LongType
  #       ::LongTypeContinued &identifier
  #   LongType::
  #       LongTypeContinued &identifier
  #   LongType<
  #       ...>::LongTypeContinued &identifier
  #
  # If we detected a type split across two lines, join the previous
  # line to current line so that we can match const references
  # accordingly.
  #
  # Note that this only scans back one line, since scanning back
  # arbitrary number of lines would be expensive.  If you have a type
  # that spans more than 2 lines, please use a typedef.
  if linenum > 1:
    previous = None
    if Match(r'\s*::(?:[\w<>]|::)+\s*&\s*\S', line):
      # previous_line\n + ::current_line
      previous = Search(r'\b((?:const\s*)?(?:[\w<>]|::)+[\w<>])\s*$',
                        clean_lines.elided[linenum - 1])
    elif Match(r'\s*[a-zA-Z_]([\w<>]|::)+\s*&\s*\S', line):
      # previous_line::\n + current_line
      previous = Search(r'\b((?:const\s*)?(?:[\w<>]|::)+::)\s*$',
                        clean_lines.elided[linenum - 1])
    if previous:
      line = previous.group(1) + line.lstrip()
    else:
      # Check for templated parameter that is split across multiple lines
      endpos = line.rfind('>')
      if endpos > -1:
        (_, startline, startpos) = ReverseCloseExpression(
            clean_lines, linenum, endpos)
        if startpos > -1 and startline < linenum:
          # Found the matching < on an earlier line, collect all
          # pieces up to current line.
          line = ''
          for i in xrange(startline, linenum + 1):
            line += clean_lines.elided[i].strip()

  # Check for non-const references in function parameters.  A single '&' may
  # found in the following places:
  #   inside expression: binary & for bitwise AND
  #   inside expression: unary & for taking the address of something
  #   inside declarators: reference parameter
  # We will exclude the first two cases by checking that we are not inside a
  # function body, including one that was just introduced by a trailing '{'.
  # TODO(unknown): Doesn't account for 'catch(Exception& e)' [rare].
  if (nesting_state.previous_stack_top and
      not (isinstance(nesting_state.previous_stack_top, _ClassInfo) or
           isinstance(nesting_state.previous_stack_top, _NamespaceInfo))):
    # Not at toplevel, not within a class, and not within a namespace
    return

  # Avoid initializer lists.  We only need to scan back from the
  # current line for something that starts with ':'.
  #
  # We don't need to check the current line, since the '&' would
  # appear inside the second set of parentheses on the current line as
  # opposed to the first set.
  if linenum > 0:
    for i in xrange(linenum - 1, max(0, linenum - 10), -1):
      previous_line = clean_lines.elided[i]
      if not Search(r'[),]\s*$', previous_line):
        break
      if Match(r'^\s*:\s+\S', previous_line):
        return

  # Avoid preprocessors
  if Search(r'\\\s*$', line):
    return

  # Avoid constructor initializer lists
  if IsInitializerList(clean_lines, linenum):
    return

  # We allow non-const references in a few standard places, like functions
  # called "swap()" or iostream operators like "<<" or ">>".  Do not check
  # those function parameters.
  #
  # We also accept & in static_assert, which looks like a function but
  # it's actually a declaration expression.
  whitelisted_functions = (r'(?:[sS]wap(?:<\w:+>)?|'
                           r'operator\s*[<>][<>]|'
                           r'static_assert|COMPILE_ASSERT'
                           r')\s*\(')
  if Search(whitelisted_functions, line):
    return
  elif not Search(r'\S+\([^)]*$', line):
    # Don't see a whitelisted function on this line.  Actually we
    # didn't see any function name on this line, so this is likely a
    # multi-line parameter list.  Try a bit harder to catch this case.
    for i in xrange(2):
      if (linenum > i and
          Search(whitelisted_functions, clean_lines.elided[linenum - i - 1])):
        return

  decls = ReplaceAll(r'{[^}]*}', ' ', line)  # exclude function body
  for parameter in re.findall(_RE_PATTERN_REF_PARAM, decls):
    if (not Match(_RE_PATTERN_CONST_REF_PARAM, parameter) and
        not Match(_RE_PATTERN_REF_STREAM_PARAM, parameter)):
      error(filename, linenum, 'runtime/references', 2,
            'Is this a non-const reference? '
            'If so, make const or use a pointer: ' +
            ReplaceAll(' *<', '<', parameter))