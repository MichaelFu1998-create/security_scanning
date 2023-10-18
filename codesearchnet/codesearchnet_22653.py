def ParseLines(lines, message, allow_unknown_extension=False,
               allow_field_number=False):
  """Parses an text representation of a protocol message into a message.

  Args:
    lines: An iterable of lines of a message's text representation.
    message: A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.

  Returns:
    The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
  parser = _Parser(allow_unknown_extension, allow_field_number)
  return parser.ParseLines(lines, message)