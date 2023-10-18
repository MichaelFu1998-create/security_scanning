def get_variable_name(self, name):
    """Produce a default variable name if none is specified."""
    if not name:
      name = '%s%s' % (self._auto_prefix, self._auto_index)
      self._auto_index += 1
    return name