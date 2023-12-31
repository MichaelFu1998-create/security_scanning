def generate_bytecode_from_obb(obb: object, previous: bytes) -> bytes:
    """
    Generates a bytecode from an object.

    :param obb: The object to generate.
    :param previous: The previous bytecode to use when generating subobjects.
    :return: The generated bytecode.
    """
    # Generates bytecode from a specified object, be it a validator or an int or bytes even.
    if isinstance(obb, pyte.superclasses._PyteOp):
        return obb.to_bytes(previous)
    elif isinstance(obb, (pyte.superclasses._PyteAugmentedComparator,
                          pyte.superclasses._PyteAugmentedValidator._FakeMathematicalOP)):
        return obb.to_bytes(previous)
    elif isinstance(obb, pyte.superclasses._PyteAugmentedValidator):
        obb.validate()
        return obb.to_load()
    elif isinstance(obb, int):
        return obb.to_bytes((obb.bit_length() + 7) // 8, byteorder="little") or b''
    elif isinstance(obb, bytes):
        return obb
    else:
        raise TypeError("`{}` was not a valid bytecode-encodable item".format(obb))