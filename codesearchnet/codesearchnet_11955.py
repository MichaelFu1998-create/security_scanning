def filter_tess_lcdict(lcdict,
                       filterqualityflags=True,
                       nanfilter='sap,pdc,time',
                       timestoignore=None,
                       quiet=False):
    '''This filters the provided TESS `lcdict`, removing nans and bad
    observations.

    By default, this function removes points in the TESS LC that have ANY
    quality flags set.

    Parameters
    ----------

    lcdict : lcdict
        An `lcdict` produced by `consolidate_tess_fitslc` or
        `read_tess_fitslc`.

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
    if filterqualityflags:

        nbefore = lcdict['time'].size
        filterind = lcdict['quality'] == 0

        for col in cols:
            if '.' in col:
                key, subkey = col.split('.')
                lcdict[key][subkey] = lcdict[key][subkey][filterind]
            else:
                lcdict[col] = lcdict[col][filterind]

        nafter = lcdict['time'].size
        if not quiet:
            LOGINFO('applied quality flag filter, '
                    'ndet before = %s, ndet after = %s'
                    % (nbefore, nafter))


    if nanfilter and nanfilter == 'sap,pdc,time':
        notnanind = (
            np.isfinite(lcdict['sap']['sap_flux']) &
            np.isfinite(lcdict['sap']['sap_flux_err']) &
            np.isfinite(lcdict['pdc']['pdcsap_flux']) &
            np.isfinite(lcdict['pdc']['pdcsap_flux_err']) &
            np.isfinite(lcdict['time'])
        )
    elif nanfilter and nanfilter == 'sap,time':
        notnanind = (
            np.isfinite(lcdict['sap']['sap_flux']) &
            np.isfinite(lcdict['sap']['sap_flux_err']) &
            np.isfinite(lcdict['time'])
        )
    elif nanfilter and nanfilter == 'pdc,time':
        notnanind = (
            np.isfinite(lcdict['pdc']['pdcsap_flux']) &
            np.isfinite(lcdict['pdc']['pdcsap_flux_err']) &
            np.isfinite(lcdict['time'])
        )
    elif nanfilter is None:
        pass
    else:
        raise NotImplementedError

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

        if not quiet:
            LOGINFO('removed nans, ndet before = %s, ndet after = %s'
                    % (nbefore, nafter))


    # exclude all times in timestoignore
    if (timestoignore and
        isinstance(timestoignore, list) and
        len(timestoignore) > 0):

        exclind = np.full_like(lcdict['time'],True).astype(bool)
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
        if not quiet:
            LOGINFO('removed timestoignore, ndet before = %s, ndet after = %s'
                    % (nbefore, nafter))

    return lcdict