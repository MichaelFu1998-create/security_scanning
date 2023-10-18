def decimal_to_dms(decimal_value):
    '''Converts from decimal degrees (for declination coords) to DD:MM:SS.

    Parameters
    ----------

    decimal_value : float
        A decimal value to convert to degrees, minutes, seconds sexagesimal
        format.

    Returns
    -------

    tuple
        A four element tuple is returned: (sign, HH, MM, SS.ssss...)

    '''

    if decimal_value < 0:
        negative = True
        dec_val = fabs(decimal_value)
    else:
        negative = False
        dec_val = decimal_value

    degrees = trunc(dec_val)
    minutes_deg = dec_val - degrees

    minutes_mm = minutes_deg * 60.0
    minutes_out = trunc(minutes_mm)
    seconds = (minutes_mm - minutes_out)*60.0

    if negative:
        degrees = degrees
        return '-', degrees, minutes_out, seconds
    else:
        return '+', degrees, minutes_out, seconds