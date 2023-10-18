def pwd_phasebin(phases, mags, binsize=0.002, minbin=9):
    '''
    This bins the phased mag series using the given binsize.

    '''

    bins = np.arange(0.0, 1.0, binsize)
    binnedphaseinds = npdigitize(phases, bins)

    binnedphases, binnedmags = [], []

    for x in npunique(binnedphaseinds):

        thisbin_inds = binnedphaseinds == x
        thisbin_phases = phases[thisbin_inds]
        thisbin_mags = mags[thisbin_inds]
        if thisbin_inds.size > minbin:
            binnedphases.append(npmedian(thisbin_phases))
            binnedmags.append(npmedian(thisbin_mags))

    return np.array(binnedphases), np.array(binnedmags)