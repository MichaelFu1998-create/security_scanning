def T_converter(T, current, desired):
    r'''Converts the a temperature reading made in any of the scales
    'ITS-90', 'ITS-68','ITS-48', 'ITS-76', or 'ITS-27' to any of the other
    scales. Not all temperature ranges can be converted to other ranges; for
    instance, 'ITS-76' is purely for low temperatures, and 5 K on it has no
    conversion to 'ITS-90' or any other scale. Both a conversion to ITS-90 and
    to the desired scale must be possible for the conversion to occur.
    The conversion uses cubic spline interpolation.

    ITS-68 conversion is valid from 14 K to 4300 K.
    ITS-48 conversion is valid from 93.15 K to 4273.15 K
    ITS-76 conversion is valid from 5 K to 27 K.
    ITS-27 is valid from 903.15 K to 4273.15 k.

    Parameters
    ----------
    T : float
        Temperature, on `current` scale [K]
    current : str
        String representing the scale T is in, 'ITS-90', 'ITS-68',
        'ITS-48', 'ITS-76', or 'ITS-27'.
    desired : str
        String representing the scale T will be returned in, 'ITS-90',
        'ITS-68', 'ITS-48', 'ITS-76', or 'ITS-27'.

    Returns
    -------
    T : float
        Temperature, on scale `desired` [K]

    Notes
    -----
    Because the conversion is performed by spline functions, a re-conversion
    of a value will not yield exactly the original value. However, it is quite
    close.

    The use of splines is quite quick (20 micro seconds/calculation). While
    just a spline for one-way conversion could be used, a numerical solver
    would have to be used to obtain an exact result for the reverse conversion.
    This was found to take approximately 1 ms/calculation, depending on the
    region.

    Examples
    --------
    >>> T_converter(500, 'ITS-68', 'ITS-48')
    499.9470092992346

    References
    ----------
    .. [1] Wier, Ron D., and Robert N. Goldberg. "On the Conversion of
       Thermodynamic Properties to the Basis of the International Temperature
       Scale of 1990." The Journal of Chemical Thermodynamics 28, no. 3
       (March 1996): 261-76. doi:10.1006/jcht.1996.0026.
    .. [2] Goldberg, Robert N., and R. D. Weir. "Conversion of Temperatures
       and Thermodynamic Properties to the Basis of the International
       Temperature Scale of 1990 (Technical Report)." Pure and Applied
       Chemistry 64, no. 10 (1992): 1545-1562. doi:10.1351/pac199264101545.
    '''
    def range_check(T, Tmin, Tmax):
        if T < Tmin or T > Tmax:
            raise Exception('Temperature conversion is outside one or both scales')

    try:
        if current == 'ITS-90':
            pass
        elif current == 'ITS-68':
            range_check(T, 13.999, 4300.0001)
            T = T68_to_T90(T)
        elif current == 'ITS-76':
            range_check(T, 4.9999, 27.0001)
            T = T76_to_T90(T)
        elif current == 'ITS-48':
            range_check(T, 93.149999, 4273.15001)
            T = T48_to_T90(T)
        elif current == 'ITS-27':
            range_check(T, 903.15, 4273.15)
            T = T27_to_T90(T)
        else:
            raise Exception('Current scale not supported')
        # T should be in ITS-90 now

        if desired == 'ITS-90':
            pass
        elif desired == 'ITS-68':
            range_check(T, 13.999, 4300.0001)
            T = T90_to_T68(T)
        elif desired == 'ITS-76':
            range_check(T, 4.9999, 27.0001)
            T = T90_to_T76(T)
        elif desired == 'ITS-48':
            range_check(T, 93.149999, 4273.15001)
            T = T90_to_T48(T)
        elif desired == 'ITS-27':
            range_check(T, 903.15, 4273.15)
            T = T90_to_T27(T)
        else:
            raise Exception('Desired scale not supported')
    except ValueError:
        raise Exception('Temperature could not be converted to desired scale')
    return float(T)