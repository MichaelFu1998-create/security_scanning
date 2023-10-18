def FindEndOfExpressionInLine(line, startpos, stack):
  """Find the position just after the end of current parenthesized expression.

  Args:
    line: a CleansedLines line.
    startpos: start searching at this position.
    stack: nesting stack at startpos.

  Returns:
    On finding matching end: (index just after matching end, None)
    On finding an unclosed expression: (-1, None)
    Otherwise: (-1, new stack at end of this line)
  """
  for i in xrange(startpos, len(line)):
    char = line[i]
    if char in '([{':
      # Found start of parenthesized expression, push to expression stack
      stack.append(char)
    elif char == '<':
      # Found potential start of template argument list
      if i > 0 and line[i - 1] == '<':
        # Left shift operator
        if stack and stack[-1] == '<':
          stack.pop()
          if not stack:
            return (-1, None)
      elif i > 0 and Search(r'\boperator\s*$', line[0:i]):
        # operator<, don't add to stack
        continue
      else:
        # Tentative start of template argument list
        stack.append('<')
    elif char in ')]}':
      # Found end of parenthesized expression.
      #
      # If we are currently expecting a matching '>', the pending '<'
      # must have been an operator.  Remove them from expression stack.
      while stack and stack[-1] == '<':
        stack.pop()
      if not stack:
        return (-1, None)
      if ((stack[-1] == '(' and char == ')') or
          (stack[-1] == '[' and char == ']') or
          (stack[-1] == '{' and char == '}')):
        stack.pop()
        if not stack:
          return (i + 1, None)
      else:
        # Mismatched parentheses
        return (-1, None)
    elif char == '>':
      # Found potential end of template argument list.

      # Ignore "->" and operator functions
      if (i > 0 and
          (line[i - 1] == '-' or Search(r'\boperator\s*$', line[0:i - 1]))):
        continue

      # Pop the stack if there is a matching '<'.  Otherwise, ignore
      # this '>' since it must be an operator.
      if stack:
        if stack[-1] == '<':
          stack.pop()
          if not stack:
            return (i + 1, None)
    elif char == ';':
      # Found something that look like end of statements.  If we are currently
      # expecting a '>', the matching '<' must have been an operator, since
      # template argument list should not contain statements.
      while stack and stack[-1] == '<':
        stack.pop()
      if not stack:
        return (-1, None)

  # Did not find end of expression or unbalanced parentheses on this line
  return (-1, stack)