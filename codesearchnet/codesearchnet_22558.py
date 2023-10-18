def AddEnumDescriptor(self, enum_desc):
    """Adds an EnumDescriptor to the pool.

    This method also registers the FileDescriptor associated with the message.

    Args:
      enum_desc: An EnumDescriptor.
    """

    if not isinstance(enum_desc, descriptor.EnumDescriptor):
      raise TypeError('Expected instance of descriptor.EnumDescriptor.')

    self._enum_descriptors[enum_desc.full_name] = enum_desc
    self.AddFileDescriptor(enum_desc.file)