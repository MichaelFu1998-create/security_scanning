def normalize_lcdict(lcdict,
                     timecol='rjd',
                     magcols='all',
                     mingap=4.0,
                     normto='sdssr',
                     debugmode=False,
                     quiet=False):
    '''This normalizes magcols in `lcdict` using `timecol` to find timegroups.

    Parameters
    ----------

    lcdict : dict
        The input lcdict to process.

    timecol : str
        The key in the lcdict that is to be used to extract the time column.

    magcols : 'all' or list of str
        If this is 'all', all of the columns in the lcdict that are indicated to
        be magnitude measurement columns are normalized. If this is a list of
        str, must contain the keys of the lcdict specifying which magnitude
        columns will be normalized.

    mingap : float
        This defines how much the difference between consecutive measurements is
        allowed to be to consider them as parts of different timegroups. By
        default it is set to 4.0 days.

    normto : {'globalmedian', 'zero', 'jmag', 'hmag', 'kmag', 'bmag', 'vmag', 'sdssg', 'sdssr', 'sdssi'}
        This indicates which column will be the normalization target. If this is
        'globalmedian', the normalization will be to the global median of each
        LC column. If this is 'zero', will normalize to 0.0 for each LC
        column. Otherwise, will normalize to the value of one of the other keys
        in the lcdict['objectinfo'][magkey], meaning the normalization will be
        to some form of catalog magnitude.

    debugmode : bool
        If True, will indicate progress as time-groups are found and processed.

    quiet : bool
        If True, will not emit any messages when processing.

    Returns
    -------

    dict
        Returns the lcdict with the magnitude measurements normalized as
        specified. The normalization happens IN PLACE.

    '''

    # check if this lc has been normalized already. return as-is if so
    if 'lcnormcols' in lcdict and len(lcdict['lcnormcols']) > 0:
        if not quiet:
            LOGWARNING('this lightcurve is already normalized, returning...')
        return lcdict

    # first, get the LC timegroups
    if timecol in lcdict:
        times = lcdict[timecol]
    elif 'rjd' in lcdict:
        times = lcdict['rjd']
    # if there aren't any time columns in this lcdict, then we can't do any
    # normalization, return it as-is
    else:
        LOGERROR("can't figure out the time column to use, lcdict cols = %s" %
                 lcdict['columns'])
        return lcdict

    ngroups, timegroups = find_lc_timegroups(np.array(times),
                                             mingap=mingap)

    # HATLC V2 format
    if 'lcapertures' in lcdict:
        apertures = sorted(lcdict['lcapertures'].keys())
    # LCC-CSV-V1 format HATLC
    elif 'objectinfo' in lcdict and 'lcapertures' in lcdict['objectinfo']:
        apertures = sorted(lcdict['objectinfo']['lcapertures'].keys())


    aimcols = [('aim_%s' % x) for x in apertures if ('aim_%s' % x) in lcdict]
    armcols = [('arm_%s' % x) for x in apertures if ('arm_%s' % x) in lcdict]
    aepcols = [('aep_%s' % x)for x in apertures if ('aep_%s' % x) in lcdict]
    atfcols = [('atf_%s' % x) for x in apertures if ('atf_%s' % x) in lcdict]
    psimcols = [x for x in ['psim','psrm','psep','pstf'] if x in lcdict]
    irmcols = [('irm_%s' % x) for x in apertures if ('irm_%s' % x) in lcdict]
    iepcols = [('iep_%s' % x) for x in apertures if ('iep_%s' % x) in lcdict]
    itfcols = [('itf_%s' % x) for x in apertures if ('itf_%s' % x) in lcdict]

    # next, find all the mag columns to normalize
    if magcols == 'all':
        cols_to_normalize = (aimcols + armcols + aepcols + atfcols +
                             psimcols + irmcols + iepcols + itfcols)
    elif magcols == 'redmags':
        cols_to_normalize = (irmcols + (['psrm'] if 'psrm' in lcdict else []) +
                             irmcols)
    elif magcols == 'epdmags':
        cols_to_normalize = (aepcols + (['psep'] if 'psep' in lcdict else []) +
                             iepcols)
    elif magcols == 'tfamags':
        cols_to_normalize = (atfcols + (['pstf'] if 'pstf' in lcdict else []) +
                             itfcols)
    elif magcols == 'epdtfa':
        cols_to_normalize = (aepcols + (['psep'] if 'psep' in lcdict else []) +
                             iepcols + atfcols +
                             (['pstf'] if 'pstf' in lcdict else []) +
                             itfcols)
    else:
        cols_to_normalize = magcols.split(',')
        cols_to_normalize = [x.strip() for x in cols_to_normalize]

    colsnormalized = []

    # now, normalize each column
    for col in cols_to_normalize:

        if col in lcdict:

            mags = lcdict[col]
            mags = [(nan if x is None else x) for x in mags]
            mags = np.array(mags)

            colsnormalized.append(col)

            # find all the non-nan indices
            finite_ind = np.isfinite(mags)

            if any(finite_ind):

                # find the global median
                global_mag_median = np.median(mags[finite_ind])

                # go through the groups and normalize them to the median for
                # each group
                for tgind, tg in enumerate(timegroups):

                    finite_ind = np.isfinite(mags[tg])

                    # find this timegroup's median mag and normalize the mags in
                    # it to this median
                    group_median = np.median((mags[tg])[finite_ind])
                    mags[tg] = mags[tg] - group_median

                    if debugmode:
                        LOGDEBUG('%s group %s: elems %s, '
                                 'finite elems %s, median mag %s' %
                                 (col, tgind,
                                  len(mags[tg]),
                                  len(finite_ind),
                                  group_median))

            else:
                LOGWARNING('column %s is all nan, skipping...' % col)
                continue


            # now that everything is normalized to 0.0, add the global median
            # offset back to all the mags and write the result back to the dict
            if normto == 'globalmedian':
                mags = mags + global_mag_median
            elif normto in ('jmag', 'hmag', 'kmag',
                            'bmag', 'vmag',
                            'sdssg', 'sdssr', 'sdssi'):

                if (normto in lcdict['objectinfo'] and
                    lcdict['objectinfo'][normto] is not None):
                    mags = mags + lcdict['objectinfo'][normto]

                else:
                    if not quiet:
                        LOGWARNING('no %s available in lcdict, '
                                   'normalizing to global mag median' % normto)
                    normto = 'globalmedian'
                    mags = mags + global_mag_median

            lcdict[col] = mags

        else:
            if not quiet:
                LOGWARNING('column %s is not present, skipping...' % col)
            continue

    # add the lcnormcols key to the lcdict
    lcnormcols = ('cols normalized: %s - '
                  'min day gap: %s - '
                  'normalized to: %s') % (
        repr(colsnormalized),
        mingap,
        normto
    )
    lcdict['lcnormcols'] = lcnormcols

    return lcdict