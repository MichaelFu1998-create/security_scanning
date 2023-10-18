def read_var_array(fd, endian, header):
    """Read variable array (of any supported type)."""
    mc = inv_mclasses[header['mclass']]

    if mc in numeric_class_etypes:
        return read_numeric_array(
            fd, endian, header,
            set(compressed_numeric).union([numeric_class_etypes[mc]])
        )
    elif mc == 'mxSPARSE_CLASS':
        raise ParseError('Sparse matrices not supported')
    elif mc == 'mxCHAR_CLASS':
        return read_char_array(fd, endian, header)
    elif mc == 'mxCELL_CLASS':
        return read_cell_array(fd, endian, header)
    elif mc == 'mxSTRUCT_CLASS':
        return read_struct_array(fd, endian, header)
    elif mc == 'mxOBJECT_CLASS':
        raise ParseError('Object classes not supported')
    elif mc == 'mxFUNCTION_CLASS':
        raise ParseError('Function classes not supported')
    elif mc == 'mxOPAQUE_CLASS':
        raise ParseError('Anonymous function classes not supported')