def dump_raw_data(filename, data):
    """ Write the data into a raw format file. Big endian is always used.

    Parameters
    ----------
    filename: str
        Path to the output file

    data: numpy.ndarray
        n-dimensional image data array.
    """
    if data.ndim == 3:
        # Begin 3D fix
        data = data.reshape([data.shape[0], data.shape[1]*data.shape[2]])
        # End 3D fix

    a = array.array('f')
    for o in data:
        a.fromlist(list(o.flatten()))

    # if is_little_endian():
    #     a.byteswap()

    with open(filename, 'wb') as rawf:
        a.tofile(rawf)