def main():
    """Parse arguments and print generated documentation to stdout."""
    parser = argparse.ArgumentParser()
    parser.add_argument('protofilepath')
    args = parser.parse_args()

    out_file = compile_protofile(args.protofilepath)
    with open(out_file, 'rb') as proto_file:
        # pylint: disable=no-member
        file_descriptor_set = descriptor_pb2.FileDescriptorSet.FromString(
            proto_file.read()
        )
        # pylint: enable=no-member

    for file_descriptor in file_descriptor_set.file:
        # Build dict of location tuples
        locations = {}
        for location in file_descriptor.source_code_info.location:
            locations[tuple(location.path)] = location
        # Add comment to top
        print(make_comment('This file was automatically generated from {} and '
                           'should not be edited directly.'
                           .format(args.protofilepath)))
        # Generate documentation
        for index, message_desc in enumerate(file_descriptor.message_type):
            generate_message_doc(message_desc, locations, (4, index))
        for index, enum_desc in enumerate(file_descriptor.enum_type):
            generate_enum_doc(enum_desc, locations, (5, index))