def GetMessages(self, files):
    """Gets all the messages from a specified file.

    This will find and resolve dependencies, failing if the descriptor
    pool cannot satisfy them.

    Args:
      files: The file names to extract messages from.

    Returns:
      A dictionary mapping proto names to the message classes. This will include
      any dependent messages as well as any messages defined in the same file as
      a specified message.
    """
    result = {}
    for file_name in files:
      file_desc = self.pool.FindFileByName(file_name)
      for name, msg in file_desc.message_types_by_name.items():
        if file_desc.package:
          full_name = '.'.join([file_desc.package, name])
        else:
          full_name = msg.name
        result[full_name] = self.GetPrototype(
            self.pool.FindMessageTypeByName(full_name))

      # While the extension FieldDescriptors are created by the descriptor pool,
      # the python classes created in the factory need them to be registered
      # explicitly, which is done below.
      #
      # The call to RegisterExtension will specifically check if the
      # extension was already registered on the object and either
      # ignore the registration if the original was the same, or raise
      # an error if they were different.

      for name, extension in file_desc.extensions_by_name.items():
        if extension.containing_type.full_name not in self._classes:
          self.GetPrototype(extension.containing_type)
        extended_class = self._classes[extension.containing_type.full_name]
        extended_class.RegisterExtension(extension)
    return result