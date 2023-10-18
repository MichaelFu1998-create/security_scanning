def FindEnumTypeByName(self, full_name):
    """Loads the named enum descriptor from the pool.

    Args:
      full_name: The full name of the enum descriptor to load.

    Returns:
      The enum descriptor for the named type.
    """

    full_name = _NormalizeFullyQualifiedName(full_name)
    if full_name not in self._enum_descriptors:
      self.FindFileContainingSymbol(full_name)
    return self._enum_descriptors[full_name]