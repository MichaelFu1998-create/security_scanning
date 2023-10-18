def FindExtensionByName(self, full_name):
    """Loads the named extension descriptor from the pool.

    Args:
      full_name: The full name of the extension descriptor to load.

    Returns:
      A FieldDescriptor, describing the named extension.
    """
    full_name = _NormalizeFullyQualifiedName(full_name)
    message_name, _, extension_name = full_name.rpartition('.')
    try:
      # Most extensions are nested inside a message.
      scope = self.FindMessageTypeByName(message_name)
    except KeyError:
      # Some extensions are defined at file scope.
      scope = self.FindFileContainingSymbol(full_name)
    return scope.extensions_by_name[extension_name]