def hms_to_decimal(hours, minutes, seconds, returndeg=True):
    '''Converts from HH, MM, SS to a decimal value.

    Parameters
    ----------

    hours : int
        The HH part of a RA coordinate.

    minutes : int
        The MM part of a RA coordinate.

    seconds : float
        The SS.sss part of a RA coordinate.

    returndeg : bool
        If this is True, then will return decimal degrees as the output.
        If this is False, then will return decimal HOURS as the output.
        Decimal hours are sometimes used in FITS headers.

    Returns
    -------

    float
        The right ascension value in either decimal degrees or decimal hours
        depending on `returndeg`.

    '''

    if hours > 24:

        return None

    else:

        dec_hours = fabs(hours) + fabs(minutes)/60.0 + fabs(seconds)/3600.0

        if returndeg:

            dec_deg = dec_hours*15.0

            if dec_deg < 0:
                dec_deg = dec_deg + 360.0
            dec_deg = dec_deg % 360.0
            return dec_deg
        else:
            return dec_hours