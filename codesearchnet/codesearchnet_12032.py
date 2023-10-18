def dms_str_to_tuple(dms_string):
    '''Converts a string of the form [+-]DD:MM:SS or [+-]DD MM SS to a tuple of
    the form (sign, DD, MM, SS).

    Parameters
    ----------

    dms_string : str
        A declination coordinate string of the form '[+-]DD:MM:SS.sss' or
        '[+-]DD MM SS.sss'. The sign in front of DD is optional. If it's not
        there, this function will assume that the coordinate string is a
        positive value.

    Returns
    -------

    tuple
        A four element tuple of the form: (sign, DD, MM, SS.ssss...).

    '''
    if ':' in dms_string:
        separator = ':'
    else:
        separator = ' '

    sign_dd, mm, ss = dms_string.split(separator)
    if sign_dd.startswith('+') or sign_dd.startswith('-'):
        sign, dd = sign_dd[0], sign_dd[1:]
    else:
        sign, dd = '+', sign_dd

    return sign, int(dd), int(mm), float(ss)