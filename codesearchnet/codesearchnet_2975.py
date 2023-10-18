def CheckCheck(filename, clean_lines, linenum, error):
  """Checks the use of CHECK and EXPECT macros.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """

  # Decide the set of replacement macros that should be suggested
  lines = clean_lines.elided
  (check_macro, start_pos) = FindCheckMacro(lines[linenum])
  if not check_macro:
    return

  # Find end of the boolean expression by matching parentheses
  (last_line, end_line, end_pos) = CloseExpression(
      clean_lines, linenum, start_pos)
  if end_pos < 0:
    return

  # If the check macro is followed by something other than a
  # semicolon, assume users will log their own custom error messages
  # and don't suggest any replacements.
  if not Match(r'\s*;', last_line[end_pos:]):
    return

  if linenum == end_line:
    expression = lines[linenum][start_pos + 1:end_pos - 1]
  else:
    expression = lines[linenum][start_pos + 1:]
    for i in xrange(linenum + 1, end_line):
      expression += lines[i]
    expression += last_line[0:end_pos - 1]

  # Parse expression so that we can take parentheses into account.
  # This avoids false positives for inputs like "CHECK((a < 4) == b)",
  # which is not replaceable by CHECK_LE.
  lhs = ''
  rhs = ''
  operator = None
  while expression:
    matched = Match(r'^\s*(<<|<<=|>>|>>=|->\*|->|&&|\|\||'
                    r'==|!=|>=|>|<=|<|\()(.*)$', expression)
    if matched:
      token = matched.group(1)
      if token == '(':
        # Parenthesized operand
        expression = matched.group(2)
        (end, _) = FindEndOfExpressionInLine(expression, 0, ['('])
        if end < 0:
          return  # Unmatched parenthesis
        lhs += '(' + expression[0:end]
        expression = expression[end:]
      elif token in ('&&', '||'):
        # Logical and/or operators.  This means the expression
        # contains more than one term, for example:
        #   CHECK(42 < a && a < b);
        #
        # These are not replaceable with CHECK_LE, so bail out early.
        return
      elif token in ('<<', '<<=', '>>', '>>=', '->*', '->'):
        # Non-relational operator
        lhs += token
        expression = matched.group(2)
      else:
        # Relational operator
        operator = token
        rhs = matched.group(2)
        break
    else:
      # Unparenthesized operand.  Instead of appending to lhs one character
      # at a time, we do another regular expression match to consume several
      # characters at once if possible.  Trivial benchmark shows that this
      # is more efficient when the operands are longer than a single
      # character, which is generally the case.
      matched = Match(r'^([^-=!<>()&|]+)(.*)$', expression)
      if not matched:
        matched = Match(r'^(\s*\S)(.*)$', expression)
        if not matched:
          break
      lhs += matched.group(1)
      expression = matched.group(2)

  # Only apply checks if we got all parts of the boolean expression
  if not (lhs and operator and rhs):
    return

  # Check that rhs do not contain logical operators.  We already know
  # that lhs is fine since the loop above parses out && and ||.
  if rhs.find('&&') > -1 or rhs.find('||') > -1:
    return

  # At least one of the operands must be a constant literal.  This is
  # to avoid suggesting replacements for unprintable things like
  # CHECK(variable != iterator)
  #
  # The following pattern matches decimal, hex integers, strings, and
  # characters (in that order).
  lhs = lhs.strip()
  rhs = rhs.strip()
  match_constant = r'^([-+]?(\d+|0[xX][0-9a-fA-F]+)[lLuU]{0,3}|".*"|\'.*\')$'
  if Match(match_constant, lhs) or Match(match_constant, rhs):
    # Note: since we know both lhs and rhs, we can provide a more
    # descriptive error message like:
    #   Consider using CHECK_EQ(x, 42) instead of CHECK(x == 42)
    # Instead of:
    #   Consider using CHECK_EQ instead of CHECK(a == b)
    #
    # We are still keeping the less descriptive message because if lhs
    # or rhs gets long, the error message might become unreadable.
    error(filename, linenum, 'readability/check', 2,
          'Consider using %s instead of %s(a %s b)' % (
              _CHECK_REPLACEMENT[check_macro][operator],
              check_macro, operator))