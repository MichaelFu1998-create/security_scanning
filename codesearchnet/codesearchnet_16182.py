def write_numeric_array(fd, header, array):
    """Write the numeric array"""
    # make a memory file for writing array data
    bd = BytesIO()

    # write matrix header to memory file
    write_var_header(bd, header)

    if not isinstance(array, basestring) and header['dims'][0] > 1:
        # list array data in column major order
        array = list(chain.from_iterable(izip(*array)))

    # write matrix data to memory file
    write_elements(bd, header['mtp'], array)

    # write the variable to disk file
    data = bd.getvalue()
    bd.close()
    write_var_data(fd, data)