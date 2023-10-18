def CheckEmptyBlockBody(filename, clean_lines, linenum, error):
  """Look for empty loop/conditional body with only a single semicolon.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """

  # Search for loop keywords at the beginning of the line.  Because only
  # whitespaces are allowed before the keywords, this will also ignore most
  # do-while-loops, since those lines should start with closing brace.
  #
  # We also check "if" blocks here, since an empty conditional block
  # is likely an error.
  line = clean_lines.elided[linenum]
  matched = Match(r'\s*(for|while|if)\s*\(', line)
  if matched:
    # Find the end of the conditional expression.
    (end_line, end_linenum, end_pos) = CloseExpression(
        clean_lines, linenum, line.find('('))

    # Output warning if what follows the condition expression is a semicolon.
    # No warning for all other cases, including whitespace or newline, since we
    # have a separate check for semicolons preceded by whitespace.
    if end_pos >= 0 and Match(r';', end_line[end_pos:]):
      if matched.group(1) == 'if':
        error(filename, end_linenum, 'whitespace/empty_conditional_body', 5,
              'Empty conditional bodies should use {}')
      else:
        error(filename, end_linenum, 'whitespace/empty_loop_body', 5,
              'Empty loop bodies should use {} or continue')

    # Check for if statements that have completely empty bodies (no comments)
    # and no else clauses.
    if end_pos >= 0 and matched.group(1) == 'if':
      # Find the position of the opening { for the if statement.
      # Return without logging an error if it has no brackets.
      opening_linenum = end_linenum
      opening_line_fragment = end_line[end_pos:]
      # Loop until EOF or find anything that's not whitespace or opening {.
      while not Search(r'^\s*\{', opening_line_fragment):
        if Search(r'^(?!\s*$)', opening_line_fragment):
          # Conditional has no brackets.
          return
        opening_linenum += 1
        if opening_linenum == len(clean_lines.elided):
          # Couldn't find conditional's opening { or any code before EOF.
          return
        opening_line_fragment = clean_lines.elided[opening_linenum]
      # Set opening_line (opening_line_fragment may not be entire opening line).
      opening_line = clean_lines.elided[opening_linenum]

      # Find the position of the closing }.
      opening_pos = opening_line_fragment.find('{')
      if opening_linenum == end_linenum:
        # We need to make opening_pos relative to the start of the entire line.
        opening_pos += end_pos
      (closing_line, closing_linenum, closing_pos) = CloseExpression(
          clean_lines, opening_linenum, opening_pos)
      if closing_pos < 0:
        return

      # Now construct the body of the conditional. This consists of the portion
      # of the opening line after the {, all lines until the closing line,
      # and the portion of the closing line before the }.
      if (clean_lines.raw_lines[opening_linenum] !=
          CleanseComments(clean_lines.raw_lines[opening_linenum])):
        # Opening line ends with a comment, so conditional isn't empty.
        return
      if closing_linenum > opening_linenum:
        # Opening line after the {. Ignore comments here since we checked above.
        bodylist = list(opening_line[opening_pos+1:])
        # All lines until closing line, excluding closing line, with comments.
        bodylist.extend(clean_lines.raw_lines[opening_linenum+1:closing_linenum])
        # Closing line before the }. Won't (and can't) have comments.
        bodylist.append(clean_lines.elided[closing_linenum][:closing_pos-1])
        body = '\n'.join(bodylist)
      else:
        # If statement has brackets and fits on a single line.
        body = opening_line[opening_pos+1:closing_pos-1]

      # Check if the body is empty
      if not _EMPTY_CONDITIONAL_BODY_PATTERN.search(body):
        return
      # The body is empty. Now make sure there's not an else clause.
      current_linenum = closing_linenum
      current_line_fragment = closing_line[closing_pos:]
      # Loop until EOF or find anything that's not whitespace or else clause.
      while Search(r'^\s*$|^(?=\s*else)', current_line_fragment):
        if Search(r'^(?=\s*else)', current_line_fragment):
          # Found an else clause, so don't log an error.
          return
        current_linenum += 1
        if current_linenum == len(clean_lines.elided):
          break
        current_line_fragment = clean_lines.elided[current_linenum]

      # The body is empty and there's no else clause until EOF or other code.
      error(filename, end_linenum, 'whitespace/empty_if_body', 4,
            ('If statement had no body and no else clause'))