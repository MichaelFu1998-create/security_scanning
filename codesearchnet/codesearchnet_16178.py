def write_elements(fd, mtp, data, is_name=False):
    """Write data element tag and data.

    The tag contains the array type and the number of
    bytes the array data will occupy when written to file.

    If data occupies 4 bytes or less, it is written immediately
    as a Small Data Element (SDE).
    """
    fmt = etypes[mtp]['fmt']
    if isinstance(data, Sequence):
        if fmt == 's' or is_name:
            if isinstance(data, bytes):
                if is_name and len(data) > 31:
                    raise ValueError(
                        'Name "{}" is too long (max. 31 '
                        'characters allowed)'.format(data))
                fmt = '{}s'.format(len(data))
                data = (data,)
            else:
                fmt = ''.join('{}s'.format(len(s)) for s in data)
        else:
            l = len(data)
            if l == 0:
                # empty array
                fmt = ''
            if l > 1:
                # more than one element to be written
                fmt = '{}{}'.format(l, fmt)
    else:
        data = (data,)
    num_bytes = struct.calcsize(fmt)
    if num_bytes <= 4:
        # write SDE
        if num_bytes < 4:
            # add pad bytes
            fmt += '{}x'.format(4 - num_bytes)
        fd.write(struct.pack('hh' + fmt, etypes[mtp]['n'],
                 *chain([num_bytes], data)))
        return
    # write tag: element type and number of bytes
    fd.write(struct.pack('b3xI', etypes[mtp]['n'], num_bytes))
    # add pad bytes to fmt, if needed
    mod8 = num_bytes % 8
    if mod8:
        fmt += '{}x'.format(8 - mod8)
    # write data
    fd.write(struct.pack(fmt, *data))