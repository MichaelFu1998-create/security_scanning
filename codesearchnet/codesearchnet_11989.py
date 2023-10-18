def normalize_lcdict_byinst(
        lcdict,
        magcols='all',
        normto='sdssr',
        normkeylist=('stf','ccd','flt','fld','prj','exp'),
        debugmode=False,
        quiet=False
):
    '''This is a function to normalize light curves across all instrument
    combinations present.

    Use this to normalize a light curve containing a variety of:

    - HAT station IDs ('stf')
    - camera IDs ('ccd')
    - filters ('flt')
    - observed field names ('fld')
    - HAT project IDs ('prj')
    - exposure times ('exp')

    Parameters
    ----------

    lcdict : dict
        The input lcdict to process.

    magcols : 'all' or list of str
        If this is 'all', all of the columns in the lcdict that are indicated to
        be magnitude measurement columns are normalized. If this is a list of
        str, must contain the keys of the lcdict specifying which magnitude
        columns will be normalized.

    normto : {'zero', 'jmag', 'hmag', 'kmag', 'bmag', 'vmag', 'sdssg', 'sdssr', 'sdssi'}
        This indicates which column will be the normalization target. If this is
        'zero', will normalize to 0.0 for each LC column. Otherwise, will
        normalize to the value of one of the other keys in the
        lcdict['objectinfo'][magkey], meaning the normalization will be to some
        form of catalog magnitude.

    normkeylist : list of str
        These are the column keys to use to form the normalization
        index. Measurements in the specified `magcols` with identical
        normalization index values will be considered as part of a single
        measurement 'era', and will be normalized to zero. Once all eras have
        been normalized this way, the final light curve will be re-normalized as
        specified in `normto`.

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
    if 'lcinstnormcols' in lcdict and len(lcdict['lcinstnormcols']) > 0:
        if not quiet:
            LOGWARNING('this lightcurve is already '
                       'normalized by instrument keys, '
                       'returning...')
        return lcdict

    # generate the normalization key
    normkeycols = []
    availablenormkeys = []
    for key in normkeylist:
        if key in lcdict and lcdict[key] is not None:
            normkeycols.append(lcdict[key])
            availablenormkeys.append(key)

    # transpose to turn these into rows
    normkeycols = list(zip(*normkeycols))

    # convert to a string rep for each key and post-process for simplicity
    allkeys = [repr(x) for x in normkeycols]
    allkeys = [a.replace('(','').replace(')','').replace("'",'').replace(' ','')
               for a in allkeys]

    # turn these into a numpy array and get the unique values
    allkeys = np.array(allkeys)
    normkeys = np.unique(allkeys)

    # figure out the apertures
    # HATLC V2 format
    if 'lcapertures' in lcdict:
        apertures = sorted(lcdict['lcapertures'].keys())
    # LCC-CSV-V1 format HATLC
    elif 'objectinfo' in lcdict and 'lcapertures' in lcdict['objectinfo']:
        apertures = sorted(lcdict['objectinfo']['lcapertures'].keys())

    # put together the column names
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

    # go through each column and normalize them
    for col in cols_to_normalize:

        if col in lcdict:

            # note: this requires the columns in ndarray format
            # unlike normalize_lcdict
            thismags = lcdict[col]

            # go through each key in normusing
            for nkey in normkeys:

                thisind = allkeys == nkey

                # make sure we have at least 3 elements in the matched set of
                # magnitudes corresponding to this key. also make sure that the
                # magnitudes corresponding to this key aren't all nan.
                thismagsize = thismags[thisind].size
                thismagfinite = np.where(np.isfinite(thismags[thisind]))[0].size

                if thismagsize > 2 and thismagfinite > 2:

                    # do the normalization and update the thismags in the lcdict
                    medmag = np.nanmedian(thismags[thisind])
                    lcdict[col][thisind] = lcdict[col][thisind] - medmag

                    if debugmode:
                        LOGDEBUG('magcol: %s, currkey: "%s", nelem: %s, '
                                 'medmag: %s' %
                                 (col, nkey, len(thismags[thisind]), medmag))

                # we remove mags that correspond to keys with less than 3
                # (finite) elements because we can't get the median mag
                # correctly and renormalizing them to zero would just set them
                # to zero
                else:

                    lcdict[col][thisind] = np.nan

            # everything should now be normalized to zero
            # add back the requested normto
            if normto in ('jmag', 'hmag', 'kmag',
                          'bmag', 'vmag',
                          'sdssg', 'sdssr', 'sdssi'):

                if (normto in lcdict['objectinfo'] and
                    lcdict['objectinfo'][normto] is not None):
                    lcdict[col] = lcdict[col] + lcdict['objectinfo'][normto]

                else:
                    if not quiet:
                        LOGWARNING('no %s available in lcdict, '
                                   'normalizing to 0.0' % normto)
                    normto = 'zero'

            # update the colsnormalized list
            colsnormalized.append(col)

        else:
            if not quiet:
                LOGWARNING('column %s is not present, skipping...' % col)
            continue

    # add the lcnormcols key to the lcdict
    lcinstnormcols = ('cols normalized: %s - '
                      'normalized to: %s - '
                      'norm keys used: %s') % (repr(colsnormalized),
                                               normto,
                                               repr(availablenormkeys))
    lcdict['lcinstnormcols'] = lcinstnormcols

    return lcdict