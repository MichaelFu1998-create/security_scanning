def GetNBits(value, nbits):
    """
    Get the first `nbits` from `value`.

    :param value: Source value from which to extract
    :type value: int or long or BitVec
    :param int nbits: How many bits to extract
    :return: Low `nbits` bits of `value`.
    :rtype int or long or BitVec
    """
    # NOP if sizes are the same
    if isinstance(value, int):
        return Operators.EXTRACT(value, 0, nbits)
    elif isinstance(value, BitVec):
        if value.size < nbits:
            return Operators.ZEXTEND(value, nbits)
        else:
            return Operators.EXTRACT(value, 0, nbits)