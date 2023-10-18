def unpack(endian, fmt, data):
    """Unpack a byte string to the given format. If the byte string
    contains more bytes than required for the given format, the function
    returns a tuple of values.
    """
    if fmt == 's':
        # read data as an array of chars
        val = struct.unpack(''.join([endian, str(len(data)), 's']),
                            data)[0]
    else:
        # read a number of values
        num = len(data) // struct.calcsize(fmt)
        val = struct.unpack(''.join([endian, str(num), fmt]), data)
        if len(val) == 1:
            val = val[0]
    return val