def _indentLines(str, indentLevels = 1, indentFirstLine=True):
  """ Indent all lines in the given string

  str:          input string
  indentLevels: number of levels of indentation to apply
  indentFirstLine: if False, the 1st line will not be indented

  Returns:      The result string with all lines indented
  """

  indent = _ONE_INDENT * indentLevels

  lines = str.splitlines(True)
  result = ''

  if len(lines) > 0 and not indentFirstLine:
    first = 1
    result += lines[0]
  else:
    first = 0

  for line in lines[first:]:
    result += indent + line

  return result