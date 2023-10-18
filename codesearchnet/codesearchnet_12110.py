def independent_freq_count(frequencies, times, conservative=True):
    '''This estimates M: the number of independent frequencies in the periodogram.

    This follows the terminology on page 3 of Zechmeister & Kurster (2009)::

        M = DELTA_f / delta_f

    where::

        DELTA_f = freq.max() - freq.min()
        delta_f = 1.0/(times.max() - times.min())

    Parameters
    ----------

    frequencies : np.array
        The frequencies array used for the calculation of the GLS periodogram.

    times : np.array
        The array of input times used for the calculation of the GLS
        periodogram.

    conservative : bool
        If True, will follow the prescription given in Schwarzenberg-Czerny
        (2003):

        http://adsabs.harvard.edu/abs/2003ASPC..292..383S

        and estimate the number of independent frequences as::

            min(N_obs, N_freq, DELTA_f/delta_f)

    Returns
    -------

    M : int
        The number of independent frequencies.

    '''

    M = frequencies.ptp()*times.ptp()

    if conservative:
        M_eff = min([times.size, frequencies.size, M])
    else:
        M_eff = M

    return M_eff