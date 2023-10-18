def CheckComment(line, filename, linenum, next_line_start, error):
  """Checks for common mistakes in comments.

  Args:
    line: The line in question.
    filename: The name of the current file.
    linenum: The number of the line to check.
    next_line_start: The first non-whitespace column of the next line.
    error: The function to call with any errors found.
  """
  commentpos = line.find('//')
  if commentpos != -1:
    # Check if the // may be in quotes.  If so, ignore it
    if re.sub(r'\\.', '', line[0:commentpos]).count('"') % 2 == 0:
      # Allow one space for new scopes, two spaces otherwise:
      if (not (Match(r'^.*{ *//', line) and next_line_start == commentpos) and
          ((commentpos >= 1 and
            line[commentpos-1] not in string.whitespace) or
           (commentpos >= 2 and
            line[commentpos-2] not in string.whitespace))):
        error(filename, linenum, 'whitespace/comments', 2,
              'At least two spaces is best between code and comments')

      # Checks for common mistakes in TODO comments.
      comment = line[commentpos:]
      match = _RE_PATTERN_TODO.match(comment)
      if match:
        # One whitespace is correct; zero whitespace is handled elsewhere.
        leading_whitespace = match.group(1)
        if len(leading_whitespace) > 1:
          error(filename, linenum, 'whitespace/todo', 2,
                'Too many spaces before TODO')

        username = match.group(2)
        if not username:
          error(filename, linenum, 'readability/todo', 2,
                'Missing username in TODO; it should look like '
                '"// TODO(my_username): Stuff."')

        middle_whitespace = match.group(3)
        # Comparisons made explicit for correctness -- pylint: disable=g-explicit-bool-comparison
        if middle_whitespace != ' ' and middle_whitespace != '':
          error(filename, linenum, 'whitespace/todo', 2,
                'TODO(my_username) should be followed by a space')

      # If the comment contains an alphanumeric character, there
      # should be a space somewhere between it and the // unless
      # it's a /// or //! Doxygen comment.
      if (Match(r'//[^ ]*\w', comment) and
          not Match(r'(///|//\!)(\s+|$)', comment)):
        error(filename, linenum, 'whitespace/comments', 4,
              'Should have a space between // and comment')