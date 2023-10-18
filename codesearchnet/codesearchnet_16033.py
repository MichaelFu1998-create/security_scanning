def pack_value(index: int) -> bytes:
    """
    Small helper value to pack an index value into bytecode.

    This is used for version compat between 3.5- and 3.6+

    :param index: The item to pack.
    :return: The packed item.
    """
    if PY36:
        return index.to_bytes(1, byteorder="little")
    else:
        return index.to_bytes(2, byteorder="little")