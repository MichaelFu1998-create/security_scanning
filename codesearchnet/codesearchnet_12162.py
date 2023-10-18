def filter_kepler_lcdict(lcdict,
                         filterflags=True,
                         nanfilter='sap,pdc',
                         timestoignore=None):
    '''This filters the Kepler `lcdict`, removing nans and bad
    observations.

    By default, this function removes points in the Kepler LC that have ANY
    quality flags set.

    Parameters
    ----------

    lcdict : lcdict
        An `lcdict` produced by `consolidate_kepler_fitslc` or
        `read_kepler_fitslc`.

    filterflags : bool
        If True, will remove any measurements that have non-zero quality flags
        present. This usually indicates an issue with the instrument or
        spacecraft.

    nanfilter : {'sap','pdc','sap,pdc'}
        Indicates the flux measurement type(s) to apply the filtering to.

    timestoignore : list of tuples or None
        This is of the form::

            [(time1_start, time1_end), (time2_start, time2_end), ...]

        and indicates the start and end times to mask out of the final
        lcdict. Use this to remove anything that wasn't caught by the quality
        flags.

    Returns
    -------

    lcdict
        Returns an `lcdict` (this is useable by most astrobase functions for LC
        processing). The `lcdict` is filtered IN PLACE!

    '''

    cols = lcdict['columns']

    # filter all bad LC points as noted by quality flags
    if filterflags:

        nbefore = lcdict['time'].size
        filterind = lcdict['sap_quality'] == 0

        for col in cols:
            if '.' in col:
                key, subkey = col.split('.')
                lcdict[key][subkey] = lcdict[key][subkey][filterind]
            else:
                lcdict[col] = lcdict[col][filterind]

        nafter = lcdict['time'].size
        LOGINFO('applied quality flag filter, ndet before = %s, ndet after = %s'
                % (nbefore, nafter))


    if nanfilter and nanfilter == 'sap,pdc':
        notnanind = (
            npisfinite(lcdict['sap']['sap_flux']) &
            npisfinite(lcdict['pdc']['pdcsap_flux']) &
            npisfinite(lcdict['time'])
        )
    elif nanfilter and nanfilter == 'sap':
        notnanind = (
            npisfinite(lcdict['sap']['sap_flux']) &
            npisfinite(lcdict['time'])
        )
    elif nanfilter and nanfilter == 'pdc':
        notnanind = (
            npisfinite(lcdict['pdc']['pdcsap_flux']) &
            npisfinite(lcdict['time'])
        )


    # remove nans from all columns
    if nanfilter:

        nbefore = lcdict['time'].size
        for col in cols:
            if '.' in col:
                key, subkey = col.split('.')
                lcdict[key][subkey] = lcdict[key][subkey][notnanind]
            else:
                lcdict[col] = lcdict[col][notnanind]

        nafter = lcdict['time'].size

        LOGINFO('removed nans, ndet before = %s, ndet after = %s'
                % (nbefore, nafter))


    # exclude all times in timestoignore
    if (timestoignore and
        isinstance(timestoignore, list) and
        len(timestoignore) > 0):

        exclind = npfull_like(lcdict['time'], True, dtype=np.bool_)
        nbefore = exclind.size

        # get all the masks
        for ignoretime in timestoignore:
            time0, time1 = ignoretime[0], ignoretime[1]
            thismask = ~((lcdict['time'] >= time0) & (lcdict['time'] <= time1))
            exclind = exclind & thismask

        # apply the masks
        for col in cols:
            if '.' in col:
                key, subkey = col.split('.')
                lcdict[key][subkey] = lcdict[key][subkey][exclind]
            else:
                lcdict[col] = lcdict[col][exclind]

        nafter = lcdict['time'].size
        LOGINFO('removed timestoignore, ndet before = %s, ndet after = %s'
                % (nbefore, nafter))

    return lcdict