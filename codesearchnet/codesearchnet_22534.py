def GetMessages(self, files):
    """Gets all the messages from a specified file.

    This will find and resolve dependencies, failing if they are not registered
    in the symbol database.


    Args:
      files: The file names to extract messages from.

    Returns:
      A dictionary mapping proto names to the message classes. This will include
      any dependent messages as well as any messages defined in the same file as
      a specified message.

    Raises:
      KeyError: if a file could not be found.
    """

    result = {}
    for f in files:
      result.update(self._symbols_by_file[f])
    return result