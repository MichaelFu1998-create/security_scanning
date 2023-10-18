def make_fakelc(lcfile,
                outdir,
                magrms=None,
                randomizemags=True,
                randomizecoords=False,
                lcformat='hat-sql',
                lcformatdir=None,
                timecols=None,
                magcols=None,
                errcols=None):
    '''This preprocesses an input real LC and sets it up to be a fake LC.

    Parameters
    ----------

    lcfile : str
        This is an input light curve file that will be used to copy over the
        time-base. This will be used to generate the time-base for fake light
        curves to provide a realistic simulation of the observing window
        function.

    outdir : str
        The output directory where the the fake light curve will be written.

    magrms : dict
        This is a dict containing the SDSS r mag-RMS (SDSS rmag-MAD preferably)
        relation based on all light curves that the input lcfile is from. This
        will be used to generate the median mag and noise corresponding to the
        magnitude chosen for this fake LC.

    randomizemags : bool
        If this is True, then a random mag between the first and last magbin in
        magrms will be chosen as the median mag for this light curve. This
        choice will be weighted by the mag bin probability obtained from the
        magrms kwarg. Otherwise, the median mag will be taken from the input
        lcfile's lcdict['objectinfo']['sdssr'] key or a transformed SDSS r mag
        generated from the input lcfile's lcdict['objectinfo']['jmag'],
        ['hmag'], and ['kmag'] keys. The magrms relation for each magcol will be
        used to generate Gaussian noise at the correct level for the magbin this
        light curve's median mag falls into.

    randomizecoords : bool
        If this is True, will randomize the RA, DEC of the output fake object
        and not copy over the RA/DEC from the real input object.

    lcformat : str
        This is the `formatkey` associated with your input real light curve
        format, which you previously passed in to the `lcproc.register_lcformat`
        function. This will be used to look up how to find and read the light
        curve specified in `lcfile`.

    lcformatdir : str or None
        If this is provided, gives the path to a directory when you've stored
        your lcformat description JSONs, other than the usual directories lcproc
        knows to search for them in. Use this along with `lcformat` to specify
        an LC format JSON file that's not currently registered with lcproc.

    timecols : list of str or None
        The timecol keys to use from the input lcdict in generating the fake
        light curve. Fake LCs will be generated for each each
        timecol/magcol/errcol combination in the input light curve.

    magcols : list of str or None
        The magcol keys to use from the input lcdict in generating the fake
        light curve. Fake LCs will be generated for each each
        timecol/magcol/errcol combination in the input light curve.

    errcols : list of str or None
        The errcol keys to use from the input lcdict in generating the fake
        light curve. Fake LCs will be generated for each each
        timecol/magcol/errcol combination in the input light curve.

    Returns
    -------

    tuple
        A tuple of the following form is returned::

            (fakelc_fpath,
             fakelc_lcdict['columns'],
             fakelc_lcdict['objectinfo'],
             fakelc_lcdict['moments'])

    '''

    try:
        formatinfo = get_lcformat(lcformat,
                                  use_lcformat_dir=lcformatdir)
        if formatinfo:
            (fileglob, readerfunc,
             dtimecols, dmagcols, derrcols,
             magsarefluxes, normfunc) = formatinfo
        else:
            LOGERROR("can't figure out the light curve format")
            return None
    except Exception as e:
        LOGEXCEPTION("can't figure out the light curve format")
        return None

    # override the default timecols, magcols, and errcols
    # using the ones provided to the function
    if timecols is None:
        timecols = dtimecols
    if magcols is None:
        magcols = dmagcols
    if errcols is None:
        errcols = derrcols

    # read in the light curve
    lcdict = readerfunc(lcfile)
    if isinstance(lcdict, tuple) and isinstance(lcdict[0],dict):
        lcdict = lcdict[0]

    # set up the fakelcdict with a randomly assigned objectid
    fakeobjectid = sha512(npr.bytes(12)).hexdigest()[-8:]
    fakelcdict = {
        'objectid':fakeobjectid,
        'objectinfo':{'objectid':fakeobjectid},
        'columns':[],
        'moments':{},
        'origformat':lcformat,
    }


    # now, get the actual mag of this object and other info and use that to
    # populate the corresponding entries of the fakelcdict objectinfo
    if ('objectinfo' in lcdict and
        isinstance(lcdict['objectinfo'], dict)):

        objectinfo = lcdict['objectinfo']

        # get the RA
        if (not randomizecoords and 'ra' in objectinfo and
            objectinfo['ra'] is not None and
            np.isfinite(objectinfo['ra'])):

            fakelcdict['objectinfo']['ra'] = objectinfo['ra']

        else:

            # if there's no RA available, we'll assign a random one between 0
            # and 360.0
            LOGWARNING('%s: assigning a random right ascension' % lcfile)
            fakelcdict['objectinfo']['ra'] = npr.random()*360.0

        # get the DEC
        if (not randomizecoords and 'decl' in objectinfo and
            objectinfo['decl'] is not None and
            np.isfinite(objectinfo['decl'])):

            fakelcdict['objectinfo']['decl'] = objectinfo['decl']

        else:

            # if there's no DECL available, we'll assign a random one between
            # -90.0 and +90.0
            LOGWARNING(' %s: assigning a random declination' % lcfile)
            fakelcdict['objectinfo']['decl'] = npr.random()*180.0 - 90.0

        # get the SDSS r mag for this object
        # this will be used for getting the eventual mag-RMS relation later
        if ((not randomizemags) and 'sdssr' in objectinfo and
            objectinfo['sdssr'] is not None and
            np.isfinite(objectinfo['sdssr'])):

            fakelcdict['objectinfo']['sdssr'] = objectinfo['sdssr']

        # if the SDSS r is unavailable, but we have J, H, K: use those to get
        # the SDSS r by using transformations
        elif ((not randomizemags) and ('jmag' in objectinfo and
                                       objectinfo['jmag'] is not None and
                                       np.isfinite(objectinfo['jmag'])) and
              ('hmag' in objectinfo and
               objectinfo['hmag'] is not None and
               np.isfinite(objectinfo['hmag'])) and
              ('kmag' in objectinfo and
               objectinfo['kmag'] is not None and
               np.isfinite(objectinfo['kmag']))):

            LOGWARNING('used JHK mags to generate an SDSS r mag for %s' %
                       lcfile)
            fakelcdict['objectinfo']['sdssr'] = jhk_to_sdssr(
                objectinfo['jmag'],
                objectinfo['hmag'],
                objectinfo['kmag']
            )

        # if there are no mags available or we're specically told to randomize
        # them, generate a random mag between 8 and 16.0
        elif randomizemags and magrms:

            LOGWARNING(' %s: assigning a random mag weighted by mag '
                       'bin probabilities' % lcfile)

            magbins = magrms[magcols[0]]['binned_sdssr_median']
            binprobs = magrms[magcols[0]]['magbin_probabilities']

            # this is the center of the magbin chosen
            magbincenter = npr.choice(magbins,size=1,p=binprobs)

            # in this magbin, choose between center and -+ 0.25 mag
            chosenmag = (
                npr.random()*((magbincenter+0.25) - (magbincenter-0.25)) +
                (magbincenter-0.25)
            )

            fakelcdict['objectinfo']['sdssr'] = np.asscalar(chosenmag)

        # if there are no mags available at all, generate a random mag
        # between 8 and 16.0
        else:

            LOGWARNING(' %s: assigning a random mag from '
                       'uniform distribution between 8.0 and 16.0' % lcfile)

            fakelcdict['objectinfo']['sdssr'] = npr.random()*8.0 + 8.0

    # if there's no info available, generate fake info
    else:

        LOGWARNING('no object information found in %s, '
                   'generating random ra, decl, sdssr' %
                   lcfile)
        fakelcdict['objectinfo']['ra'] = npr.random()*360.0
        fakelcdict['objectinfo']['decl'] = npr.random()*180.0 - 90.0
        fakelcdict['objectinfo']['sdssr'] = npr.random()*8.0 + 8.0


    #
    # NOW FILL IN THE TIMES, MAGS, ERRS
    #

    # get the time columns
    for tcind, tcol in enumerate(timecols):

        if '.' in tcol:
            tcolget = tcol.split('.')
        else:
            tcolget = [tcol]

        if tcol not in fakelcdict:
            fakelcdict[tcol] = _dict_get(lcdict, tcolget)
            fakelcdict['columns'].append(tcol)

            # update the ndet with the first time column's size. it's possible
            # that different time columns have different lengths, but that would
            # be weird and we won't deal with it for now
            if tcind == 0:
                fakelcdict['objectinfo']['ndet'] = fakelcdict[tcol].size


    # get the mag columns
    for mcol in magcols:

        if '.' in mcol:
            mcolget = mcol.split('.')
        else:
            mcolget = [mcol]

        # put the mcol in only once
        if mcol not in fakelcdict:

            measuredmags = _dict_get(lcdict, mcolget)
            measuredmags = measuredmags[np.isfinite(measuredmags)]

            # if we're randomizing, get the mags from the interpolated mag-RMS
            # relation
            if (randomizemags and magrms and mcol in magrms and
                'interpolated_magmad' in magrms[mcol] and
                magrms[mcol]['interpolated_magmad'] is not None):

                interpfunc = magrms[mcol]['interpolated_magmad']
                lcmad = interpfunc(fakelcdict['objectinfo']['sdssr'])

                fakelcdict['moments'][mcol] = {
                    'median': fakelcdict['objectinfo']['sdssr'],
                    'mad': lcmad
                }

            # if we're not randomizing, get the median and MAD from the light
            # curve itself
            else:

                # we require at least 10 finite measurements
                if measuredmags.size > 9:

                    measuredmedian = np.median(measuredmags)
                    measuredmad = np.median(
                        np.abs(measuredmags - measuredmedian)
                    )
                    fakelcdict['moments'][mcol] = {'median':measuredmedian,
                                                   'mad':measuredmad}

                # if there aren't enough measurements in this LC, try to get the
                # median and RMS from the interpolated mag-RMS relation first
                else:

                    if (magrms and mcol in magrms and
                        'interpolated_magmad' in magrms[mcol] and
                        magrms[mcol]['interpolated_magmad'] is not None):

                        LOGWARNING(
                            'input LC %s does not have enough '
                            'finite measurements, '
                            'generating mag moments from '
                            'fakelc sdssr and the mag-RMS relation' % lcfile
                        )

                        interpfunc = magrms[mcol]['interpolated_magmad']
                        lcmad = interpfunc(fakelcdict['objectinfo']['sdssr'])

                        fakelcdict['moments'][mcol] = {
                            'median': fakelcdict['objectinfo']['sdssr'],
                            'mad': lcmad
                        }

                    # if we don't have the mag-RMS relation either, then we
                    # can't do anything for this light curve, generate a random
                    # MAD between 5e-4 and 0.1
                    else:

                        LOGWARNING(
                            'input LC %s does not have enough '
                            'finite measurements and '
                            'no mag-RMS relation provided '
                            'assigning a random MAD between 5.0e-4 and 0.1'
                            % lcfile
                        )

                        fakelcdict['moments'][mcol] = {
                            'median':fakelcdict['objectinfo']['sdssr'],
                            'mad':npr.random()*(0.1 - 5.0e-4) + 5.0e-4
                        }

            # the magnitude column is set to all zeros initially. this will be
            # filled in by the add_fakelc_variability function below
            fakelcdict[mcol] = np.full_like(_dict_get(lcdict, mcolget), 0.0)
            fakelcdict['columns'].append(mcol)


    # get the err columns
    for mcol, ecol in zip(magcols, errcols):

        if '.' in ecol:
            ecolget = ecol.split('.')
        else:
            ecolget = [ecol]

        if ecol not in fakelcdict:

            measurederrs = _dict_get(lcdict, ecolget)
            measurederrs = measurederrs[np.isfinite(measurederrs)]

            # if we're randomizing, get the errs from the interpolated mag-RMS
            # relation
            if (randomizemags and magrms and mcol in magrms and
                'interpolated_magmad' in magrms[mcol] and
                magrms[mcol]['interpolated_magmad'] is not None):

                interpfunc = magrms[mcol]['interpolated_magmad']
                lcmad = interpfunc(fakelcdict['objectinfo']['sdssr'])

                # the median of the errs = lcmad
                # the mad of the errs is 0.1 x lcmad
                fakelcdict['moments'][ecol] = {
                    'median': lcmad,
                    'mad': 0.1*lcmad
                }

            else:

                # we require at least 10 finite measurements
                # we'll calculate the median and MAD of the errs to use later on
                if measurederrs.size > 9:
                    measuredmedian = np.median(measurederrs)
                    measuredmad = np.median(
                        np.abs(measurederrs - measuredmedian)
                    )
                    fakelcdict['moments'][ecol] = {'median':measuredmedian,
                                                   'mad':measuredmad}
                else:

                    if (magrms and mcol in magrms and
                        'interpolated_magmad' in magrms[mcol] and
                        magrms[mcol]['interpolated_magmad'] is not None):

                        LOGWARNING(
                            'input LC %s does not have enough '
                            'finite measurements, '
                            'generating err moments from '
                            'the mag-RMS relation' % lcfile
                        )

                        interpfunc = magrms[mcol]['interpolated_magmad']
                        lcmad = interpfunc(fakelcdict['objectinfo']['sdssr'])

                        fakelcdict['moments'][ecol] = {
                            'median': lcmad,
                            'mad': 0.1*lcmad
                        }

                    # if we don't have the mag-RMS relation either, then we
                    # can't do anything for this light curve, generate a random
                    # MAD between 5e-4 and 0.1
                    else:

                        LOGWARNING(
                            'input LC %s does not have '
                            'enough finite measurements and '
                            'no mag-RMS relation provided, '
                            'generating errs randomly' % lcfile
                        )
                        fakelcdict['moments'][ecol] = {
                            'median':npr.random()*(0.01 - 5.0e-4) + 5.0e-4,
                            'mad':npr.random()*(0.01 - 5.0e-4) + 5.0e-4
                        }

            # the errors column is set to all zeros initially. this will be
            # filled in by the add_fakelc_variability function below.
            fakelcdict[ecol] = np.full_like(_dict_get(lcdict, ecolget), 0.0)
            fakelcdict['columns'].append(ecol)



    # add the timecols, magcols, errcols to the lcdict
    fakelcdict['timecols'] = timecols
    fakelcdict['magcols'] = magcols
    fakelcdict['errcols'] = errcols

    # generate an output file name
    fakelcfname = '%s-fakelc.pkl' % fakelcdict['objectid']
    fakelcfpath = os.path.abspath(os.path.join(outdir, fakelcfname))

    # write this out to the output directory
    with open(fakelcfpath,'wb') as outfd:
        pickle.dump(fakelcdict, outfd, protocol=pickle.HIGHEST_PROTOCOL)

    # return the fakelc path, its columns, info, and moments so we can put them
    # into a collection DB later on
    LOGINFO('real LC %s -> fake LC %s OK' % (lcfile, fakelcfpath))

    return (fakelcfpath, fakelcdict['columns'],
            fakelcdict['objectinfo'], fakelcdict['moments'])