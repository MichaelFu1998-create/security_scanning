def FromJsonString(self, value):
    """Converts string to FieldMask according to proto3 JSON spec."""
    self.Clear()
    for path in value.split(','):
      self.paths.append(path)