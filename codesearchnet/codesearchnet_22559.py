def FindFileContainingSymbol(self, symbol):
    """Gets the FileDescriptor for the file containing the specified symbol.

    Args:
      symbol: The name of the symbol to search for.

    Returns:
      A FileDescriptor that contains the specified symbol.

    Raises:
      KeyError: if the file can not be found in the pool.
    """

    symbol = _NormalizeFullyQualifiedName(symbol)
    try:
      return self._descriptors[symbol].file
    except KeyError:
      pass

    try:
      return self._enum_descriptors[symbol].file
    except KeyError:
      pass

    try:
      file_proto = self._internal_db.FindFileContainingSymbol(symbol)
    except KeyError as error:
      if self._descriptor_db:
        file_proto = self._descriptor_db.FindFileContainingSymbol(symbol)
      else:
        raise error
    if not file_proto:
      raise KeyError('Cannot find a file containing %s' % symbol)
    return self._ConvertFileProtoToFileDescriptor(file_proto)