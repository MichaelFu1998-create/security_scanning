def dms_to_decimal(sign, degrees, minutes, seconds):
    '''Converts from DD:MM:SS to a decimal value.

    Parameters
    ----------

    sign : {'+', '-', ''}
        The sign part of a Dec coordinate.

    degrees : int
        The DD part of a Dec coordinate.

    minutes : int
        The MM part of a Dec coordinate.

    seconds : float
        The SS.sss part of a Dec coordinate.

    Returns
    -------

    float
        The declination value in decimal degrees.

    '''

    dec_deg = fabs(degrees) + fabs(minutes)/60.0 + fabs(seconds)/3600.0

    if sign == '-':
        return -dec_deg
    else:
        return dec_deg