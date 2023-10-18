def read_var_header(fd, endian):
    """Read full header tag.

    Return a dict with the parsed header, the file position of next tag,
    a file like object for reading the uncompressed element data.
    """
    mtpn, num_bytes = unpack(endian, 'II', fd.read(8))
    next_pos = fd.tell() + num_bytes

    if mtpn == etypes['miCOMPRESSED']['n']:
        # read compressed data
        data = fd.read(num_bytes)
        dcor = zlib.decompressobj()
        # from here, read of the decompressed data
        fd_var = BytesIO(dcor.decompress(data))
        del data
        fd = fd_var
        # Check the stream is not so broken as to leave cruft behind
        if dcor.flush() != b'':
            raise ParseError('Error in compressed data.')
        # read full tag from the uncompressed data
        mtpn, num_bytes = unpack(endian, 'II', fd.read(8))

    if mtpn != etypes['miMATRIX']['n']:
        raise ParseError('Expecting miMATRIX type number {}, '
                         'got {}'.format(etypes['miMATRIX']['n'], mtpn))
    # read the header
    header = read_header(fd, endian)
    return header, next_pos, fd