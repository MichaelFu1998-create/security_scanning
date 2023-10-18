def read_header(fd, endian):
    """Read and return the matrix header."""
    flag_class, nzmax = read_elements(fd, endian, ['miUINT32'])
    header = {
        'mclass': flag_class & 0x0FF,
        'is_logical': (flag_class >> 9 & 1) == 1,
        'is_global': (flag_class >> 10 & 1) == 1,
        'is_complex': (flag_class >> 11 & 1) == 1,
        'nzmax': nzmax
    }
    header['dims'] = read_elements(fd, endian, ['miINT32'])
    header['n_dims'] = len(header['dims'])
    if header['n_dims'] != 2:
        raise ParseError('Only matrices with dimension 2 are supported.')
    header['name'] = read_elements(fd, endian, ['miINT8'], is_name=True)
    return header