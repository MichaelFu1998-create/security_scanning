def _IsType(clean_lines, nesting_state, expr):
  """Check if expression looks like a type name, returns true if so.

  Args:
    clean_lines: A CleansedLines instance containing the file.
    nesting_state: A NestingState instance which maintains information about
                   the current stack of nested blocks being parsed.
    expr: The expression to check.
  Returns:
    True, if token looks like a type.
  """
  # Keep only the last token in the expression
  last_word = Match(r'^.*(\b\S+)$', expr)
  if last_word:
    token = last_word.group(1)
  else:
    token = expr

  # Match native types and stdint types
  if _TYPES.match(token):
    return True

  # Try a bit harder to match templated types.  Walk up the nesting
  # stack until we find something that resembles a typename
  # declaration for what we are looking for.
  typename_pattern = (r'\b(?:typename|class|struct)\s+' + re.escape(token) +
                      r'\b')
  block_index = len(nesting_state.stack) - 1
  while block_index >= 0:
    if isinstance(nesting_state.stack[block_index], _NamespaceInfo):
      return False

    # Found where the opening brace is.  We want to scan from this
    # line up to the beginning of the function, minus a few lines.
    #   template <typename Type1,  // stop scanning here
    #             ...>
    #   class C
    #     : public ... {  // start scanning here
    last_line = nesting_state.stack[block_index].starting_linenum

    next_block_start = 0
    if block_index > 0:
      next_block_start = nesting_state.stack[block_index - 1].starting_linenum
    first_line = last_line
    while first_line >= next_block_start:
      if clean_lines.elided[first_line].find('template') >= 0:
        break
      first_line -= 1
    if first_line < next_block_start:
      # Didn't find any "template" keyword before reaching the next block,
      # there are probably no template things to check for this block
      block_index -= 1
      continue

    # Look for typename in the specified range
    for i in xrange(first_line, last_line + 1, 1):
      if Search(typename_pattern, clean_lines.elided[i]):
        return True
    block_index -= 1

  return False