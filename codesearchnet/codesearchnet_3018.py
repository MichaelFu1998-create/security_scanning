def _CollapseStrings(elided):
    """Collapses strings and chars on a line to simple "" or '' blocks.

    We nix strings first so we're not fooled by text like '"http://"'

    Args:
      elided: The line being processed.

    Returns:
      The line with collapsed strings.
    """
    if _RE_PATTERN_INCLUDE.match(elided):
      return elided

    # Remove escaped characters first to make quote/single quote collapsing
    # basic.  Things that look like escaped characters shouldn't occur
    # outside of strings and chars.
    elided = _RE_PATTERN_CLEANSE_LINE_ESCAPES.sub('', elided)

    # Replace quoted strings and digit separators.  Both single quotes
    # and double quotes are processed in the same loop, otherwise
    # nested quotes wouldn't work.
    collapsed = ''
    while True:
      # Find the first quote character
      match = Match(r'^([^\'"]*)([\'"])(.*)$', elided)
      if not match:
        collapsed += elided
        break
      head, quote, tail = match.groups()

      if quote == '"':
        # Collapse double quoted strings
        second_quote = tail.find('"')
        if second_quote >= 0:
          collapsed += head + '""'
          elided = tail[second_quote + 1:]
        else:
          # Unmatched double quote, don't bother processing the rest
          # of the line since this is probably a multiline string.
          collapsed += elided
          break
      else:
        # Found single quote, check nearby text to eliminate digit separators.
        #
        # There is no special handling for floating point here, because
        # the integer/fractional/exponent parts would all be parsed
        # correctly as long as there are digits on both sides of the
        # separator.  So we are fine as long as we don't see something
        # like "0.'3" (gcc 4.9.0 will not allow this literal).
        if Search(r'\b(?:0[bBxX]?|[1-9])[0-9a-fA-F]*$', head):
          match_literal = Match(r'^((?:\'?[0-9a-zA-Z_])*)(.*)$', "'" + tail)
          collapsed += head + match_literal.group(1).replace("'", '')
          elided = match_literal.group(2)
        else:
          second_quote = tail.find('\'')
          if second_quote >= 0:
            collapsed += head + "''"
            elided = tail[second_quote + 1:]
          else:
            # Unmatched single quote
            collapsed += elided
            break

    return collapsed