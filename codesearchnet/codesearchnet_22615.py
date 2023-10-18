def MessageToJson(message, including_default_value_fields=False):
  """Converts protobuf message to JSON format.

  Args:
    message: The protocol buffers message instance to serialize.
    including_default_value_fields: If True, singular primitive fields,
        repeated fields, and map fields will always be serialized.  If
        False, only serialize non-empty fields.  Singular message fields
        and oneof fields are not affected by this option.

  Returns:
    A string containing the JSON formatted protocol buffer message.
  """
  js = _MessageToJsonObject(message, including_default_value_fields)
  return json.dumps(js, indent=2)