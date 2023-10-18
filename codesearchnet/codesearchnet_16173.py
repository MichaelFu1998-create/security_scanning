def read_cell_array(fd, endian, header):
    """Read a cell array.
    Returns an array with rows of the cell array.
    """
    array = [list() for i in range(header['dims'][0])]
    for row in range(header['dims'][0]):
        for col in range(header['dims'][1]):
            # read the matrix header and array
            vheader, next_pos, fd_var = read_var_header(fd, endian)
            varray = read_var_array(fd_var, endian, vheader)
            array[row].append(varray)
            # move on to next field
            fd.seek(next_pos)
    # pack and return the array
    if header['dims'][0] == 1:
        return squeeze(array[0])
    return squeeze(array)