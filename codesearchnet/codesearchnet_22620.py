def _ConvertMessage(value, message):
  """Convert a JSON object into a message.

  Args:
    value: A JSON object.
    message: A WKT or regular protocol message to record the data.

  Raises:
    ParseError: In case of convert problems.
  """
  message_descriptor = message.DESCRIPTOR
  full_name = message_descriptor.full_name
  if _IsWrapperMessage(message_descriptor):
    _ConvertWrapperMessage(value, message)
  elif full_name in _WKTJSONMETHODS:
    _WKTJSONMETHODS[full_name][1](value, message)
  else:
    _ConvertFieldValuePair(value, message)