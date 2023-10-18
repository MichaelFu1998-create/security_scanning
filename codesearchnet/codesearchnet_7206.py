def generate_message_doc(message_descriptor, locations, path, name_prefix=''):
    """Generate docs for message and nested messages and enums.

    Args:
        message_descriptor: descriptor_pb2.DescriptorProto instance for message
            to generate docs for.
        locations: Dictionary of location paths tuples to
            descriptor_pb2.SourceCodeInfo.Location instances.
        path: Path tuple to the message definition.
        name_prefix: Optional prefix for this message's name.
    """
    # message_type is 4
    prefixed_name = name_prefix + message_descriptor.name
    print(make_subsection(prefixed_name))
    location = locations[path]
    if location.HasField('leading_comments'):
        print(textwrap.dedent(location.leading_comments))

    row_tuples = []
    for field_index, field in enumerate(message_descriptor.field):
        field_location = locations[path + (2, field_index)]
        if field.type not in [11, 14]:
            type_str = TYPE_TO_STR[field.type]
        else:
            type_str = make_link(field.type_name.lstrip('.'))
        row_tuples.append((
            make_code(field.name),
            field.number,
            type_str,
            LABEL_TO_STR[field.label],
            textwrap.fill(get_comment_from_location(field_location), INFINITY),
        ))
    print_table(('Field', 'Number', 'Type', 'Label', 'Description'),
                row_tuples)

    # Generate nested messages
    nested_types = enumerate(message_descriptor.nested_type)
    for index, nested_message_desc in nested_types:
        generate_message_doc(nested_message_desc, locations,
                             path + (3, index),
                             name_prefix=prefixed_name + '.')

    # Generate nested enums
    for index, nested_enum_desc in enumerate(message_descriptor.enum_type):
        generate_enum_doc(nested_enum_desc, locations, path + (4, index),
                          name_prefix=prefixed_name + '.')