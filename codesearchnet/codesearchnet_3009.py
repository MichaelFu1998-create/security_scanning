def IsInAlphabeticalOrder(self, clean_lines, linenum, header_path):
    """Check if a header is in alphabetical order with the previous header.

    Args:
      clean_lines: A CleansedLines instance containing the file.
      linenum: The number of the line to check.
      header_path: Canonicalized header to be checked.

    Returns:
      Returns true if the header is in alphabetical order.
    """
    # If previous section is different from current section, _last_header will
    # be reset to empty string, so it's always less than current header.
    #
    # If previous line was a blank line, assume that the headers are
    # intentionally sorted the way they are.
    if (self._last_header > header_path and
        Match(r'^\s*#\s*include\b', clean_lines.elided[linenum - 1])):
      return False
    return True