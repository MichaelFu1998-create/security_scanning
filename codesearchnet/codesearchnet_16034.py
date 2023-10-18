def generate_simple_call(opcode: int, index: int):
    """
    Generates a simple call, with an index for something.

    :param opcode: The opcode to generate.
    :param index: The index to use as an argument.
    :return:
    """
    bs = b""
    # add the opcode
    bs += opcode.to_bytes(1, byteorder="little")
    # Add the index
    if isinstance(index, int):
        if PY36:
            bs += index.to_bytes(1, byteorder="little")
        else:
            bs += index.to_bytes(2, byteorder="little")
    else:
        bs += index
    return bs