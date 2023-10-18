def readFromFile(cls, f, packed=True):
    """
    Read serialized object from file.

    :param f: input file
    :param packed: If true, will assume content is packed
    :return: first-class instance initialized from proto obj
    """
    # Get capnproto schema from instance
    schema = cls.getSchema()

    # Read from file
    if packed:
      proto = schema.read_packed(f)
    else:
      proto = schema.read(f)

    # Return first-class instance initialized from proto obj
    return cls.read(proto)