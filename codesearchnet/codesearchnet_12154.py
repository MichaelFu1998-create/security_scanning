def _stellingwerf_pdm_worker(task):
    '''
    This is a parallel worker for the function below.

    Parameters
    ----------

    task : tuple
        This is of the form below::

            task[0] = times
            task[1] = mags
            task[2] = errs
            task[3] = frequency
            task[4] = binsize
            task[5] = minbin

    Returns
    -------

    theta_pdm : float
        The theta value at the specified frequency. nan if the calculation
        fails.

    '''

    times, mags, errs, frequency, binsize, minbin = task

    try:

        theta = stellingwerf_pdm_theta(times, mags, errs, frequency,
                                       binsize=binsize, minbin=minbin)

        return theta

    except Exception as e:

        return npnan