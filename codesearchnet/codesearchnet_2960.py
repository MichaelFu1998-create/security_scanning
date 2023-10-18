def CheckSpacingForFunctionCall(filename, clean_lines, linenum, error):
  """Checks for the correctness of various spacing around function calls.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """
  line = clean_lines.elided[linenum]

  # Since function calls often occur inside if/for/while/switch
  # expressions - which have their own, more liberal conventions - we
  # first see if we should be looking inside such an expression for a
  # function call, to which we can apply more strict standards.
  fncall = line    # if there's no control flow construct, look at whole line
  for pattern in (r'\bif\s*\((.*)\)\s*{',
                  r'\bfor\s*\((.*)\)\s*{',
                  r'\bwhile\s*\((.*)\)\s*[{;]',
                  r'\bswitch\s*\((.*)\)\s*{'):
    match = Search(pattern, line)
    if match:
      fncall = match.group(1)    # look inside the parens for function calls
      break

  # Except in if/for/while/switch, there should never be space
  # immediately inside parens (eg "f( 3, 4 )").  We make an exception
  # for nested parens ( (a+b) + c ).  Likewise, there should never be
  # a space before a ( when it's a function argument.  I assume it's a
  # function argument when the char before the whitespace is legal in
  # a function name (alnum + _) and we're not starting a macro. Also ignore
  # pointers and references to arrays and functions coz they're too tricky:
  # we use a very simple way to recognize these:
  # " (something)(maybe-something)" or
  # " (something)(maybe-something," or
  # " (something)[something]"
  # Note that we assume the contents of [] to be short enough that
  # they'll never need to wrap.
  if (  # Ignore control structures.
      not Search(r'\b(if|for|while|switch|return|new|delete|catch|sizeof)\b',
                 fncall) and
      # Ignore pointers/references to functions.
      not Search(r' \([^)]+\)\([^)]*(\)|,$)', fncall) and
      # Ignore pointers/references to arrays.
      not Search(r' \([^)]+\)\[[^\]]+\]', fncall)):
    if Search(r'\w\s*\(\s(?!\s*\\$)', fncall):      # a ( used for a fn call
      error(filename, linenum, 'whitespace/parens', 4,
            'Extra space after ( in function call')
    elif Search(r'\(\s+(?!(\s*\\)|\()', fncall):
      error(filename, linenum, 'whitespace/parens', 2,
            'Extra space after (')
    if (Search(r'\w\s+\(', fncall) and
        not Search(r'_{0,2}asm_{0,2}\s+_{0,2}volatile_{0,2}\s+\(', fncall) and
        not Search(r'#\s*define|typedef|using\s+\w+\s*=', fncall) and
        not Search(r'\w\s+\((\w+::)*\*\w+\)\(', fncall) and
        not Search(r'\bcase\s+\(', fncall)):
      # TODO(unknown): Space after an operator function seem to be a common
      # error, silence those for now by restricting them to highest verbosity.
      if Search(r'\boperator_*\b', line):
        error(filename, linenum, 'whitespace/parens', 0,
              'Extra space before ( in function call')
      else:
        error(filename, linenum, 'whitespace/parens', 4,
              'Extra space before ( in function call')
    # If the ) is followed only by a newline or a { + newline, assume it's
    # part of a control statement (if/while/etc), and don't complain
    if Search(r'[^)]\s+\)\s*[^{\s]', fncall):
      # If the closing parenthesis is preceded by only whitespaces,
      # try to give a more descriptive error message.
      if Search(r'^\s+\)', fncall):
        error(filename, linenum, 'whitespace/parens', 2,
              'Closing ) should be moved to the previous line')
      else:
        error(filename, linenum, 'whitespace/parens', 2,
              'Extra space before )')