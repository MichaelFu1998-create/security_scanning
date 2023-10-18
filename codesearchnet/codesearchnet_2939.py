def CleanseRawStrings(raw_lines):
  """Removes C++11 raw strings from lines.

    Before:
      static const char kData[] = R"(
          multi-line string
          )";

    After:
      static const char kData[] = ""
          (replaced by blank line)
          "";

  Args:
    raw_lines: list of raw lines.

  Returns:
    list of lines with C++11 raw strings replaced by empty strings.
  """

  delimiter = None
  lines_without_raw_strings = []
  for line in raw_lines:
    if delimiter:
      # Inside a raw string, look for the end
      end = line.find(delimiter)
      if end >= 0:
        # Found the end of the string, match leading space for this
        # line and resume copying the original lines, and also insert
        # a "" on the last line.
        leading_space = Match(r'^(\s*)\S', line)
        line = leading_space.group(1) + '""' + line[end + len(delimiter):]
        delimiter = None
      else:
        # Haven't found the end yet, append a blank line.
        line = '""'

    # Look for beginning of a raw string, and replace them with
    # empty strings.  This is done in a loop to handle multiple raw
    # strings on the same line.
    while delimiter is None:
      # Look for beginning of a raw string.
      # See 2.14.15 [lex.string] for syntax.
      #
      # Once we have matched a raw string, we check the prefix of the
      # line to make sure that the line is not part of a single line
      # comment.  It's done this way because we remove raw strings
      # before removing comments as opposed to removing comments
      # before removing raw strings.  This is because there are some
      # cpplint checks that requires the comments to be preserved, but
      # we don't want to check comments that are inside raw strings.
      matched = Match(r'^(.*?)\b(?:R|u8R|uR|UR|LR)"([^\s\\()]*)\((.*)$', line)
      if (matched and
          not Match(r'^([^\'"]|\'(\\.|[^\'])*\'|"(\\.|[^"])*")*//',
                    matched.group(1))):
        delimiter = ')' + matched.group(2) + '"'

        end = matched.group(3).find(delimiter)
        if end >= 0:
          # Raw string ended on same line
          line = (matched.group(1) + '""' +
                  matched.group(3)[end + len(delimiter):])
          delimiter = None
        else:
          # Start of a multi-line raw string
          line = matched.group(1) + '""'
      else:
        break

    lines_without_raw_strings.append(line)

  # TODO(unknown): if delimiter is not None here, we might want to
  # emit a warning for unterminated string.
  return lines_without_raw_strings