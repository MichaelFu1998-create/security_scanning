def generate_enum_doc(enum_descriptor, locations, path, name_prefix=''):
    """Generate doc for an enum.

    Args:
        enum_descriptor: descriptor_pb2.EnumDescriptorProto instance for enum
            to generate docs for.
        locations: Dictionary of location paths tuples to
            descriptor_pb2.SourceCodeInfo.Location instances.
        path: Path tuple to the enum definition.
        name_prefix: Optional prefix for this enum's name.
    """
    print(make_subsection(name_prefix + enum_descriptor.name))
    location = locations[path]
    if location.HasField('leading_comments'):
        print(textwrap.dedent(location.leading_comments))

    row_tuples = []
    for value_index, value in enumerate(enum_descriptor.value):
        field_location = locations[path + (2, value_index)]
        row_tuples.append((
            make_code(value.name),
            value.number,
            textwrap.fill(get_comment_from_location(field_location), INFINITY),
        ))
    print_table(('Name', 'Number', 'Description'), row_tuples)