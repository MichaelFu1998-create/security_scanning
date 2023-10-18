def CheckBracesSpacing(filename, clean_lines, linenum, nesting_state, error):
  """Checks for horizontal spacing near commas.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    nesting_state: A NestingState instance which maintains information about
                   the current stack of nested blocks being parsed.
    error: The function to call with any errors found.
  """
  line = clean_lines.elided[linenum]

  # Except after an opening paren, or after another opening brace (in case of
  # an initializer list, for instance), you should have spaces before your
  # braces when they are delimiting blocks, classes, namespaces etc.
  # And since you should never have braces at the beginning of a line,
  # this is an easy test.  Except that braces used for initialization don't
  # follow the same rule; we often don't want spaces before those.
  match = Match(r'^(.*[^ ({>]){', line)

  if match:
    # Try a bit harder to check for brace initialization.  This
    # happens in one of the following forms:
    #   Constructor() : initializer_list_{} { ... }
    #   Constructor{}.MemberFunction()
    #   Type variable{};
    #   FunctionCall(type{}, ...);
    #   LastArgument(..., type{});
    #   LOG(INFO) << type{} << " ...";
    #   map_of_type[{...}] = ...;
    #   ternary = expr ? new type{} : nullptr;
    #   OuterTemplate<InnerTemplateConstructor<Type>{}>
    #
    # We check for the character following the closing brace, and
    # silence the warning if it's one of those listed above, i.e.
    # "{.;,)<>]:".
    #
    # To account for nested initializer list, we allow any number of
    # closing braces up to "{;,)<".  We can't simply silence the
    # warning on first sight of closing brace, because that would
    # cause false negatives for things that are not initializer lists.
    #   Silence this:         But not this:
    #     Outer{                if (...) {
    #       Inner{...}            if (...){  // Missing space before {
    #     };                    }
    #
    # There is a false negative with this approach if people inserted
    # spurious semicolons, e.g. "if (cond){};", but we will catch the
    # spurious semicolon with a separate check.
    leading_text = match.group(1)
    (endline, endlinenum, endpos) = CloseExpression(
        clean_lines, linenum, len(match.group(1)))
    trailing_text = ''
    if endpos > -1:
      trailing_text = endline[endpos:]
    for offset in xrange(endlinenum + 1,
                         min(endlinenum + 3, clean_lines.NumLines() - 1)):
      trailing_text += clean_lines.elided[offset]
    # We also suppress warnings for `uint64_t{expression}` etc., as the style
    # guide recommends brace initialization for integral types to avoid
    # overflow/truncation.
    if (not Match(r'^[\s}]*[{.;,)<>\]:]', trailing_text)
        and not _IsType(clean_lines, nesting_state, leading_text)):
      error(filename, linenum, 'whitespace/braces', 5,
            'Missing space before {')

  # Make sure '} else {' has spaces.
  if Search(r'}else', line):
    error(filename, linenum, 'whitespace/braces', 5,
          'Missing space before else')

  # You shouldn't have a space before a semicolon at the end of the line.
  # There's a special case for "for" since the style guide allows space before
  # the semicolon there.
  if Search(r':\s*;\s*$', line):
    error(filename, linenum, 'whitespace/semicolon', 5,
          'Semicolon defining empty statement. Use {} instead.')
  elif Search(r'^\s*;\s*$', line):
    error(filename, linenum, 'whitespace/semicolon', 5,
          'Line contains only semicolon. If this should be an empty statement, '
          'use {} instead.')
  elif (Search(r'\s+;\s*$', line) and
        not Search(r'\bfor\b', line)):
    error(filename, linenum, 'whitespace/semicolon', 5,
          'Extra space before last semicolon. If this should be an empty '
          'statement, use {} instead.')