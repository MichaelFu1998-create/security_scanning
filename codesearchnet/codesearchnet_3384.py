def SInt(value, width):
    """
    Convert a bitstring `value` of `width` bits to a signed integer
    representation.

    :param value: The value to convert.
    :type value: int or long or BitVec
    :param int width: The width of the bitstring to consider
    :return: The converted value
    :rtype int or long or BitVec
    """
    return Operators.ITEBV(width, Bit(value, width - 1) == 1,
                           GetNBits(value, width) - 2**width,
                           GetNBits(value, width))