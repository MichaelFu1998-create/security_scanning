def read_numeric_array(fd, endian, header, data_etypes):
    """Read a numeric matrix.
    Returns an array with rows of the numeric matrix.
    """
    if header['is_complex']:
        raise ParseError('Complex arrays are not supported')
    # read array data (stored as column-major)
    data = read_elements(fd, endian, data_etypes)
    if not isinstance(data, Sequence):
        # not an array, just a value
        return data
    # transform column major data continous array to
    # a row major array of nested lists
    rowcount = header['dims'][0]
    colcount = header['dims'][1]
    array = [list(data[c * rowcount + r] for c in range(colcount))
             for r in range(rowcount)]
    # pack and return the array
    return squeeze(array)