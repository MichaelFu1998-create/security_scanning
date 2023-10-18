def read_element_tag(fd, endian):
    """Read data element tag: type and number of bytes.
    If tag is of the Small Data Element (SDE) type the element data
    is also returned.
    """
    data = fd.read(8)
    mtpn = unpack(endian, 'I', data[:4])
    # The most significant two bytes of mtpn will always be 0,
    # if they are not, this must be SDE format
    num_bytes = mtpn >> 16
    if num_bytes > 0:
        # small data element format
        mtpn = mtpn & 0xFFFF
        if num_bytes > 4:
            raise ParseError('Error parsing Small Data Element (SDE) '
                             'formatted data')
        data = data[4:4 + num_bytes]
    else:
        # regular element
        num_bytes = unpack(endian, 'I', data[4:])
        data = None
    return (mtpn, num_bytes, data)