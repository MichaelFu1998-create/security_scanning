def _MessageToJsonObject(message, including_default_value_fields):
  """Converts message to an object according to Proto3 JSON Specification."""
  message_descriptor = message.DESCRIPTOR
  full_name = message_descriptor.full_name
  if _IsWrapperMessage(message_descriptor):
    return _WrapperMessageToJsonObject(message)
  if full_name in _WKTJSONMETHODS:
    return _WKTJSONMETHODS[full_name][0](
        message, including_default_value_fields)
  js = {}
  return _RegularMessageToJsonObject(
      message, js, including_default_value_fields)