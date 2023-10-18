def CheckSpacing(filename, clean_lines, linenum, nesting_state, error):
  """Checks for the correctness of various spacing issues in the code.

  Things we check for: spaces around operators, spaces after
  if/for/while/switch, no spaces around parens in function calls, two
  spaces between code and comment, don't start a block with a blank
  line, don't end a function with a blank line, don't add a blank line
  after public/protected/private, don't have too many blank lines in a row.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    nesting_state: A NestingState instance which maintains information about
                   the current stack of nested blocks being parsed.
    error: The function to call with any errors found.
  """

  # Don't use "elided" lines here, otherwise we can't check commented lines.
  # Don't want to use "raw" either, because we don't want to check inside C++11
  # raw strings,
  raw = clean_lines.lines_without_raw_strings
  line = raw[linenum]

  # Before nixing comments, check if the line is blank for no good
  # reason.  This includes the first line after a block is opened, and
  # blank lines at the end of a function (ie, right before a line like '}'
  #
  # Skip all the blank line checks if we are immediately inside a
  # namespace body.  In other words, don't issue blank line warnings
  # for this block:
  #   namespace {
  #
  #   }
  #
  # A warning about missing end of namespace comments will be issued instead.
  #
  # Also skip blank line checks for 'extern "C"' blocks, which are formatted
  # like namespaces.
  if (IsBlankLine(line) and
      not nesting_state.InNamespaceBody() and
      not nesting_state.InExternC()):
    elided = clean_lines.elided
    prev_line = elided[linenum - 1]
    prevbrace = prev_line.rfind('{')
    # TODO(unknown): Don't complain if line before blank line, and line after,
    #                both start with alnums and are indented the same amount.
    #                This ignores whitespace at the start of a namespace block
    #                because those are not usually indented.
    if prevbrace != -1 and prev_line[prevbrace:].find('}') == -1:
      # OK, we have a blank line at the start of a code block.  Before we
      # complain, we check if it is an exception to the rule: The previous
      # non-empty line has the parameters of a function header that are indented
      # 4 spaces (because they did not fit in a 80 column line when placed on
      # the same line as the function name).  We also check for the case where
      # the previous line is indented 6 spaces, which may happen when the
      # initializers of a constructor do not fit into a 80 column line.
      exception = False
      if Match(r' {6}\w', prev_line):  # Initializer list?
        # We are looking for the opening column of initializer list, which
        # should be indented 4 spaces to cause 6 space indentation afterwards.
        search_position = linenum-2
        while (search_position >= 0
               and Match(r' {6}\w', elided[search_position])):
          search_position -= 1
        exception = (search_position >= 0
                     and elided[search_position][:5] == '    :')
      else:
        # Search for the function arguments or an initializer list.  We use a
        # simple heuristic here: If the line is indented 4 spaces; and we have a
        # closing paren, without the opening paren, followed by an opening brace
        # or colon (for initializer lists) we assume that it is the last line of
        # a function header.  If we have a colon indented 4 spaces, it is an
        # initializer list.
        exception = (Match(r' {4}\w[^\(]*\)\s*(const\s*)?(\{\s*$|:)',
                           prev_line)
                     or Match(r' {4}:', prev_line))

      if not exception:
        error(filename, linenum, 'whitespace/blank_line', 2,
              'Redundant blank line at the start of a code block '
              'should be deleted.')
    # Ignore blank lines at the end of a block in a long if-else
    # chain, like this:
    #   if (condition1) {
    #     // Something followed by a blank line
    #
    #   } else if (condition2) {
    #     // Something else
    #   }
    if linenum + 1 < clean_lines.NumLines():
      next_line = raw[linenum + 1]
      if (next_line
          and Match(r'\s*}', next_line)
          and next_line.find('} else ') == -1):
        error(filename, linenum, 'whitespace/blank_line', 3,
              'Redundant blank line at the end of a code block '
              'should be deleted.')

    matched = Match(r'\s*(public|protected|private):', prev_line)
    if matched:
      error(filename, linenum, 'whitespace/blank_line', 3,
            'Do not leave a blank line after "%s:"' % matched.group(1))

  # Next, check comments
  next_line_start = 0
  if linenum + 1 < clean_lines.NumLines():
    next_line = raw[linenum + 1]
    next_line_start = len(next_line) - len(next_line.lstrip())
  CheckComment(line, filename, linenum, next_line_start, error)

  # get rid of comments and strings
  line = clean_lines.elided[linenum]

  # You shouldn't have spaces before your brackets, except maybe after
  # 'delete []' or 'return []() {};'
  if Search(r'\w\s+\[', line) and not Search(r'(?:delete|return)\s+\[', line):
    error(filename, linenum, 'whitespace/braces', 5,
          'Extra space before [')

  # In range-based for, we wanted spaces before and after the colon, but
  # not around "::" tokens that might appear.
  if (Search(r'for *\(.*[^:]:[^: ]', line) or
      Search(r'for *\(.*[^: ]:[^:]', line)):
    error(filename, linenum, 'whitespace/forcolon', 2,
          'Missing space around colon in range-based for loop')