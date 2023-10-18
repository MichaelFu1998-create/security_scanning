def update_checkplotdict_nbrlcs(
        checkplotdict,
        timecol, magcol, errcol,
        lcformat='hat-sql',
        lcformatdir=None,
        verbose=True,
):

    '''For all neighbors in a checkplotdict, make LCs and phased LCs.

    Parameters
    ----------

    checkplotdict : dict
        This is the checkplot to process. The light curves for the neighbors to
        the object here will be extracted from the stored file paths, and this
        function will make plots of these time-series. If the object has 'best'
        periods and epochs generated by period-finder functions in this
        checkplotdict, phased light curve plots of each neighbor will be made
        using these to check the effects of blending.

    timecol,magcol,errcol : str
        The timecol, magcol, and errcol keys used to generate this object's
        checkplot. This is used to extract the correct times-series from the
        neighbors' light curves.

    lcformat : str
        This is the `formatkey` associated with your light curve format, which
        you previously passed in to the `lcproc.register_lcformat`
        function. This will be used to look up how to find and read the light
        curves specified in `basedir` or `use_list_of_filenames`.

    lcformatdir : str or None
        If this is provided, gives the path to a directory when you've stored
        your lcformat description JSONs, other than the usual directories lcproc
        knows to search for them in. Use this along with `lcformat` to specify
        an LC format JSON file that's not currently registered with lcproc.

    Returns
    -------

    dict
        The input checkplotdict is returned with the neighor light curve plots
        added in.

    '''

    try:
        formatinfo = get_lcformat(lcformat,
                                  use_lcformat_dir=lcformatdir)
        if formatinfo:
            (dfileglob, readerfunc,
             dtimecols, dmagcols, derrcols,
             magsarefluxes, normfunc) = formatinfo
        else:
            LOGERROR("can't figure out the light curve format")
            return checkplotdict
    except Exception as e:
        LOGEXCEPTION("can't figure out the light curve format")
        return checkplotdict

    if not ('neighbors' in checkplotdict and
            checkplotdict['neighbors'] and
            len(checkplotdict['neighbors']) > 0):

        LOGERROR('no neighbors for %s, not updating...' %
                 (checkplotdict['objectid']))
        return checkplotdict

    # get our object's magkeys to compare to the neighbor
    objmagkeys = {}

    # handle diff generations of checkplots
    if 'available_bands' in checkplotdict['objectinfo']:
        mclist = checkplotdict['objectinfo']['available_bands']
    else:
        mclist = ('bmag','vmag','rmag','imag','jmag','hmag','kmag',
                  'sdssu','sdssg','sdssr','sdssi','sdssz')

    for mc in mclist:
        if (mc in checkplotdict['objectinfo'] and
            checkplotdict['objectinfo'][mc] is not None and
            np.isfinite(checkplotdict['objectinfo'][mc])):

            objmagkeys[mc] = checkplotdict['objectinfo'][mc]


    # if there are actually neighbors, go through them in order
    for nbr in checkplotdict['neighbors']:

        objectid, lcfpath = (nbr['objectid'],
                             nbr['lcfpath'])

        # get the light curve
        if not os.path.exists(lcfpath):
            LOGERROR('objectid: %s, neighbor: %s, '
                     'lightcurve: %s not found, skipping...' %
                     (checkplotdict['objectid'], objectid, lcfpath))
            continue

        lcdict = readerfunc(lcfpath)

        # this should handle lists/tuples being returned by readerfunc
        # we assume that the first element is the actual lcdict
        # FIXME: figure out how to not need this assumption
        if ( (isinstance(lcdict, (list, tuple))) and
             (isinstance(lcdict[0], dict)) ):
            lcdict = lcdict[0]


        # 0. get this neighbor's magcols and get the magdiff and colordiff
        # between it and the object

        nbrmagkeys = {}

        for mc in objmagkeys:

            if (('objectinfo' in lcdict) and
                (isinstance(lcdict['objectinfo'], dict)) and
                (mc in lcdict['objectinfo']) and
                (lcdict['objectinfo'][mc] is not None) and
                (np.isfinite(lcdict['objectinfo'][mc]))):

                nbrmagkeys[mc] = lcdict['objectinfo'][mc]

        # now calculate the magdiffs
        magdiffs = {}
        for omc in objmagkeys:
            if omc in nbrmagkeys:
                magdiffs[omc] = objmagkeys[omc] - nbrmagkeys[omc]

        # calculate colors and colordiffs
        colordiffs = {}

        # generate the list of colors to get
        # NOTE: here, we don't really bother with new/old gen checkplots
        # maybe change this later to handle arbitrary colors

        for ctrio in (['bmag','vmag','bvcolor'],
                      ['vmag','kmag','vkcolor'],
                      ['jmag','kmag','jkcolor'],
                      ['sdssi','jmag','ijcolor'],
                      ['sdssg','kmag','gkcolor'],
                      ['sdssg','sdssr','grcolor']):
            m1, m2, color = ctrio

            if (m1 in objmagkeys and
                m2 in objmagkeys and
                m1 in nbrmagkeys and
                m2 in nbrmagkeys):

                objcolor = objmagkeys[m1] - objmagkeys[m2]
                nbrcolor = nbrmagkeys[m1] - nbrmagkeys[m2]
                colordiffs[color] = objcolor - nbrcolor

        # finally, add all the color and magdiff info to the nbr dict
        nbr.update({'magdiffs':magdiffs,
                    'colordiffs':colordiffs})

        #
        # process magcols
        #

        # normalize using the special function if specified
        if normfunc is not None:
            lcdict = normfunc(lcdict)

        try:

            # get the times, mags, and errs
            # dereference the columns and get them from the lcdict
            if '.' in timecol:
                timecolget = timecol.split('.')
            else:
                timecolget = [timecol]
            times = _dict_get(lcdict, timecolget)

            if '.' in magcol:
                magcolget = magcol.split('.')
            else:
                magcolget = [magcol]
            mags = _dict_get(lcdict, magcolget)

            if '.' in errcol:
                errcolget = errcol.split('.')
            else:
                errcolget = [errcol]
            errs = _dict_get(lcdict, errcolget)

        except KeyError:

            LOGERROR('LC for neighbor: %s (target object: %s) does not '
                     'have one or more of the required columns: %s, '
                     'skipping...' %
                     (objectid, checkplotdict['objectid'],
                      ', '.join([timecol, magcol, errcol])))
            continue

        # filter the input times, mags, errs; do sigclipping and normalization
        stimes, smags, serrs = sigclip_magseries(times,
                                                 mags,
                                                 errs,
                                                 magsarefluxes=magsarefluxes,
                                                 sigclip=4.0)

        # normalize here if not using special normalization
        if normfunc is None:
            ntimes, nmags = normalize_magseries(
                stimes, smags,
                magsarefluxes=magsarefluxes
            )
            xtimes, xmags, xerrs = ntimes, nmags, serrs
        else:
            xtimes, xmags, xerrs = stimes, smags, serrs


        # check if this neighbor has enough finite points in its LC
        # fail early if not enough light curve points
        if ((xtimes is None) or (xmags is None) or (xerrs is None) or
            (xtimes.size < 49) or (xmags.size < 49) or (xerrs.size < 49)):

            LOGERROR("one or more of times, mags, errs appear to be None "
                     "after sig-clipping. are the measurements all nan? "
                     "can't make neighbor light curve plots "
                     "for target: %s, neighbor: %s, neighbor LC: %s" %
                     (checkplotdict['objectid'],
                      nbr['objectid'],
                      nbr['lcfpath']))
            continue

        #
        # now we can start doing stuff if everything checks out
        #

        # make an unphased mag-series plot
        nbrdict = _pkl_magseries_plot(xtimes,
                                      xmags,
                                      xerrs,
                                      magsarefluxes=magsarefluxes)
        # update the nbr
        nbr.update(nbrdict)

        # for each lspmethod in the checkplot, make a corresponding plot for
        # this neighbor

        # figure out the period finder methods present
        if 'pfmethods' in checkplotdict:
            pfmethods = checkplotdict['pfmethods']
        else:
            pfmethods = []
            for cpkey in checkplotdict:
                for pfkey in PFMETHODS:
                    if pfkey in cpkey:
                        pfmethods.append(pfkey)

        for lspt in pfmethods:

            # initialize this lspmethod entry
            nbr[lspt] = {}

            # we only care about the best period and its options
            operiod, oepoch = (checkplotdict[lspt][0]['period'],
                               checkplotdict[lspt][0]['epoch'])
            (ophasewrap, ophasesort, ophasebin,
             ominbinelems, oplotxlim) = (
                 checkplotdict[lspt][0]['phasewrap'],
                 checkplotdict[lspt][0]['phasesort'],
                 checkplotdict[lspt][0]['phasebin'],
                 checkplotdict[lspt][0]['minbinelems'],
                 checkplotdict[lspt][0]['plotxlim'],
            )

            # make the phasedlc plot for this period
            nbr = _pkl_phased_magseries_plot(
                nbr,
                lspt.split('-')[1],  # this splits '<pfindex>-<pfmethod>'
                0,
                xtimes, xmags, xerrs,
                operiod, oepoch,
                phasewrap=ophasewrap,
                phasesort=ophasesort,
                phasebin=ophasebin,
                minbinelems=ominbinelems,
                plotxlim=oplotxlim,
                magsarefluxes=magsarefluxes,
                verbose=verbose,
                override_pfmethod=lspt
            )

    # at this point, this neighbor's dict should be up to date with all
    # info, magseries plot, and all phased LC plots
    # return the updated checkplotdict
    return checkplotdict