def read_translation(filename):
    """Returns protobuf mapcontainer. Read from translation file."""
    translation = triple_pb.Translation()
    with open(filename, "rb") as f:
        translation.ParseFromString(f.read())

    def unwrap_translation_units(units):
        for u in units: yield u.element, u.index

    return (list(unwrap_translation_units(translation.entities)),
        list(unwrap_translation_units(translation.relations)))