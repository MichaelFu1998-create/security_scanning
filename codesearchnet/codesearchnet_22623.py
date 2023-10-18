def _ConvertStructMessage(value, message):
  """Convert a JSON representation into Struct message."""
  if not isinstance(value, dict):
    raise ParseError(
        'Struct must be in a dict which is {0}.'.format(value))
  for key in value:
    _ConvertValueMessage(value[key], message.fields[key])
  return