def _bls_runner(times,
                mags,
                nfreq,
                freqmin,
                stepsize,
                nbins,
                minduration,
                maxduration):
    '''This runs the pyeebls.eebls function using the given inputs.

    Parameters
    ----------

    times,mags : np.array
        The input magnitude time-series to search for transits.

    nfreq : int
        The number of frequencies to use when searching for transits.

    freqmin : float
        The minimum frequency of the period-search -> max period that will be
        used for the search.

    stepsize : float
        The step-size in frequency to use to generate a frequency-grid.

    nbins : int
        The number of phase bins to use.

    minduration : float
        The minimum fractional transit duration that will be considered.

    maxduration : float
        The maximum fractional transit duration that will be considered.

    Returns
    -------

    dict
        Returns a dict of the form::

            {
                'power':           the periodogram power array,
                'bestperiod':      the best period found,
                'bestpower':       the highest peak of the periodogram power,
                'transdepth':      transit depth found by eebls.f,
                'transduration':   transit duration found by eebls.f,
                'transingressbin': transit ingress bin found by eebls.f,
                'transegressbin':  transit egress bin found by eebls.f,
            }

    '''

    workarr_u = npones(times.size)
    workarr_v = npones(times.size)

    blsresult = eebls(times, mags,
                      workarr_u, workarr_v,
                      nfreq, freqmin, stepsize,
                      nbins, minduration, maxduration)

    return {'power':blsresult[0],
            'bestperiod':blsresult[1],
            'bestpower':blsresult[2],
            'transdepth':blsresult[3],
            'transduration':blsresult[4],
            'transingressbin':blsresult[5],
            'transegressbin':blsresult[6]}