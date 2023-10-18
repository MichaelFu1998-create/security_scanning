def Merge(text, message, allow_unknown_extension=False,
          allow_field_number=False):
  """Parses an text representation of a protocol message into a message.

  Like Parse(), but allows repeated values for a non-repeated field, and uses
  the last one.

  Args:
    text: Message text representation.
    message: A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.

  Returns:
    The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
  return MergeLines(text.split('\n'), message, allow_unknown_extension,
                    allow_field_number)