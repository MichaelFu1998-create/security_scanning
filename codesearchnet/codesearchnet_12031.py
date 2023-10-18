def hms_str_to_tuple(hms_string):
    '''Converts a string of the form HH:MM:SS or HH MM SS to a tuple of the form
    (HH, MM, SS).

    Parameters
    ----------

    hms_string : str
        A RA coordinate string of the form 'HH:MM:SS.sss' or 'HH MM SS.sss'.

    Returns
    -------

    tuple
        A three element tuple is returned (HH, MM, SS.ssss...)

    '''

    if ':' in hms_string:
        separator = ':'
    else:
        separator = ' '

    hh, mm, ss = hms_string.split(separator)

    return int(hh), int(mm), float(ss)