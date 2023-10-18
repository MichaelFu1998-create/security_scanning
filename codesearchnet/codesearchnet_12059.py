def _get_acf_peakheights(lags, acf, npeaks=20, searchinterval=1):
    '''This calculates the relative peak heights for first npeaks in ACF.

    Usually, the first peak or the second peak (if its peak height > first peak)
    corresponds to the correct lag. When we know the correct lag, the period is
    then::

        bestperiod = time[lags == bestlag] - time[0]

    Parameters
    ----------

    lags : np.array
        An array of lags that the ACF is calculated at.

    acf : np.array
        The array containing the ACF values.

    npeaks : int
        THe maximum number of peaks to consider when finding peak heights.

    searchinterval : int
        From `scipy.signal.argrelmax`: "How many points on each side to use for
        the comparison to consider comparator(n, n+x) to be True." This
        effectively sets how many points on each of the current peak will be
        used to check if the current peak is the local maximum.

    Returns
    -------

    dict
        This returns a dict of the following form::

            {'maxinds':the indices of the lag array where maxes are,
             'maxacfs':the ACF values at each max,
             'maxlags':the lag values at each max,
             'mininds':the indices of the lag array where mins are,
             'minacfs':the ACF values at each min,
             'minlags':the lag values at each min,
             'relpeakheights':the relative peak heights of each rel. ACF peak,
             'relpeaklags':the lags at each rel. ACF peak found,
             'peakindices':the indices of arrays where each rel. ACF peak is,
             'bestlag':the lag value with the largest rel. ACF peak height,
             'bestpeakheight':the largest rel. ACF peak height,
             'bestpeakindex':the largest rel. ACF peak's number in all peaks}

    '''

    maxinds = argrelmax(acf, order=searchinterval)[0]
    maxacfs = acf[maxinds]
    maxlags = lags[maxinds]
    mininds = argrelmin(acf, order=searchinterval)[0]
    minacfs = acf[mininds]
    minlags = lags[mininds]

    relpeakheights = npzeros(npeaks)
    relpeaklags = npzeros(npeaks,dtype=npint64)
    peakindices = npzeros(npeaks,dtype=npint64)

    for peakind, mxi in enumerate(maxinds[:npeaks]):

        # check if there are no mins to the left
        # throw away this peak because it's probably spurious
        # (FIXME: is this OK?)
        if npall(mxi < mininds):
            continue

        leftminind = mininds[mininds < mxi][-1]  # the last index to the left
        rightminind = mininds[mininds > mxi][0]  # the first index to the right
        relpeakheights[peakind] = (
            acf[mxi] - (acf[leftminind] + acf[rightminind])/2.0
        )
        relpeaklags[peakind] = lags[mxi]
        peakindices[peakind] = peakind

    # figure out the bestperiod if possible
    if relpeakheights[0] > relpeakheights[1]:
        bestlag = relpeaklags[0]
        bestpeakheight = relpeakheights[0]
        bestpeakindex = peakindices[0]
    else:
        bestlag = relpeaklags[1]
        bestpeakheight = relpeakheights[1]
        bestpeakindex = peakindices[1]

    return {'maxinds':maxinds,
            'maxacfs':maxacfs,
            'maxlags':maxlags,
            'mininds':mininds,
            'minacfs':minacfs,
            'minlags':minlags,
            'relpeakheights':relpeakheights,
            'relpeaklags':relpeaklags,
            'peakindices':peakindices,
            'bestlag':bestlag,
            'bestpeakheight':bestpeakheight,
            'bestpeakindex':bestpeakindex}