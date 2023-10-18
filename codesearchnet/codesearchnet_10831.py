def to_bin(data, width):
    """
    Convert an unsigned integer to a numpy binary array with the first
    element the MSB and the last element the LSB.
    """
    data_str = bin(data & (2**width-1))[2:].zfill(width)
    return [int(x) for x in tuple(data_str)]