def savemat(filename, data):
    """Save data to MAT-file:

    savemat(filename, data)

    The filename argument is either a string with the filename, or
    a file like object.

    The parameter ``data`` shall be a dict with the variables.

    A ``ValueError`` exception is raised if data has invalid format, or if the
    data structure cannot be mapped to a known MAT array type.
    """

    if not isinstance(data, Mapping):
        raise ValueError('Data should be a dict of variable arrays')

    if isinstance(filename, basestring):
        fd = open(filename, 'wb')
    else:
        fd = filename

    write_file_header(fd)

    # write variables
    for name, array in data.items():
        write_compressed_var_array(fd, array, name)

    fd.close()