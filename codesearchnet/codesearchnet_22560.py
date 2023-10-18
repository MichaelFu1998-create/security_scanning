def FindMessageTypeByName(self, full_name):
    """Loads the named descriptor from the pool.

    Args:
      full_name: The full name of the descriptor to load.

    Returns:
      The descriptor for the named type.
    """

    full_name = _NormalizeFullyQualifiedName(full_name)
    if full_name not in self._descriptors:
      self.FindFileContainingSymbol(full_name)
    return self._descriptors[full_name]