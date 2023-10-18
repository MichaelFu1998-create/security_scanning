def _ConvertValueMessage(value, message):
  """Convert a JSON representation into Value message."""
  if isinstance(value, dict):
    _ConvertStructMessage(value, message.struct_value)
  elif isinstance(value, list):
    _ConvertListValueMessage(value, message.list_value)
  elif value is None:
    message.null_value = 0
  elif isinstance(value, bool):
    message.bool_value = value
  elif isinstance(value, six.string_types):
    message.string_value = value
  elif isinstance(value, _INT_OR_FLOAT):
    message.number_value = value
  else:
    raise ParseError('Unexpected type for Value message.')