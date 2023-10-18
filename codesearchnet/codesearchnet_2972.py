def CheckTrailingSemicolon(filename, clean_lines, linenum, error):
  """Looks for redundant trailing semicolon.

  Args:
    filename: The name of the current file.
    clean_lines: A CleansedLines instance containing the file.
    linenum: The number of the line to check.
    error: The function to call with any errors found.
  """

  line = clean_lines.elided[linenum]

  # Block bodies should not be followed by a semicolon.  Due to C++11
  # brace initialization, there are more places where semicolons are
  # required than not, so we use a whitelist approach to check these
  # rather than a blacklist.  These are the places where "};" should
  # be replaced by just "}":
  # 1. Some flavor of block following closing parenthesis:
  #    for (;;) {};
  #    while (...) {};
  #    switch (...) {};
  #    Function(...) {};
  #    if (...) {};
  #    if (...) else if (...) {};
  #
  # 2. else block:
  #    if (...) else {};
  #
  # 3. const member function:
  #    Function(...) const {};
  #
  # 4. Block following some statement:
  #    x = 42;
  #    {};
  #
  # 5. Block at the beginning of a function:
  #    Function(...) {
  #      {};
  #    }
  #
  #    Note that naively checking for the preceding "{" will also match
  #    braces inside multi-dimensional arrays, but this is fine since
  #    that expression will not contain semicolons.
  #
  # 6. Block following another block:
  #    while (true) {}
  #    {};
  #
  # 7. End of namespaces:
  #    namespace {};
  #
  #    These semicolons seems far more common than other kinds of
  #    redundant semicolons, possibly due to people converting classes
  #    to namespaces.  For now we do not warn for this case.
  #
  # Try matching case 1 first.
  match = Match(r'^(.*\)\s*)\{', line)
  if match:
    # Matched closing parenthesis (case 1).  Check the token before the
    # matching opening parenthesis, and don't warn if it looks like a
    # macro.  This avoids these false positives:
    #  - macro that defines a base class
    #  - multi-line macro that defines a base class
    #  - macro that defines the whole class-head
    #
    # But we still issue warnings for macros that we know are safe to
    # warn, specifically:
    #  - TEST, TEST_F, TEST_P, MATCHER, MATCHER_P
    #  - TYPED_TEST
    #  - INTERFACE_DEF
    #  - EXCLUSIVE_LOCKS_REQUIRED, SHARED_LOCKS_REQUIRED, LOCKS_EXCLUDED:
    #
    # We implement a whitelist of safe macros instead of a blacklist of
    # unsafe macros, even though the latter appears less frequently in
    # google code and would have been easier to implement.  This is because
    # the downside for getting the whitelist wrong means some extra
    # semicolons, while the downside for getting the blacklist wrong
    # would result in compile errors.
    #
    # In addition to macros, we also don't want to warn on
    #  - Compound literals
    #  - Lambdas
    #  - alignas specifier with anonymous structs
    #  - decltype
    closing_brace_pos = match.group(1).rfind(')')
    opening_parenthesis = ReverseCloseExpression(
        clean_lines, linenum, closing_brace_pos)
    if opening_parenthesis[2] > -1:
      line_prefix = opening_parenthesis[0][0:opening_parenthesis[2]]
      macro = Search(r'\b([A-Z_][A-Z0-9_]*)\s*$', line_prefix)
      func = Match(r'^(.*\])\s*$', line_prefix)
      if ((macro and
           macro.group(1) not in (
               'TEST', 'TEST_F', 'MATCHER', 'MATCHER_P', 'TYPED_TEST',
               'EXCLUSIVE_LOCKS_REQUIRED', 'SHARED_LOCKS_REQUIRED',
               'LOCKS_EXCLUDED', 'INTERFACE_DEF')) or
          (func and not Search(r'\boperator\s*\[\s*\]', func.group(1))) or
          Search(r'\b(?:struct|union)\s+alignas\s*$', line_prefix) or
          Search(r'\bdecltype$', line_prefix) or
          Search(r'\s+=\s*$', line_prefix)):
        match = None
    if (match and
        opening_parenthesis[1] > 1 and
        Search(r'\]\s*$', clean_lines.elided[opening_parenthesis[1] - 1])):
      # Multi-line lambda-expression
      match = None

  else:
    # Try matching cases 2-3.
    match = Match(r'^(.*(?:else|\)\s*const)\s*)\{', line)
    if not match:
      # Try matching cases 4-6.  These are always matched on separate lines.
      #
      # Note that we can't simply concatenate the previous line to the
      # current line and do a single match, otherwise we may output
      # duplicate warnings for the blank line case:
      #   if (cond) {
      #     // blank line
      #   }
      prevline = GetPreviousNonBlankLine(clean_lines, linenum)[0]
      if prevline and Search(r'[;{}]\s*$', prevline):
        match = Match(r'^(\s*)\{', line)

  # Check matching closing brace
  if match:
    (endline, endlinenum, endpos) = CloseExpression(
        clean_lines, linenum, len(match.group(1)))
    if endpos > -1 and Match(r'^\s*;', endline[endpos:]):
      # Current {} pair is eligible for semicolon check, and we have found
      # the redundant semicolon, output warning here.
      #
      # Note: because we are scanning forward for opening braces, and
      # outputting warnings for the matching closing brace, if there are
      # nested blocks with trailing semicolons, we will get the error
      # messages in reversed order.

      # We need to check the line forward for NOLINT
      raw_lines = clean_lines.raw_lines
      ParseNolintSuppressions(filename, raw_lines[endlinenum-1], endlinenum-1,
                              error)
      ParseNolintSuppressions(filename, raw_lines[endlinenum], endlinenum,
                              error)

      error(filename, endlinenum, 'readability/braces', 4,
            "You don't need a ; after a }")