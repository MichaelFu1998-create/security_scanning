def _ConvertEnumDescriptor(self, enum_proto, package=None, file_desc=None,
                             containing_type=None, scope=None):
    """Make a protobuf EnumDescriptor given an EnumDescriptorProto protobuf.

    Args:
      enum_proto: The descriptor_pb2.EnumDescriptorProto protobuf message.
      package: Optional package name for the new message EnumDescriptor.
      file_desc: The file containing the enum descriptor.
      containing_type: The type containing this enum.
      scope: Scope containing available types.

    Returns:
      The added descriptor
    """

    if package:
      enum_name = '.'.join((package, enum_proto.name))
    else:
      enum_name = enum_proto.name

    if file_desc is None:
      file_name = None
    else:
      file_name = file_desc.name

    values = [self._MakeEnumValueDescriptor(value, index)
              for index, value in enumerate(enum_proto.value)]
    desc = descriptor.EnumDescriptor(name=enum_proto.name,
                                     full_name=enum_name,
                                     filename=file_name,
                                     file=file_desc,
                                     values=values,
                                     containing_type=containing_type,
                                     options=enum_proto.options)
    scope['.%s' % enum_name] = desc
    self._enum_descriptors[enum_name] = desc
    return desc