def _aovhm_theta_worker(task):
    '''
    This is a parallel worker for the function below.

    Parameters
    ----------

    tasks : tuple
        This is of the form below::

            task[0] = times
            task[1] = mags
            task[2] = errs
            task[3] = frequency
            task[4] = nharmonics
            task[5] = magvariance

    Returns
    -------

    harmonic_aov_theta : float
        The value of the harmonic AoV statistic for the test frequency used.
        If something goes wrong with the calculation, nan is returned.

    '''

    times, mags, errs, frequency, nharmonics, magvariance = task

    try:

        theta = aovhm_theta(times, mags, errs, frequency,
                            nharmonics, magvariance)

        return theta

    except Exception as e:

        return npnan