def ensure_instruction(instruction: int) -> bytes:
    """
    Wraps an instruction to be Python 3.6+ compatible. This does nothing on Python 3.5 and below.

    This is most useful for operating on bare, single-width instructions such as
    ``RETURN_FUNCTION`` in a version portable way.

    :param instruction: The instruction integer to use.
    :return: A safe bytes object, if applicable.
    """
    if PY36:
        return instruction.to_bytes(2, byteorder="little")
    else:
        return instruction.to_bytes(1, byteorder="little")