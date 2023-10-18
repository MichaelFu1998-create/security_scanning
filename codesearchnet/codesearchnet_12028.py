def angle_wrap(angle, radians=False):
    '''Wraps the input angle to 360.0 degrees.

    Parameters
    ----------

    angle : float
        The angle to wrap around 360.0 deg.

    radians : bool
        If True, will assume that the input is in radians. The output will then
        also be in radians.

    Returns
    -------

    float
        Wrapped angle. If radians is True: input is assumed to be in radians,
        output is also in radians.

    '''

    if radians:
        wrapped = angle % (2.0*pi_value)
        if wrapped < 0.0:
            wrapped = 2.0*pi_value + wrapped

    else:

        wrapped = angle % 360.0
        if wrapped < 0.0:
            wrapped = 360.0 + wrapped

    return wrapped