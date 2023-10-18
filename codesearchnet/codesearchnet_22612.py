def GetTopLevelContainingType(self):
    """Returns the root if this is a nested type, or itself if its the root."""
    desc = self
    while desc.containing_type is not None:
      desc = desc.containing_type
    return desc