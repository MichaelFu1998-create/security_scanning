def linspacestep(start, stop, step=1):
    """
    Create a vector of values over an interval with a specified step size.

    Parameters
    ----------

    start : float
        The beginning of the interval.
    stop : float
        The end of the interval.
    step : float
        The step size.

    Returns
    -------
    vector : :class:`numpy.ndarray`
        The vector of values.
    """
    # Find an integer number of steps
    numsteps = _np.int((stop-start)/step)

    # Do a linspace over the new range
    # that has the correct endpoint
    return _np.linspace(start, start+step*numsteps, numsteps+1)