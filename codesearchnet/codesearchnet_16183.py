def write_var_array(fd, array, name=''):
    """Write variable array (of any supported type)"""
    header, array = guess_header(array, name)
    mc = header['mclass']
    if mc in numeric_class_etypes:
        return write_numeric_array(fd, header, array)
    elif mc == 'mxCHAR_CLASS':
        return write_char_array(fd, header, array)
    elif mc == 'mxCELL_CLASS':
        return write_cell_array(fd, header, array)
    elif mc == 'mxSTRUCT_CLASS':
        return write_struct_array(fd, header, array)
    else:
        raise ValueError('Unknown mclass {}'.format(mc))