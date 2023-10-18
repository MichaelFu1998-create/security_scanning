def _InternalUnpackAny(msg):
  """Unpacks Any message and returns the unpacked message.

  This internal method is differnt from public Any Unpack method which takes
  the target message as argument. _InternalUnpackAny method does not have
  target message type and need to find the message type in descriptor pool.

  Args:
    msg: An Any message to be unpacked.

  Returns:
    The unpacked message.
  """
  type_url = msg.type_url
  db = symbol_database.Default()

  if not type_url:
    return None

  # TODO(haberman): For now we just strip the hostname.  Better logic will be
  # required.
  type_name = type_url.split("/")[-1]
  descriptor = db.pool.FindMessageTypeByName(type_name)

  if descriptor is None:
    return None

  message_class = db.GetPrototype(descriptor)
  message = message_class()

  message.ParseFromString(msg.value)
  return message