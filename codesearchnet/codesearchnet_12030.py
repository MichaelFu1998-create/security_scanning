def decimal_to_hms(decimal_value):
    '''Converts from decimal degrees (for RA coords) to HH:MM:SS.

    Parameters
    ----------

    decimal_value : float
        A decimal value to convert to hours, minutes, seconds. Negative values
        will be wrapped around 360.0.

    Returns
    -------

    tuple
        A three element tuple is returned: (HH, MM, SS.ssss...)

    '''

    # wrap to 360.0
    if decimal_value < 0:
        dec_wrapped = 360.0 + decimal_value
    else:
        dec_wrapped = decimal_value

    # convert to decimal hours first
    dec_hours = dec_wrapped/15.0

    if dec_hours < 0:
        negative = True
        dec_val = fabs(dec_hours)
    else:
        negative = False
        dec_val = dec_hours

    hours = trunc(dec_val)
    minutes_hrs = dec_val - hours

    minutes_mm = minutes_hrs * 60.0
    minutes_out = trunc(minutes_mm)
    seconds = (minutes_mm - minutes_out)*60.0

    if negative:
        hours = -hours
        return hours, minutes_out, seconds
    else:
        return hours, minutes_out, seconds