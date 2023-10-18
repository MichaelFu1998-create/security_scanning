def MakeDescriptor(desc_proto, package='', build_file_if_cpp=True,
                   syntax=None):
  """Make a protobuf Descriptor given a DescriptorProto protobuf.

  Handles nested descriptors. Note that this is limited to the scope of defining
  a message inside of another message. Composite fields can currently only be
  resolved if the message is defined in the same scope as the field.

  Args:
    desc_proto: The descriptor_pb2.DescriptorProto protobuf message.
    package: Optional package name for the new message Descriptor (string).
    build_file_if_cpp: Update the C++ descriptor pool if api matches.
                       Set to False on recursion, so no duplicates are created.
    syntax: The syntax/semantics that should be used.  Set to "proto3" to get
            proto3 field presence semantics.
  Returns:
    A Descriptor for protobuf messages.
  """
  if api_implementation.Type() == 'cpp' and build_file_if_cpp:
    # The C++ implementation requires all descriptors to be backed by the same
    # definition in the C++ descriptor pool. To do this, we build a
    # FileDescriptorProto with the same definition as this descriptor and build
    # it into the pool.
    from typy.google.protobuf import descriptor_pb2
    file_descriptor_proto = descriptor_pb2.FileDescriptorProto()
    file_descriptor_proto.message_type.add().MergeFrom(desc_proto)

    # Generate a random name for this proto file to prevent conflicts with any
    # imported ones. We need to specify a file name so the descriptor pool
    # accepts our FileDescriptorProto, but it is not important what that file
    # name is actually set to.
    proto_name = str(uuid.uuid4())

    if package:
      file_descriptor_proto.name = os.path.join(package.replace('.', '/'),
                                                proto_name + '.proto')
      file_descriptor_proto.package = package
    else:
      file_descriptor_proto.name = proto_name + '.proto'

    _message.default_pool.Add(file_descriptor_proto)
    result = _message.default_pool.FindFileByName(file_descriptor_proto.name)

    if _USE_C_DESCRIPTORS:
      return result.message_types_by_name[desc_proto.name]

  full_message_name = [desc_proto.name]
  if package: full_message_name.insert(0, package)

  # Create Descriptors for enum types
  enum_types = {}
  for enum_proto in desc_proto.enum_type:
    full_name = '.'.join(full_message_name + [enum_proto.name])
    enum_desc = EnumDescriptor(
      enum_proto.name, full_name, None, [
          EnumValueDescriptor(enum_val.name, ii, enum_val.number)
          for ii, enum_val in enumerate(enum_proto.value)])
    enum_types[full_name] = enum_desc

  # Create Descriptors for nested types
  nested_types = {}
  for nested_proto in desc_proto.nested_type:
    full_name = '.'.join(full_message_name + [nested_proto.name])
    # Nested types are just those defined inside of the message, not all types
    # used by fields in the message, so no loops are possible here.
    nested_desc = MakeDescriptor(nested_proto,
                                 package='.'.join(full_message_name),
                                 build_file_if_cpp=False,
                                 syntax=syntax)
    nested_types[full_name] = nested_desc

  fields = []
  for field_proto in desc_proto.field:
    full_name = '.'.join(full_message_name + [field_proto.name])
    enum_desc = None
    nested_desc = None
    if field_proto.HasField('type_name'):
      type_name = field_proto.type_name
      full_type_name = '.'.join(full_message_name +
                                [type_name[type_name.rfind('.')+1:]])
      if full_type_name in nested_types:
        nested_desc = nested_types[full_type_name]
      elif full_type_name in enum_types:
        enum_desc = enum_types[full_type_name]
      # Else type_name references a non-local type, which isn't implemented
    field = FieldDescriptor(
        field_proto.name, full_name, field_proto.number - 1,
        field_proto.number, field_proto.type,
        FieldDescriptor.ProtoTypeToCppProtoType(field_proto.type),
        field_proto.label, None, nested_desc, enum_desc, None, False, None,
        options=field_proto.options, has_default_value=False)
    fields.append(field)

  desc_name = '.'.join(full_message_name)
  return Descriptor(desc_proto.name, desc_name, None, None, fields,
                    list(nested_types.values()), list(enum_types.values()), [],
                    options=desc_proto.options)