def read_elements(fd, endian, mtps, is_name=False):
    """Read elements from the file.

    If list of possible matrix data types mtps is provided, the data type
    of the elements are verified.
    """
    mtpn, num_bytes, data = read_element_tag(fd, endian)
    if mtps and mtpn not in [etypes[mtp]['n'] for mtp in mtps]:
        raise ParseError('Got type {}, expected {}'.format(
            mtpn, ' / '.join('{} ({})'.format(
                etypes[mtp]['n'], mtp) for mtp in mtps)))
    if not data:
        # full format, read data
        data = fd.read(num_bytes)
        # Seek to next 64-bit boundary
        mod8 = num_bytes % 8
        if mod8:
            fd.seek(8 - mod8, 1)

    # parse data and return values
    if is_name:
        # names are stored as miINT8 bytes
        fmt = 's'
        val = [unpack(endian, fmt, s)
               for s in data.split(b'\0') if s]
        if len(val) == 0:
            val = ''
        elif len(val) == 1:
            val = asstr(val[0])
        else:
            val = [asstr(s) for s in val]
    else:
        fmt = etypes[inv_etypes[mtpn]]['fmt']
        val = unpack(endian, fmt, data)
    return val