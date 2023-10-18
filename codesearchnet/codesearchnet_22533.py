def RegisterMessage(self, message):
    """Registers the given message type in the local database.

    Args:
      message: a message.Message, to be registered.

    Returns:
      The provided message.
    """

    desc = message.DESCRIPTOR
    self._symbols[desc.full_name] = message
    if desc.file.name not in self._symbols_by_file:
      self._symbols_by_file[desc.file.name] = {}
    self._symbols_by_file[desc.file.name][desc.full_name] = message
    self.pool.AddDescriptor(desc)
    return message