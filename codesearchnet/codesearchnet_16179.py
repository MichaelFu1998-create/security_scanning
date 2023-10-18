def write_var_header(fd, header):
    """Write variable header"""

    # write tag bytes,
    # and array flags + class and nzmax (null bytes)
    fd.write(struct.pack('b3xI', etypes['miUINT32']['n'], 8))
    fd.write(struct.pack('b3x4x', mclasses[header['mclass']]))

    # write dimensions array
    write_elements(fd, 'miINT32', header['dims'])

    # write var name
    write_elements(fd, 'miINT8', asbytes(header['name']), is_name=True)