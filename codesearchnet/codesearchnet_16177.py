def loadmat(filename, meta=False):
    """Load data from MAT-file:

    data = loadmat(filename, meta=False)

    The filename argument is either a string with the filename, or
    a file like object.

    The returned parameter ``data`` is a dict with the variables found
    in the MAT file.

    Call ``loadmat`` with parameter meta=True to include meta data, such
    as file header information and list of globals.

    A ``ParseError`` exception is raised if the MAT-file is corrupt or
    contains a data type that cannot be parsed.
    """

    if isinstance(filename, basestring):
        fd = open(filename, 'rb')
    else:
        fd = filename

    # Check mat file format is version 5
    # For 5 format we need to read an integer in the header.
    # Bytes 124 through 128 contain a version integer and an
    # endian test string
    fd.seek(124)
    tst_str = fd.read(4)
    little_endian = (tst_str[2:4] == b'IM')
    endian = ''
    if (sys.byteorder == 'little' and little_endian) or \
       (sys.byteorder == 'big' and not little_endian):
        # no byte swapping same endian
        pass
    elif sys.byteorder == 'little':
        # byte swapping
        endian = '>'
    else:
        # byte swapping
        endian = '<'
    maj_ind = int(little_endian)
    # major version number
    maj_val = ord(tst_str[maj_ind]) if ispy2 else tst_str[maj_ind]
    if maj_val != 1:
        raise ParseError('Can only read from Matlab level 5 MAT-files')
    # the minor version number (unused value)
    # min_val = ord(tst_str[1 - maj_ind]) if ispy2 else tst_str[1 - maj_ind]

    mdict = {}
    if meta:
        # read the file header
        fd.seek(0)
        mdict['__header__'] = read_file_header(fd, endian)
        mdict['__globals__'] = []

    # read data elements
    while not eof(fd):
        hdr, next_position, fd_var = read_var_header(fd, endian)
        name = hdr['name']
        if name in mdict:
            raise ParseError('Duplicate variable name "{}" in mat file.'
                             .format(name))

        # read the matrix
        mdict[name] = read_var_array(fd_var, endian, hdr)
        if meta and hdr['is_global']:
            mdict['__globals__'].append(name)

        # move on to next entry in file
        fd.seek(next_position)

    fd.close()
    return mdict