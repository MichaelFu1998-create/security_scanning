def _ConvertListValueMessage(value, message):
  """Convert a JSON representation into ListValue message."""
  if not isinstance(value, list):
    raise ParseError(
        'ListValue must be in [] which is {0}.'.format(value))
  message.ClearField('values')
  for item in value:
    _ConvertValueMessage(item, message.values.add())