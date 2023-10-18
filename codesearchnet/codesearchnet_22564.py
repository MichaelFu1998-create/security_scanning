def _MakeFieldDescriptor(self, field_proto, message_name, index,
                           is_extension=False):
    """Creates a field descriptor from a FieldDescriptorProto.

    For message and enum type fields, this method will do a look up
    in the pool for the appropriate descriptor for that type. If it
    is unavailable, it will fall back to the _source function to
    create it. If this type is still unavailable, construction will
    fail.

    Args:
      field_proto: The proto describing the field.
      message_name: The name of the containing message.
      index: Index of the field
      is_extension: Indication that this field is for an extension.

    Returns:
      An initialized FieldDescriptor object
    """

    if message_name:
      full_name = '.'.join((message_name, field_proto.name))
    else:
      full_name = field_proto.name

    return descriptor.FieldDescriptor(
        name=field_proto.name,
        full_name=full_name,
        index=index,
        number=field_proto.number,
        type=field_proto.type,
        cpp_type=None,
        message_type=None,
        enum_type=None,
        containing_type=None,
        label=field_proto.label,
        has_default_value=False,
        default_value=None,
        is_extension=is_extension,
        extension_scope=None,
        options=field_proto.options)