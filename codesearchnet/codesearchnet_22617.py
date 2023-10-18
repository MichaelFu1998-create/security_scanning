def _StructMessageToJsonObject(message, unused_including_default=False):
  """Converts Struct message according to Proto3 JSON Specification."""
  fields = message.fields
  ret = {}
  for key in fields:
    ret[key] = _ValueMessageToJsonObject(fields[key])
  return ret