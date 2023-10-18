def read_file_header(fd, endian):
    """Read mat 5 file header of the file fd.
    Returns a dict with header values.
    """
    fields = [
        ('description', 's', 116),
        ('subsystem_offset', 's', 8),
        ('version', 'H', 2),
        ('endian_test', 's', 2)
    ]
    hdict = {}
    for name, fmt, num_bytes in fields:
        data = fd.read(num_bytes)
        hdict[name] = unpack(endian, fmt, data)
    hdict['description'] = hdict['description'].strip()
    v_major = hdict['version'] >> 8
    v_minor = hdict['version'] & 0xFF
    hdict['__version__'] = '%d.%d' % (v_major, v_minor)
    return hdict