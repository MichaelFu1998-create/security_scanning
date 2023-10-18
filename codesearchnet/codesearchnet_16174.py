def read_struct_array(fd, endian, header):
    """Read a struct array.
    Returns a dict with fields of the struct array.
    """
    # read field name length (unused, as strings are null terminated)
    field_name_length = read_elements(fd, endian, ['miINT32'])
    if field_name_length > 32:
        raise ParseError('Unexpected field name length: {}'.format(
                         field_name_length))

    # read field names
    fields = read_elements(fd, endian, ['miINT8'], is_name=True)
    if isinstance(fields, basestring):
        fields = [fields]

    # read rows and columns of each field
    empty = lambda: [list() for i in range(header['dims'][0])]
    array = {}
    for row in range(header['dims'][0]):
        for col in range(header['dims'][1]):
            for field in fields:
                # read the matrix header and array
                vheader, next_pos, fd_var = read_var_header(fd, endian)
                data = read_var_array(fd_var, endian, vheader)
                if field not in array:
                    array[field] = empty()
                array[field][row].append(data)
                # move on to next field
                fd.seek(next_pos)
    # pack the nested arrays
    for field in fields:
        rows = array[field]
        for i in range(header['dims'][0]):
            rows[i] = squeeze(rows[i])
        array[field] = squeeze(array[field])
    return array